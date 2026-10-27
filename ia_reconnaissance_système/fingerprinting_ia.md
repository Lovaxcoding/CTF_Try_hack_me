# Fingerprinting des services IA

## 1. Objectif

Le **fingerprinting** consiste à identifier un service, son framework ou sa technologie à partir des indices qu'il expose.

Un port ouvert ne suffit pas pour identifier précisément un service. Pour renforcer l'identification, on examine plusieurs éléments :

- Les en-têtes HTTP.
- La structure des réponses JSON.
- Les messages d'erreur.
- Les conventions de nommage des endpoints.
- Les protocoles utilisés, notamment gRPC.
- Les caractéristiques du trafic TLS, lorsqu'elles sont observables.

L'objectif est de formuler une hypothèse, puis de la confirmer avec plusieurs indices indépendants.

## 2. Fingerprinting des en-têtes HTTP

Les en-têtes HTTP peuvent révéler des informations sur le serveur qui traite une requête.

| Framework ou technologie | Indice recherché | Interprétation |
|---|---|---|
| TorchServe | `Server: TorchServe/...` | Indice direct sur TorchServe si l'en-tête est authentique. |
| NVIDIA Triton | `NV-Status` dans certaines réponses | Indice pouvant aider à identifier Triton. |
| FastAPI avec Uvicorn | `server: uvicorn` | Indice d'un serveur Python utilisant Uvicorn, pas nécessairement d'une application IA. |
| API compatible OpenAI | `x-request-id` et réponses JSON caractéristiques | Indices d'une API compatible, sans identifier à eux seuls le framework sous-jacent. |

### Exemple avec curl

```bash
curl -sS -D - -o /dev/null http://ADRESSE_IP:PORT/
```

**Explication :**

- `curl` envoie une requête HTTP.
- `-sS` réduit les messages de progression tout en conservant les erreurs.
- `-D -` affiche les en-têtes de réponse dans le terminal.
- `-o /dev/null` ignore le corps de la réponse.

**À observer :** les en-têtes `Server`, `Content-Type`, les identifiants de requête et les éventuels en-têtes propres au framework.

**Limites :** les en-têtes peuvent être masqués, modifiés ou ajoutés par un reverse proxy. Un en-tête `server: uvicorn` identifie une technologie de serveur, pas la nature exacte de l'application.

### Cas particulier de Triton

Le cours indique que Triton peut fournir des informations sur les métriques matérielles lorsque la requête contient l'en-tête :

```http
endpoint-load-metrics-format: text
```

Cet indice peut être utile dans un environnement autorisé. Il ne faut cependant pas considérer qu'un comportement particulier est absolument unique à un framework sans l'avoir confirmé par d'autres éléments.

## 3. Fingerprinting des réponses JSON

Les réponses JSON peuvent révéler la structure d'une API et parfois identifier le framework utilisé.

| Service | Signature donnée dans le cours | Ce qu'elle peut indiquer |
|---|---|---|
| TensorFlow Serving | `model_version_status`, `version`, `state` | État des versions d'un modèle TensorFlow Serving. |
| NVIDIA Triton | `name`, `versions`, `platform` | Métadonnées d'un modèle servi par Triton. |
| API compatible OpenAI | `object: model`, `id`, `created` | Format de réponse compatible avec certaines API de modèles. |
| MLflow | Erreurs mentionnant `mlflow.server` ou `mlflow.tracking` | Présence possible de composants MLflow. |

Exemple de signature Triton, selon le cours :

```json
{
  "name": "fraud_detector",
  "versions": ["1"],
  "platform": "tensorflow_graphdef"
}
```

Exemple de réponse compatible OpenAI :

```json
{
  "object": "model",
  "id": "llama-3.1-8b",
  "created": 1700000000
}
```

Ces exemples illustrent des structures possibles. Les champs exacts peuvent varier selon la version, l'endpoint, la configuration et les adaptations du service.

### Interprétation

Une réponse contenant `"object": "model"` suggère une API utilisant un format compatible OpenAI. Elle ne permet pas de distinguer à elle seule vLLM, LiteLLM, Ollama ou une implémentation personnalisée.

Le bon réflexe est de comparer plusieurs indices : structure JSON, en-têtes HTTP, endpoint utilisé et comportement du service.

## 4. Fingerprinting par les messages d'erreur

Les messages d'erreur peuvent révéler des détails internes sur un framework, ses dépendances ou son architecture.

Exemples mentionnés dans le cours :

- **TensorFlow Serving :** une erreur de format de données peut faire référence à `tensorinfo_map`.
- **MLflow :** certaines erreurs peuvent mentionner les espaces de noms `mlflow.server` ou `mlflow.tracking`.
- **Databricks Mosaic AI :** certaines erreurs de validation de jetons peuvent contenir des références à `io.jsonwebtoken.IncorrectClaimException`.

Les erreurs détaillées peuvent révéler des chemins internes, des noms de modules ou des versions. En production, elles peuvent donc divulguer des informations utiles à un attaquant.

### Méthode d'analyse

1. Envoyer une requête valide et documentée.
2. Observer le code HTTP et le format de la réponse.
3. Si nécessaire, tester une entrée invalide mais inoffensive dans le laboratoire autorisé.
4. Comparer le message obtenu aux signatures documentées.
5. Vérifier si l'erreur révèle des détails internes inutiles à l'utilisateur.

Il n'est pas nécessaire d'envoyer des charges destructrices ou de chercher à provoquer un plantage. Une requête invalide simple suffit souvent à observer le traitement des erreurs.

**Point de vigilance :** une erreur détaillée ne prouve pas automatiquement qu'un service est vulnérable. Elle peut signaler un problème de divulgation d'informations, dont la gravité dépend du contenu révélé et du contexte.

## 5. Conventions de nommage des endpoints

Les services IA exposent souvent des chemins liés à l'inférence, aux modèles ou aux expériences.

| Endpoint ou préfixe | Service ou fonction possible |
|---|---|
| `/predict` | Prédiction, souvent dans une API personnalisée |
| `/invocations` | Endpoint courant dans certains déploiements Amazon SageMaker |
| `/infer` | Inférence, selon l'implémentation |
| `/generate` | Génération de contenu |
| `/embeddings` | Calcul ou accès à des embeddings |
| `/score` | Scoring ou évaluation |
| `/v1/models` | Liste de modèles dans certaines API compatibles OpenAI |
| `/v2/models` | Endpoint associé notamment à Triton |
| `/api/2.0/mlflow/` | API de suivi et de gestion MLflow |
| `/pipeline/apis/v1beta1/` | API associée à certaines versions de Kubeflow Pipelines |

Ces chemins sont des indices, pas des identifiants universels. Une application personnalisée peut réutiliser les mêmes noms, et les versions ou les configurations peuvent modifier les routes disponibles.

### Recherche de chemins

Lors d'un audit autorisé, une wordlist adaptée peut inclure ces chemins spécifiques aux systèmes IA. Des outils comme `ffuf` ou `feroxbuster` permettent de rechercher des routes, mais il faut limiter les requêtes et tenir compte de leur impact sur le service.

La découverte d'un endpoint ne signifie pas que son contenu est accessible sans authentification.

## 6. Fingerprinting gRPC

gRPC est un protocole de communication qui s'appuie généralement sur HTTP/2 et utilise des messages structurés, souvent définis par Protocol Buffers.

Certains services IA l'exposent en complément de HTTP :

| Service | Port courant du cours | Protocole |
|---|---:|---|
| NVIDIA Triton | 8001 | gRPC |
| TensorFlow Serving | 8500 | gRPC |

Les scanners HTTP classiques ne suffisent pas toujours à identifier un service gRPC. Il faut utiliser un client compatible avec ce protocole.

### Outil : grpcurl

Si le service est accessible et que la réflexion gRPC est activée, `grpcurl` peut permettre d'énumérer les services et de consulter leurs définitions.

Lister les services :

```bash
grpcurl -plaintext ADRESSE_IP:8001 list
```

Consulter la définition d'un service :

```bash
grpcurl -plaintext ADRESSE_IP:8001 describe inference.GRPCInferenceService
```

**Explication des options :**

- `grpcurl` : client permettant d'interroger des services gRPC.
- `-plaintext` : utilise une connexion sans TLS.
- `list` : demande la liste des services lorsque la réflexion est disponible.
- `describe` : demande la description d'un service ou d'un type.

**À observer :** les noms des services, les méthodes RPC et les structures de messages décrites.

**Limites :**

- La réflexion gRPC peut être désactivée.
- Le port peut nécessiter TLS ou une authentification.
- `-plaintext` n'est approprié que lorsque le service accepte une connexion sans TLS.
- L'absence de résultat avec `list` ne prouve pas que le serveur n'utilise pas gRPC.

Les schémas obtenus peuvent révéler les méthodes et les formats attendus par l'API. Leur accès doit rester dans le périmètre autorisé.

## 7. Fingerprinting TLS : JA3 et JA4

JA3 et JA4 sont des méthodes de fingerprinting du trafic TLS. Elles caractérisent certains éléments de la négociation TLS afin d'aider à distinguer des familles de clients ou des comportements réseau.

Dans une infrastructure IA, les communications automatisées peuvent provenir de bibliothèques Python, de clients gRPC ou de pipelines ML. Leurs signatures peuvent différer de celles des navigateurs web classiques.

Le cours mentionne une campagne dans laquelle une même signature JA4H était associée à une grande partie du trafic observé, malgré de nombreuses adresses IP sources. Une telle uniformité peut suggérer l'utilisation d'un outil automatisé partagé.

### Utilité défensive

Ces empreintes peuvent aider à :

- Regrouper des requêtes présentant des caractéristiques similaires.
- Repérer des outils automatisés.
- Corréler des activités provenant de plusieurs adresses IP.
- Compléter l'analyse des journaux HTTP et des flux réseau.

**Limites :** une empreinte TLS ne prouve pas à elle seule l'identité d'un outil ou l'intention d'un utilisateur. Elle doit être corrélée à d'autres indicateurs.

## 8. Méthodologie de fingerprinting

Pour identifier un service, suivre cette séquence :

1. **Découvrir :** relever l'hôte et le port ouvert.
2. **Observer :** récupérer les en-têtes HTTP et le corps de la réponse, lorsque le protocole est HTTP.
3. **Comparer :** rechercher des signatures connues dans les en-têtes, le JSON et les endpoints.
4. **Confirmer :** utiliser une autre caractéristique du service ou un endpoint documenté.
5. **Évaluer l'exposition :** déterminer quelles informations sont accessibles et quels contrôles d'accès sont en place.
6. **Documenter :** consigner les preuves, le niveau de confiance et les limites de l'identification.

### Modèle de prise de notes

| Élément | Résultat |
|---|---|
| Adresse IP et port | À compléter |
| Protocole | À compléter |
| En-têtes observés | À compléter |
| Structure de réponse | À compléter |
| Endpoint testé | À compléter |
| Message d'erreur éventuel | À compléter |
| Framework supposé | À compléter |
| Indices de confirmation | À compléter |
| Niveau de confiance | Faible / moyen / élevé |
| Informations exposées | À compléter |

## 9. À retenir

- Les en-têtes HTTP fournissent des indices rapides, mais peuvent être masqués ou modifiés.
- Les structures JSON aident à reconnaître les familles d'API et les frameworks.
- Les erreurs peuvent divulguer des détails internes et contribuer au fingerprinting.
- Les endpoints permettent d'orienter la recherche vers les fonctions d'inférence, de gestion ou de suivi ML.
- `grpcurl` est utile pour examiner les services gRPC lorsque leur configuration le permet.
- JA3/JA4 complètent l'analyse réseau, sans fournir une preuve d'identité absolue.
- Une identification fiable repose sur plusieurs indices concordants, pas sur une seule chaîne de caractères.

**Principe essentiel :** identifier une technologie est une étape de reconnaissance. Démontrer une vulnérabilité exige des preuves supplémentaires.

