# AI Reconnaissance : reconnaissance des services d'IA

> TryHackMe | Cybersécurité offensive | Reconnaissance et énumération

## Présentation

Ce dossier regroupe mes notes d'apprentissage sur la reconnaissance des services d'intelligence artificielle (IA) exposés sur un réseau.

L'objectif est de comprendre comment identifier les services IA, analyser leurs interfaces, extraire les métadonnées accessibles et cartographier leur surface d'attaque.

Un service IA ne se limite pas à un modèle de machine learning. Il peut aussi dépendre d'API, de bases de données vectorielles, de registres de modèles, de systèmes de stockage et d'outils de supervision. Chacun de ces composants peut exposer des informations utiles à un attaquant lorsqu'il est mal configuré.

**Principe : comprendre le service avant de chercher à comprendre ses vulnérabilités.**

## Objectifs d'apprentissage

- Identifier les technologies et les services IA exposés.
- Comprendre le rôle des ports et des endpoints courants.
- Effectuer le fingerprinting d'un service à partir de ses réponses HTTP, de ses en-têtes et de ses signatures JSON.
- Énumérer les API et les métadonnées accessibles.
- Comprendre les risques liés aux registres de modèles, aux artefacts, aux bases vectorielles et aux métriques.
- Cartographier la surface d'attaque d'une infrastructure IA.
- Reconnaître les risques liés à la chaîne d'approvisionnement des modèles et des dépendances.
- Distinguer la reconnaissance passive, le scan actif, le fingerprinting et l'extraction de métadonnées.

## Organisation du dossier

| Fichier | Contenu |
|---|---|
| `goals.md` | Objectifs du lab, contexte et compétences à développer. |
| `notes.md` | Notes techniques : composants IA, ports, énumération, surface d'attaque et méthodologie de reconnaissance. |
| `fingerprinting_ia.md` | Techniques de fingerprinting des services IA à partir des réponses réseau et HTTP. |
| `api-endpoints-llm.txt` | Référence des endpoints associés aux services IA et aux LLM. |

## Composants IA à connaître

Une infrastructure IA peut contenir plusieurs types de services :

| Composant | Exemples | Risques à examiner |
|---|---|---|
| Serveurs d'inférence | NVIDIA Triton, TensorFlow Serving, TorchServe, vLLM | Modèles exposés, API mal protégées, informations de déploiement. |
| Registres et plateformes ML | MLflow, Kubeflow | Expériences, versions, artefacts et métadonnées accessibles. |
| Serveurs de modèles locaux | Ollama | API exposées et accès non autorisés aux modèles. |
| Bases de données vectorielles | Qdrant, Weaviate, Milvus, Chroma | Collections, schémas, métadonnées et données accessibles. |
| Stockage d'artefacts | MinIO | Modèles, fichiers et objets mal protégés. |
| Outils de supervision | Prometheus, endpoints `/metrics` | Informations sur les performances, les modèles et l'infrastructure. |
| Interfaces de développement | Jupyter, FastAPI, documentation OpenAPI | Interfaces d'administration ou de développement exposées. |

Les ports et endpoints mentionnés dans les notes sont des **points de départ**, pas des preuves suffisantes pour identifier un service. Les configurations peuvent varier selon les versions, les déploiements et les ports personnalisés.

## Méthodologie de reconnaissance

Le travail est organisé en cinq phases complémentaires.

### 1. Reconnaissance passive

Collecter les informations disponibles sans interagir directement avec la cible de manière intrusive.

Exemples :
- Rechercher des sous-domaines et des informations DNS publiques.
- Examiner les dépôts de code et les configurations publiquement accessibles.
- Identifier les technologies mentionnées dans les informations disponibles.

### 2. Scan actif

Vérifier les hôtes, les ports et les services accessibles dans le périmètre autorisé.

Outils possibles :
- `Nmap` pour identifier les ports ouverts et les services.
- `curl` pour envoyer des requêtes HTTP ciblées.
- Wireshark pour observer les échanges réseau.

Un port ouvert ne prouve pas à lui seul qu'un service IA est présent. Il faut examiner les réponses obtenues.

### 3. Fingerprinting des API

Analyser les réponses afin d'identifier la technologie ou le framework utilisé.

Points d'observation :
- En-têtes HTTP.
- Codes de statut.
- Structure des réponses JSON.
- Messages d'erreur.
- Endpoints connus.
- Documentation API exposée.

Une signature isolée peut être trompeuse. Plusieurs indices concordants permettent une identification plus fiable.

### 4. Extraction de métadonnées

Examiner les informations accessibles via les interfaces et endpoints identifiés.

Exemples :
- Expériences et modèles enregistrés dans MLflow.
- Informations de santé et métriques d'un serveur d'inférence.
- Collections et schémas d'une base vectorielle.
- Versions de modèles et métadonnées de déploiement.

Exemple : une requête réussie vers `/metrics` sur un service utilisant le port habituel de NVIDIA Triton peut permettre de collecter des métriques de déploiement.

Une réponse HTTP `200 OK` signifie que la requête a été traitée avec succès au niveau HTTP. Elle ne garantit ni l'exhaustivité des données ni l'identification certaine du service.

### 5. Analyse de la surface d'attaque et de la chaîne d'approvisionnement

Relier les informations collectées afin de comprendre les composants exposés et leurs dépendances.

Points à examiner :
- Interfaces d'administration accessibles.
- API sans authentification suffisante.
- Accès excessifs aux modèles ou aux artefacts.
- Dépendances et images de conteneurs vulnérables.
- Secrets présents dans les configurations ou les dépôts.
- Exposition des métriques et des informations internes.
- Séparation entre les environnements de développement et de production.

L'objectif est de construire une représentation cohérente de la surface d'attaque, plutôt que d'accumuler des ports ouverts dans un fichier et d'espérer que la magie opère.

## Outils de référence

| Outil | Utilisation |
|---|---|
| Nmap | Découverte des ports et identification initiale des services. |
| curl | Analyse des réponses HTTP et exploration contrôlée des endpoints. |
| Burp Suite | Interception et modification des requêtes HTTP dans les tests web. |
| Wireshark | Observation et analyse des échanges réseau. |
| Navigateur | Inspection de la documentation et des interfaces web exposées. |

Le choix de l'outil dépend de la question à résoudre. Il est préférable de maîtriser quelques outils et de comprendre leurs limites plutôt que d'en utiliser des dizaines sans savoir interpréter leurs résultats.

## Points de vigilance

- Effectuer les scans uniquement sur des systèmes autorisés.
- Respecter le périmètre et les règles du lab TryHackMe.
- Ne pas confondre un port courant avec une identification certaine.
- Ne pas considérer un endpoint accessible comme une vulnérabilité automatiquement exploitable.
- Ne pas réutiliser des secrets découverts pendant un exercice.
- Vérifier les versions, la documentation et les avis de sécurité avant de conclure qu'un composant est vulnérable.
- Conserver les résultats, les hypothèses et les limites de chaque observation.

## Conclusion

La reconnaissance des services IA consiste à identifier les composants exposés, comprendre leurs interfaces et déterminer quelles informations sont accessibles.

Le point essentiel n'est pas de connaître par cœur chaque port ou endpoint. C'est de savoir **quoi observer, pourquoi l'observer et comment interpréter le résultat**.

La reconnaissance produit des hypothèses. Les preuves collectées permettent ensuite de les confirmer ou de les rejeter.

---

*Notes personnelles réalisées dans le cadre de mon apprentissage de la cybersécurité offensive avec TryHackMe.*
