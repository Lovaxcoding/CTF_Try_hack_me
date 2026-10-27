1. Identifier les composants essentiels d’un système d’IA en production et les flux de données entre ces composants.

2. Identifier OWASP LLM Top 10 (2025) et MITRE ATLAS comme les principaux référentiels de classification des menaces liées à l’intelligence artificielle.

3. Expliquer cinq catégories de menaces au niveau du système : le traitement inapproprié des sorties, l’excès d’autonomie, la divulgation du prompt système, la consommation sans limites et la divulgation d’informations sensibles.

4. Appliquer des modèles de conception sécurisés aux architectures des systèmes d’IA, notamment la défense en profondeur, le principe du moindre privilège et la surveillance des activités.

# Architecture et sécurité des systèmes d'IA

## 1. Des applications traditionnelles aux applications augmentées par l'IA

### Architecture traditionnelle

Dans une application web classique, les données suivent généralement ce parcours :

`Interface utilisateur → API → Base de données → API → Interface utilisateur`

Le traitement repose principalement sur du code déterministe. Les contrôles de sécurité sont placés aux points d'entrée, dans les API, au niveau des bases de données et dans les sorties.

### Architecture augmentée par l'IA

L'intégration d'un modèle de langage (LLM) introduit de nouveaux composants et de nouveaux flux de données qui ne sont pas nécessairement couverts par les contrôles existants.

| Composant | Application traditionnelle | Application augmentée par l'IA |
|---|---|---|
| Entrée utilisateur | Formulaires structurés, paramètres API | Langage naturel libre |
| Traitement | Code déterministe | Inférence probabiliste du modèle |
| Accès aux données | Requêtes directes à la base de données | Récupération médiée par le modèle, notamment via RAG |
| Sortie | Réponses générées par des templates | Texte généré par le modèle |
| Dépendances | Bibliothèques et frameworks | Bibliothèques, modèles préentraînés et embeddings |

**Point clé :** le passage des entrées structurées au langage naturel rend la validation plus complexe. Une entrée textuelle peut contenir des instructions, des données non fiables ou des tentatives de prompt injection.

La validation classique reste nécessaire, mais elle ne suffit pas à sécuriser un système d'IA.

---

## 2. Architecture du système TryAssist

TryAssist, présenté dans cette room de TryHackMe, comprend neuf composants principaux.

| Composant | Fonction |
|---|---|
| **User Interface** | Interface de chat intégrée à la plateforme de revue de code |
| **API Gateway** | Authentification, limitation du débit et routage des requêtes |
| **Orchestration Layer** | Gestion de l'état des conversations et coordination des composants |
| **Prompt Construction** | Assemblage des instructions système, de la requête utilisateur et du contexte récupéré |
| **LLM** | Modèle de langage qui génère les réponses |
| **Tool Layer** | Exécution des fonctions accessibles au modèle : requêtes en base, recherche documentaire, vérification CI/CD |
| **Output Processing** | Formatage des réponses, filtrage du contenu et limitation de la longueur |
| **Logging and Monitoring** | Conservation des conversations, statistiques d'utilisation et journal d'audit |
| **Vector Store** | Stockage des représentations vectorielles de documents pour la génération augmentée par récupération (RAG) |

### Notions importantes

- **LLM (Large Language Model)** : modèle capable de traiter et de générer du langage naturel.
- **RAG (Retrieval-Augmented Generation)** : technique qui récupère des informations dans une source documentaire pour enrichir le contexte fourni au modèle.
- **Embedding** : représentation numérique d'un contenu, utilisée notamment pour rechercher des documents sémantiquement proches.
- **Orchestration** : coordination des différentes étapes du traitement d'une requête.
- **Tool calling** : mécanisme par lequel le modèle demande l'exécution d'une fonction mise à sa disposition.

**Surface d'attaque :** chaque composant peut introduire des risques différents. Par exemple, une authentification insuffisante au niveau de l'API, des permissions excessives pour les outils ou des documents malveillants dans le contexte RAG.

---

## 3. Frontières de confiance (Trust Boundaries)

Une **frontière de confiance** est un point où des données passent d'un contexte de sécurité à un autre.

Chaque frontière constitue une surface d'attaque potentielle et doit être protégée par des contrôles adaptés.

| Frontière | Données qui la traversent | Risque à examiner |
|---|---|---|
| **User-to-System** | Texte fourni par l'utilisateur | Entrées malveillantes, prompt injection |
| **System-to-LLM** | Prompt assemblé : instructions, requête et contexte | Confusion entre instructions et données non fiables |
| **LLM-to-Tools** | Demandes d'exécution d'outils | Actions non autorisées, permissions excessives |
| **System-to-External-Data** | Documents récupérés depuis le vector store ou des sources externes | Injection indirecte, contenu non fiable |
| **System-to-User** | Réponse générée par le modèle | Divulgation d'informations, contenu dangereux ou sortie mal traitée |

### Principe de sécurité

Il ne suffit pas de sécuriser l'entrée utilisateur. Il faut examiner l'ensemble du parcours des données, depuis leur réception jusqu'à la réponse finale et aux actions exécutées par les outils.

---

## 4. Flux de données : exemple d'une requête

**Question du développeur :** « Cette pull request gère-t-elle correctement l'authentification ? »

Voici le parcours de la requête dans TryAssist.

1. **Interface utilisateur :** le développeur soumet sa question.
2. **API Gateway :** le système authentifie la requête et applique des limites de débit.
3. **Orchestration Layer :** le système récupère l'historique de conversation et détermine le traitement à effectuer.
4. **Prompt Construction :** le système assemble les instructions système, la question de l'utilisateur et la documentation pertinente récupérée dans le vector store.
5. **LLM :** le modèle analyse le contexte et génère une réponse.
6. **Tool Layer :** le modèle peut demander l'exécution d'un outil, par exemple pour récupérer le dernier état du pipeline CI d'une pull request.
7. **Exécution de l'outil :** le système vérifie les autorisations applicables, exécute l'action autorisée et renvoie le résultat au modèle.
8. **LLM :** le modèle produit une réponse finale en tenant compte du résultat.
9. **Output Processing :** le système filtre et formate la réponse.
10. **Logging and Monitoring :** l'échange est enregistré selon les règles de journalisation, puis la réponse est transmise au développeur.

**Attention :** la séquence peut varier selon l'implémentation. Une requête n'entraîne pas nécessairement l'utilisation d'un outil, et certaines étapes peuvent être répétées.

### Points de contrôle à vérifier

- L'utilisateur est-il correctement authentifié ?
- Les requêtes sont-elles soumises à des limites d'utilisation ?
- Le contenu récupéré est-il traité comme une donnée non fiable ?
- Les outils vérifient-ils les permissions indépendamment du modèle ?
- Les sorties sont-elles validées avant d'être utilisées par d'autres composants ?
- Les journaux protègent-ils les données sensibles ?

---

## 5. Principaux enseignements de sécurité

### Défense en profondeur

Mettre en place plusieurs couches de protection indépendantes. Aucun filtre unique ne doit être considéré comme suffisant.

### Principe du moindre privilège

Limiter les droits du modèle et de ses outils aux actions strictement nécessaires. Une demande formulée par le LLM ne constitue pas une autorisation.

### Validation des sorties

Traiter les réponses du modèle comme des données potentiellement non fiables, notamment lorsqu'elles sont transmises à une API, à une requête SQL, à un interpréteur ou à une interface web.

### Protection des données

Contrôler l'accès aux documents récupérés, éviter d'inclure des secrets inutiles dans les prompts et limiter les données sensibles présentes dans les journaux.

### Surveillance

Journaliser les événements pertinents et surveiller les comportements inhabituels : appels d'outils inattendus, consommation excessive, tentatives répétées d'extraction ou accès non autorisés.

---

## 6. Checklist rapide pour un audit d'architecture IA

- [ ] Identifier les neuf composants du système.
- [ ] Tracer le parcours d'une requête de bout en bout.
- [ ] Repérer les cinq frontières de confiance.
- [ ] Identifier les données sensibles présentes dans les prompts et les documents récupérés.
- [ ] Vérifier les permissions de chaque outil accessible au LLM.
- [ ] Contrôler la validation des entrées et des sorties.
- [ ] Examiner les mécanismes de limitation de débit et de consommation.
- [ ] Vérifier la journalisation et la surveillance.
- [ ] Identifier les composants qui font confiance aux réponses du modèle sans validation indépendante.

## Résumé

Une application augmentée par l'IA ne se limite pas à une interface de chat connectée à un LLM. Elle repose sur plusieurs composants qui échangent des instructions, des données, des documents et parfois des demandes d'action.

L'analyse de sécurité doit donc porter sur **les composants, les flux de données, les frontières de confiance et les autorisations**.

Le principe essentiel : ne jamais considérer une entrée utilisateur, un document récupéré ou une sortie de modèle comme fiable par défaut.
