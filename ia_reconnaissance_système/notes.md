# AI Reconnaissance – Services, ports et énumération

## 1. Objectif

Une infrastructure IA de production ne se limite pas à un serveur. Elle peut comprendre des serveurs d'inférence, des plateformes de suivi des expériences, des bases vectorielles, des registres de modèles et des services de stockage ou de surveillance.

La reconnaissance IA consiste à :

- Découvrir les services accessibles sur un réseau.
- Identifier les technologies susceptibles de se trouver derrière les ports ouverts.
- Examiner les endpoints et les réponses HTTP.
- Déterminer quelles informations sont exposées.
- Documenter les résultats et les risques potentiels.

**Attention :** un port ouvert ne confirme pas à lui seul l'identité d'un service ni l'existence d'une vulnérabilité. Il faut croiser plusieurs indices.

## 2. Les principales catégories de services IA

### 2.1 Serveurs d'inférence

Ces services chargent des modèles et exposent des API permettant d'obtenir des prédictions ou des réponses générées par un modèle.

| Composant | Ports courants | Endpoints à examiner |
|---|---|---|
| NVIDIA Triton Inference Server | 8000, 8001, 8002 | `/v2/health/ready`, `/v2/models` |
| TensorFlow Serving | 8500, 8501 | `/v1/models/<nom>` |
| TorchServe | 8080, 8081, 8082 | `/ping`, `/models` |
| Ollama | 11434 | `/api/tags`, `/api/show` |
| vLLM | 8000 | `/v1/models` |

HTTP/REST facilite les échanges avec les applications clientes. gRPC est notamment utilisé pour des communications structurées entre services, avec des capacités adaptées aux échanges à haut débit et au streaming.

Un même composant peut exposer plusieurs ports correspondant à différentes interfaces. Il faut donc examiner les ports et les protocoles séparément.

### 2.2 Orchestration et suivi des expériences

Ces plateformes gèrent les expériences, les pipelines d'entraînement et le déploiement des modèles.

| Composant | Ports courants | Informations à rechercher |
|---|---|---|
| MLflow Tracking Server | 5000 | Expériences, paramètres, métriques, artefacts |
| Kubeflow | 80, 443, selon le déploiement | Pipelines, interfaces et configurations accessibles |
| Ray Dashboard | 8265 | État des tâches, informations sur le cluster et jobs accessibles |
| Ray API | 8000, selon le service | Interfaces de gestion et d'exécution |

Un serveur MLflow accessible sans authentification adaptée peut exposer l'historique des expériences et des informations sur les modèles. Les risques réels dépendent toutefois de la configuration des permissions et des données accessibles.

### 2.3 Bases de données vectorielles

Les bases vectorielles stockent des embeddings et permettent de rechercher des contenus sémantiquement proches. Elles sont souvent utilisées dans les architectures RAG (*Retrieval-Augmented Generation*).

| Composant | Ports courants | Endpoints à examiner |
|---|---|---|
| Qdrant | 6333 (HTTP), 6334 (gRPC) | `/collections` |
| Weaviate | 8080 | `/v1/schema`, `/v1/meta` |
| Milvus | 19530 | Service gRPC |
| Chroma | 8000, selon la configuration | API dépendant de la version et du déploiement |

Les métadonnées peuvent révéler les noms des collections, les schémas ou des informations sur les modèles d'embeddings. Par exemple, une collection nommée `internal-hr-policies` peut suggérer la présence de documents liés aux ressources humaines.

Ce nom constitue un indice sur la nature des données, pas une preuve que leur contenu est effectivement accessible.

### 2.4 Registres de modèles et stockage

Les registres de modèles conservent les versions et les informations de cycle de vie des modèles. Les artefacts peuvent être stockés séparément.

Exemples de formats :

- `.pkl` : objets sérialisés Python.
- `.pt` : fichiers couramment associés à PyTorch.
- `.onnx` : modèles au format ONNX.
- `.mar` : archives de modèles utilisées par TorchServe.

Les métadonnées peuvent contenir les versions, les étapes de déploiement, les auteurs et les URI des artefacts.

MinIO fournit un stockage compatible avec l'API S3. Ses ports courants sont 9000 et 9001, mais leur rôle exact dépend de la configuration.

**Risque à examiner :** une exposition non autorisée peut révéler des modèles, des données ou des informations internes. La présence d'un registre ou d'un stockage accessible ne signifie pas automatiquement que les fichiers peuvent être téléchargés.

### 2.5 Infrastructure complémentaire

| Composant | Port courant | Intérêt pour la reconnaissance |
|---|---|---|
| Jupyter Notebook | 8888 | Interface interactive, noyaux et fichiers accessibles |
| Prometheus metrics | 8002 sur Triton, 8082 sur TorchServe | Métriques, noms de modèles et informations opérationnelles |

Un notebook exposé sans protection adaptée peut présenter un risque majeur, car une interface interactive peut parfois permettre l'exécution de code. Il faut vérifier les contrôles d'accès sans tenter d'exécuter des actions destructrices.

Les endpoints de métriques peuvent divulguer des informations sur les modèles, les ressources utilisées et les performances. Ils peuvent ainsi aider à cartographier une infrastructure sans interroger directement les API d'inférence.

## 3. Référence des ports

Cette table reprend les ports cités dans le cours. Ils correspondent à des configurations courantes et ne sont pas des signatures universelles.

| Port | Service ou composant possible | Protocole courant |
|---:|---|---|
| 5000 | MLflow | HTTP |
| 6333 | Qdrant | HTTP |
| 6334 | Qdrant | gRPC |
| 8000 | Triton HTTP, vLLM, Ray ou Chroma selon le déploiement | HTTP |
| 8001 | Triton gRPC | gRPC |
| 8002 | Métriques Triton | HTTP |
| 8080 | TorchServe ou Weaviate selon le déploiement | HTTP |
| 8081 | API de gestion TorchServe | HTTP |
| 8082 | Métriques TorchServe | HTTP |
| 8265 | Ray Dashboard | HTTP |
| 8500 | TensorFlow Serving | gRPC |
| 8501 | TensorFlow Serving | HTTP |
| 8888 | Jupyter Notebook | HTTP |
| 9000 | MinIO, souvent endpoint de stockage | HTTP/S3 compatible |
| 9001 | Console MinIO dans les configurations courantes | HTTP |
| 11434 | Ollama | HTTP |
| 19530 | Milvus | gRPC |

D'autres ports peuvent être utilisés, notamment lorsque les services sont placés derrière un reverse proxy, un ingress Kubernetes ou une configuration personnalisée.

## 4. Exercice pratique : reconnaissance du réseau Cyphira

### Contexte

Cyphira est une entreprise fintech dont le sous-réseau interne de laboratoire est :

`10.10.45.0/24`

L'objectif est d'identifier les composants IA accessibles sur ce réseau et de distinguer les services IA des services traditionnels.

Effectuer ces scans uniquement dans le laboratoire autorisé.

### Étape 1 : rechercher les ports associés à l'IA

```bash
nmap -p 5000,6333,6334,8000,8001,8002,8888,9000,9001 -sV 10.10.45.0/24
```

**Explication des options :**

- `nmap` : lance la reconnaissance réseau.
- `-p` : sélectionne les ports à examiner.
- `-sV` : tente d'identifier les services et leurs versions à partir des réponses observées.
- `10.10.45.0/24` : désigne le sous-réseau cible, soit les adresses de `10.10.45.0` à `10.10.45.255`.

**Ce que j'envoie :** des sondes réseau vers les ports sélectionnés, puis des requêtes de détection de service lorsque cela est possible.

**Ce que je cherche :** les hôtes accessibles, les ports ouverts et les indices permettant d'identifier les logiciels exposés.

**Limites :**

- `-sV` ne garantit pas une identification exacte.
- Un port filtré ou inaccessible ne prouve pas l'absence du service.
- Les services personnalisés peuvent utiliser des ports inhabituels.
- Certains services peuvent partager un même port selon l'adresse, le proxy ou le déploiement.

### Étape 2 : rechercher les services traditionnels

```bash
nmap -p 22,80,443,5432 -sV 10.10.45.0/24
```

Cette commande examine notamment SSH, HTTP, HTTPS et le port généralement associé à PostgreSQL.

Comparer les résultats avec ceux de la première étape :

- Quels hôtes exposent des ports associés à des composants IA ?
- Quels hôtes semblent uniquement proposer des services traditionnels parmi les ports testés ?
- Quels hôtes exposent les deux catégories ?
- Certains ports sont-ils associés à des services inattendus ?

**Important :** un hôte qui ne présente aucun port IA ouvert dans ce scan n'est pas nécessairement dépourvu d'infrastructure IA. Le service peut écouter sur un autre port ou être accessible uniquement par une interface intermédiaire.

## 5. Tableau de collecte des résultats

Compléter ce tableau à partir des résultats réels de Nmap.

| Adresse IP | Port | État | Service détecté par Nmap | Composant IA supposé | Niveau de confiance |
|---|---:|---|---|---|---|
| À compléter | À compléter | À compléter | À compléter | À identifier | Faible / moyen / élevé |
| À compléter | À compléter | À compléter | À compléter | À identifier | Faible / moyen / élevé |
| À compléter | À compléter | À compléter | À compléter | À identifier | Faible / moyen / élevé |

### Comment évaluer la confiance ?

- **Faible :** le port correspond à un service IA possible, mais aucun autre indice ne confirme l'hypothèse.
- **Moyenne :** la bannière ou la réponse du service correspond à la technologie supposée.
- **Élevée :** plusieurs indices cohérents, comme la signature du service et la réponse d'un endpoint caractéristique, confirment l'identification.

Le niveau de confiance porte sur l'identification du composant, pas sur sa vulnérabilité.

## 6. Étape suivante : confirmer le fingerprinting

Une fois un service identifié comme candidat, examiner ses réponses HTTP lorsque le protocole et les autorisations le permettent.

Exemple pour un service HTTP de laboratoire :

```bash
curl -i http://ADRESSE_IP:PORT/
```

Remplacer `ADRESSE_IP` et `PORT` par les valeurs réellement observées.

L'option `-i` affiche les en-têtes HTTP avec le corps de la réponse.

Observer :

- Le code de statut HTTP.
- Les en-têtes `Server` ou autres en-têtes révélateurs.
- Le format de la réponse.
- Les messages d'erreur.
- Les redirections éventuelles.

Un code `200` indique qu'une requête a été traitée avec succès au niveau HTTP, mais ne prouve pas que toutes les données sont accessibles. Un code `401` ou `403` peut indiquer une restriction d'accès. Un code `404` ne suffit pas à conclure que le service n'existe pas.

Les endpoints propres à chaque technologie seront vérifiés après identification du service et selon le périmètre autorisé.

## 7. Exemple de chaîne de découverte

Une reconnaissance structurée peut suivre ce chemin :

1. Nmap détecte le port `5000` ouvert sur un hôte.
2. La détection de service et une réponse HTTP suggèrent MLflow.
3. Une requête vers un endpoint documenté permet de confirmer la technologie.
4. Les réponses indiquent quelles métadonnées sont accessibles.
5. L'analyse des contrôles d'accès permet d'évaluer l'exposition réelle.
6. Les observations et les preuves sont documentées pour l'équipe sécurité.

Cette séquence illustre une méthode de travail. Elle ne représente pas les résultats de l'exercice Cyphira tant que les scans n'ont pas été exécutés.

## 8. Étude de cas : exposition et chaîne de confiance

Le cours cite des recherches sur l'exposition de services IA et les attaques visant les infrastructures d'entraînement ML.

Un scénario représentatif est le suivant :

1. Un notebook expose des informations de configuration ou des identifiants.
2. Ces identifiants permettent d'accéder à un serveur de suivi des expériences.
3. Le serveur révèle des métadonnées et des URI d'artefacts.
4. Ces URI désignent un stockage contenant des modèles ou d'autres fichiers.
5. Des contrôles d'accès insuffisants entre ces composants permettent d'étendre l'exposition initiale.

Le risque provient alors de la chaîne de confiance entre les services, et pas uniquement du premier port découvert.

Les requêtes Shodan citées dans le cours illustrent comment rechercher des services exposés à l'échelle d'Internet. Toute recherche de ce type doit respecter les autorisations applicables et ne doit pas être confondue avec un scan du réseau privé du laboratoire.

## 9. Défense et surveillance

Les équipes de sécurité peuvent rechercher :

- Des balayages de nombreux ports sur plusieurs hôtes.
- Des requêtes répétées vers des endpoints de métadonnées.
- Des tentatives d'accès aux interfaces de gestion.
- Des réponses d'erreur inhabituelles ou répétitives.
- Des accès inattendus aux notebooks, registres ou bases vectorielles.

Ces événements doivent être corrélés au contexte. Un scan autorisé réalisé par une équipe interne peut produire des signes similaires à ceux d'une reconnaissance malveillante.

Les mesures de réduction des risques incluent la restriction des interfaces de gestion, l'authentification, le cloisonnement réseau, la limitation des métadonnées exposées et la surveillance des accès.

## 10. À retenir

- Une infrastructure IA regroupe plusieurs services spécialisés, pas seulement un endpoint d'inférence.
- Les ports sont des indices utiles, mais leur valeur dépend de la configuration réelle.
- Nmap permet la découverte et le fingerprinting initial.
- curl permet d'examiner les réponses HTTP et les endpoints.
- Les métadonnées, les métriques et les interfaces de gestion peuvent révéler l'architecture interne.
- L'exposition d'un service ne prouve pas à elle seule l'existence d'une vulnérabilité.
- Les résultats doivent être vérifiables, reproductibles et distingués des hypothèses.

**Principe de travail :** observer, formuler une hypothèse, la vérifier, puis documenter ce que les preuves permettent réellement d'affirmer.

