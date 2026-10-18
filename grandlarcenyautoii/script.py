import pypandoc

content = r'''# TryHackMe — GrandLarcenyAuto II

> Rapport de laboratoire : reverse engineering, analyse d'API et contrôle d'accès.

## Informations générales

- **Plateforme :** TryHackMe
- **Room :** GrandLarcenyAuto II
- **Difficulté :** Intermédiaire
- **Cible du laboratoire :** `http://gla2.thm/`
- **Technologies observées :** Godot, .NET, ASP.NET Core / Kestrel
- **Outils :** `curl`, `dirsearch`, Wappalyzer, ILSpy, Python 3

> Ce document décrit une analyse réalisée dans le cadre du laboratoire TryHackMe. Les tests et exemples de requêtes sont destinés exclusivement à cet environnement autorisé.

## 1. Objectif

Le défi présente un jeu dont le coffre-fort visible n'est qu'un leurre. Le véritable objectif consiste à analyser le client, comprendre son protocole de communication avec le backend, puis identifier une faiblesse dans la logique de validation de la réclamation finale.

La démarche suivie a été la suivante :

1. Reconnaître les services et les routes HTTP exposés.
2. Extraire et analyser le client Godot/.NET.
3. Reconstituer le protocole de session et de checkpoints.
4. Examiner la signature HMAC et la génération du rôle.
5. Tester une hypothèse de manipulation du paramètre `role`.

## 2. Reconnaissance

Les premiers contrôles ont permis d'identifier les ports 22 (SSH) et 80 (HTTP) ouverts.

L'exploration HTTP a révélé plusieurs indices :

- `GET /health` renvoie un JSON indiquant que le service est opérationnel.
- `POST /session` crée une session de jeu.
- Une requête `OPTIONS /session` renvoie `405 Method Not Allowed` avec `Allow: POST`, ce qui indique que la route accepte la méthode POST.
- L'en-tête `Server: Kestrel` et Wappalyzer suggèrent une application ASP.NET Core.

Les réponses `404` obtenues sur d'autres chemins ne signifiaient pas que l'application était dépourvue de fonctionnalités intéressantes. L'examen des méthodes HTTP et l'analyse du client ont fourni des pistes plus utiles.

### Note sur les versions

Le fichier `GrandLarcenyAuto.runtimeconfig.json` mentionne le runtime .NET `8.0.29`. La version seule ne prouve pas qu'une vulnérabilité connue est exploitable. Une vérification de vulnérabilité doit tenir compte du composant précis, de la version affectée et des conditions d'exploitation. Dans ce laboratoire, l'analyse du protocole s'est révélée plus directement pertinente.

## 3. Analyse du client avec ILSpy

Après extraction de l'archive du jeu, l'assembly `GrandLarcenyAuto.dll` a été ouvert dans ILSpy.

La classe `PoPClient` a notamment révélé trois endpoints :

| Endpoint | Méthode | Rôle observé |
|---|---|---|
| `/session` | `POST` | Crée une session et renvoie les paramètres initiaux. |
| `/checkpoint` | `POST` | Soumet une étape du braquage. |
| `/claim` | `POST` | Réclame le résultat final. |

Le client contenait également une clé HMAC codée en dur :

```csharp
private static readonly byte[] SignKey =
    Encoding.UTF8.GetBytes("gla2_crew_sign_v1_2f9b6c8ad14e");
```

Cette découverte est importante : une clé secrète intégrée dans un client distribué peut être récupérée par une personne qui possède l'application. Elle ne doit donc pas être considérée comme un secret fiable côté serveur.

### La méthode `DeriveStaffRole()`

L'assembly contenait une méthode qui construisait une chaîne à partir de l'ordre des checkpoints, puis calculait son SHA-1 :

```csharp
string s = "heat5_stash" + StashOrder[0]
    + "_stash" + StashOrder[1]
    + "_stash" + StashOrder[2]
    + "_vault";
```

Cette méthode constituait un indice sur le mécanisme de rôle attendu. Son existence ne suffisait toutefois pas, à elle seule, à démontrer comment le backend validait ce rôle.

## 4. Reconstitution du protocole

Une requête `POST /session` renvoyait un identifiant de session, un token et un ordre de checkpoints, par exemple :

```json
{
  "session_id": "<session_id>",
  "stash_order": [1, 0, 2],
  "token": "<token>"
}
```

L'ordre renvoyé par le serveur déterminait la séquence à respecter. Pour cet exemple, la progression observée était :

```text
heat5
  |
stash1
  |
stash0
  |
stash2
  |
vault
```

Chaque checkpoint devait être signé avec le token courant. Lorsqu'une étape était acceptée, le serveur renvoyait un nouveau token. Il fallait utiliser ce nouveau token pour signer la requête suivante.

### Signature HMAC

Le code client construisait le message signé selon le format :

```text
session_id|step|token
```

La signature était calculée comme suit :

```text
HMAC-SHA256(SignKey, session_id + "|" + step + "|" + token)
```

Exemple de calcul en Python :

```python
import hashlib
import hmac

key = b"gla2_crew_sign_v1_2f9b6c8ad14e"
message = f"{session_id}|{step}|{token}".encode()

signature = hmac.new(
    key,
    message,
    hashlib.sha256
).hexdigest()
```

La clé, le message et la signature sont trois éléments différents. Envoyer la clé à la place de la signature ne produit pas une requête valide.

La progression complète a été acceptée par le serveur, jusqu'au checkpoint `vault`.

## 5. Première réclamation : rôle `player`

Après les checkpoints, une requête `POST /claim` a été envoyée avec le rôle `player`. Le serveur a renvoyé une réponse indiquant un accès civil et un coffre-fort leurre.

Cela a permis de séparer deux mécanismes :

- la validation de la progression du braquage ;
- l'autorisation associée à la réclamation finale.

Avoir terminé les checkpoints ne garantissait donc pas, à lui seul, l'accès au rôle recherché.

## 6. Hypothèse et test de manipulation du rôle

En poursuivant l'analyse de `PoPClient`, j'ai remarqué que le message signé pour la réclamation était construit à partir de :

```text
session_id|claim|token
```

Le paramètre `role` envoyé dans le corps JSON n'apparaissait pas dans ce message signé.

J'ai alors formulé l'hypothèse suivante :

> Si le serveur accepte le paramètre `role` fourni par le client sans le lier à la signature ni vérifier indépendamment les autorisations, il pourrait être possible de modifier ce paramètre sans invalider la signature.

Pour l'ordre de checkpoints `[1, 0, 2]`, la chaîne construite à partir du code client était :

```text
heat5_stash1_stash0_stash2_vault
```

Son SHA-1 a été calculé localement :

```python
import hashlib

sequence = "heat5_stash1_stash0_stash2_vault"
print(hashlib.sha1(sequence.encode()).hexdigest())
```

La requête de réclamation a ensuite été retestée en modifiant uniquement la valeur de `role`, tout en conservant la signature calculée sur `session_id|claim|token`.

Le serveur a renvoyé une réponse différente de celle obtenue avec `role: player`. Cette différence a confirmé que le paramètre influençait le traitement de la réclamation. Elle ne suffit cependant pas, isolément, à prouver que le véritable coffre-fort est accessible : il faut interpréter la réponse dans le contexte des objectifs et des conditions de réussite du laboratoire.

## 7. Analyse de sécurité

Les observations mettent en évidence plusieurs risques de conception.

### Secret intégré au client

Une clé HMAC embarquée dans une application distribuée peut être extraite et réutilisée. La signature ne protège donc pas le protocole contre un utilisateur qui peut analyser le client et récupérer cette clé.

### Paramètre sensible non signé

Le champ `role` n'était pas inclus dans le message HMAC construit par le client. Un paramètre de sécurité qui n'est pas couvert par l'intégrité cryptographique peut être modifié en transit, selon la manière dont le serveur traite la requête.

### Autorisation à vérifier côté serveur

Le serveur doit déterminer les permissions à partir de l'état de session et de règles de confiance côté serveur. Il ne doit pas accorder un privilège simplement parce que le client déclare un rôle ou fournit une valeur calculée localement.

### Remédiations recommandées

- Garder les clés secrètes exclusivement côté serveur.
- Calculer et valider les rôles côté serveur à partir de l'état de session.
- Vérifier explicitement les autorisations pour chaque action sensible.
- Si une signature de requête est utilisée, authentifier une représentation canonique de tous les paramètres qui influencent la décision de sécurité.
- Faire expirer et renouveler les tokens selon une politique définie, et empêcher leur réutilisation lorsque cela est nécessaire.
- Journaliser les échecs de validation et les tentatives d'accès non autorisées.

## 8. Compétences travaillées

- Analyse d'un assembly .NET avec ILSpy.
- Repérage des endpoints et reconstruction d'un protocole HTTP.
- Compréhension pratique de HMAC-SHA256.
- Gestion d'une séquence de checkpoints et de tokens renouvelés.
- Lecture du code pour identifier des hypothèses de sécurité.
- Test d'une hypothèse de contrôle d'accès à partir du comportement observable du serveur.
- Distinction entre un indice, une hypothèse et une vulnérabilité effectivement démontrée.

## 9. Conclusion

Cette room m'a permis de combiner reverse engineering et analyse de sécurité applicative. Le point décisif n'a pas été de lancer un scanner supplémentaire, mais de comprendre le fonctionnement du client, de reconstituer les échanges avec le backend et de comparer les données signées aux paramètres utilisés lors de la décision d'autorisation.

La leçon principale est qu'une signature cryptographique ne garantit pas une autorisation correcte si le protocole laisse des paramètres sensibles hors du message authentifié ou si le serveur fait confiance à des données contrôlées par le client.

L'analyse rappelle également qu'il faut distinguer le comportement observé de la conclusion finale : une réponse différente est un indice utile, mais elle doit être confrontée aux conditions de réussite du laboratoire avant de déclarer l'objectif entièrement atteint.

---

*Rapport rédigé à partir de l'analyse personnelle du laboratoire TryHackMe GrandLarcenyAuto II. Les valeurs de session, tokens et signatures temporaires ne sont pas incluses afin de garder le document réutilisable et de ne pas exposer de données de session.*
'''

output_path = "README.md"
pypandoc.convert_text(
    content,
    "md",
    format="md",
    outputfile=output_path,
    extra_args=["--standalone"]
)

print(f"README créé : {output_path}")
