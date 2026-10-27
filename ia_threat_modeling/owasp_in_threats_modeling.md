# OWASP Top 10 for LLM Applications (2025)

## 1. Introduction

L'**OWASP Top 10 for LLM Applications (2025)** est un référentiel qui présente les principaux risques de sécurité associés aux applications utilisant des grands modèles de langage (*Large Language Models*, ou LLM).

Publié par l'OWASP GenAI Security Project, il aide les développeurs, les auditeurs et les équipes de sécurité à identifier les risques propres aux systèmes LLM.

Contrairement à une simple liste de vulnérabilités, ce référentiel permet également d'associer les risques aux composants d'une architecture : endpoint d'inférence, pipeline RAG, base vectorielle, pipeline d'entraînement, intégrations d'outils et passerelles API.

Références :
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/)
- [OWASP Top 10 for Web Applications](https://owasp.org/Top10/2025/)

## 2. Les dix risques de sécurité

| ID | Risque | Description | Composants concernés |
|---|---|---|---|
| **LLM01** | Prompt Injection | Manipulation du comportement du modèle par des instructions malveillantes directes ou indirectes. | Endpoint LLM, pipeline RAG, documents récupérés. |
| **LLM02** | Sensitive Information Disclosure | Divulgation de données personnelles, de secrets ou d'informations confidentielles. | Endpoint LLM, données d'entraînement, configuration des prompts. |
| **LLM03** | Supply Chain | Compromission de modèles, de jeux de données, de dépendances ou d'intégrations tierces. | Pipeline d'entraînement, registre de modèles, plugins et outils. |
| **LLM04** | Data and Model Poisoning | Altération des données d'entraînement ou du modèle afin d'influencer son comportement. | Pipeline d'entraînement, registre de modèles, feature stores. |
| **LLM05** | Improper Output Handling | Utilisation de sorties du modèle sans validation ni traitement sécurisé. | Frontend, passerelle API, services consommateurs des réponses. |
| **LLM06** | Excessive Agency | Permissions, outils ou autonomie excessifs accordés au système IA. | Agent IA, intégrations d'outils, API et couche d'orchestration. |
| **LLM07** | System Prompt Leakage | Divulgation des instructions internes du modèle. | Endpoint LLM, configuration du prompt système. |
| **LLM08** | Vector and Embedding Weaknesses | Faiblesses des bases vectorielles, des embeddings et des mécanismes de récupération. | Base vectorielle, génération d'embeddings, pipeline RAG. |
| **LLM09** | Misinformation | Production d'informations fausses, trompeuses ou insuffisamment vérifiées. | Endpoint LLM, sources documentaires, interfaces utilisateur. |
| **LLM10** | Unbounded Consumption | Consommation excessive de ressources, déni de service ou exploitation financière. | Endpoint LLM, passerelle API, infrastructure d'entraînement. |

**Remarque :** cette liste correspond aux catégories de l'édition 2025. Il faut consulter le référentiel officiel pour vérifier les descriptions et les éventuelles mises à jour.

## 3. Associer les risques aux composants

L'une des compétences importantes du Threat Modeling consiste à analyser les risques dans les deux sens :

- **Risque vers composant :** déterminer quelles parties du système sont exposées à une menace donnée.
- **Composant vers risque :** identifier toutes les menaces pertinentes lorsqu'un composant est ajouté à l'architecture.

### 3.1 Endpoint d'inférence LLM

L'endpoint d'inférence reçoit les entrées et renvoie les réponses du modèle. Il constitue une interface particulièrement importante à sécuriser.

Risques associés :
- **LLM01 :** prompt injection directe.
- **LLM02 :** divulgation d'informations sensibles.
- **LLM05 :** sorties utilisées sans validation.
- **LLM06 :** utilisation abusive des outils accessibles au modèle.
- **LLM07 :** fuite du prompt système.
- **LLM09 :** génération d'informations erronées.
- **LLM10 :** requêtes excessives et coûts d'inférence élevés.

Mesures de protection :
- Authentifier les utilisateurs et appliquer des autorisations adaptées.
- Limiter la taille et le volume des requêtes.
- Valider les sorties avant leur utilisation dans d'autres systèmes.
- Éviter de stocker des secrets dans les prompts système.
- Surveiller les erreurs, les coûts et les comportements anormaux.
- Restreindre les capacités des outils accessibles au modèle.

### 3.2 Base vectorielle et pipeline RAG

Un système RAG (*Retrieval-Augmented Generation*) récupère des documents pertinents et les transmet au modèle pour enrichir sa réponse.

Risques associés :
- **LLM01 :** des documents récupérés peuvent contenir des instructions malveillantes.
- **LLM08 :** les embeddings et la base vectorielle peuvent être manipulés ou insuffisamment protégés.
- **LLM09 :** des documents obsolètes ou incorrects peuvent produire des réponses trompeuses.

Mesures de protection :
- Vérifier la provenance et la qualité des documents indexés.
- Contrôler les autorisations d'accès aux documents et aux résultats récupérés.
- Surveiller la fraîcheur des sources.
- Traiter les documents récupérés comme des données non fiables.
- Évaluer la pertinence et la fiabilité du contexte transmis au modèle.

### 3.3 Pipeline d'entraînement

Le pipeline d'entraînement transforme les données en un modèle exploitable. Il dépend souvent de jeux de données, de modèles préentraînés et de dépendances externes.

Risques associés :
- **LLM02 :** données sensibles intégrées aux jeux d'entraînement.
- **LLM03 :** dépendances, modèles ou données tiers compromis.
- **LLM04 :** empoisonnement des données ou altération du modèle.

Mesures de protection :
- Vérifier la provenance des jeux de données et des modèles.
- Contrôler l'intégrité des artefacts et des versions.
- Limiter les accès aux environnements d'entraînement.
- Détecter les anomalies dans les données.
- Évaluer les modèles avant leur mise en production.

## 4. Exemple pratique : MegaCorp

MegaCorp développe un chatbot destiné à ses clients. Celui-ci utilise un LLM, une base vectorielle contenant les politiques de l'entreprise et des outils permettant de consulter le statut des commandes.

Un Threat Modeling permet d'identifier plusieurs scénarios.

| Scénario | Risque OWASP | Mesure prioritaire |
|---|---|---|
| Un document malveillant influence la réponse du chatbot. | LLM01 | Contrôler les sources et traiter le contexte récupéré comme non fiable. |
| Le modèle divulgue des données personnelles. | LLM02 | Réduire l'accès aux données sensibles et vérifier les autorisations. |
| Une dépendance tierce compromise affecte le système. | LLM03 | Vérifier les dépendances, les versions et leur provenance. |
| Des données d'entraînement sont manipulées. | LLM04 | Contrôler les données et surveiller les performances du modèle. |
| Une réponse contenant du contenu dangereux est exécutée ou rendue sans validation. | LLM05 | Valider et encoder les sorties selon leur contexte d'utilisation. |
| Le chatbot utilise un outil avec des permissions trop larges. | LLM06 | Appliquer le moindre privilège et vérifier chaque action côté serveur. |
| Le prompt système est divulgué. | LLM07 | Éviter d'y placer des secrets et limiter les informations internes exposées. |
| La base vectorielle contient des documents manipulés. | LLM08 | Sécuriser l'indexation, les accès et le processus de récupération. |
| Le chatbot invente une politique commerciale. | LLM09 | Vérifier les sources et prévoir une validation humaine pour les décisions importantes. |
| Des requêtes coûteuses font exploser la facture. | LLM10 | Mettre en place des quotas, des limites de débit et des alertes de coûts. |

Cet exemple montre qu'un même composant peut être exposé à plusieurs catégories de risques. La sécurité ne consiste donc pas à associer une seule menace à chaque composant, mais à examiner l'ensemble des scénarios pertinents.

## 5. Combiner STRIDE-AI, MITRE ATLAS et OWASP

Ces trois référentiels remplissent des fonctions complémentaires.

| Référentiel | Fonction | Question principale |
|---|---|---|
| **STRIDE-AI** | Classer les menaces selon leur nature. | Qu'est-ce qui pourrait mal tourner ? |
| **MITRE ATLAS** | Documenter les tactiques et techniques d'attaque propres à l'IA. | Comment un attaquant pourrait-il procéder ? |
| **OWASP Top 10 for LLM Applications** | Structurer l'analyse des risques propres aux applications LLM. | Quels risques sont pertinents pour les composants de notre architecture ? |

### Workflow pratique

1. **Cartographier l'architecture :** identifier les modèles, les API, les bases de données, les pipelines RAG et les outils.
2. **Appliquer STRIDE-AI :** examiner les menaces possibles pour chaque composant.
3. **Consulter MITRE ATLAS :** approfondir les techniques d'attaque correspondant aux menaces identifiées.
4. **Associer les catégories OWASP :** repérer les risques LLM pertinents pour chaque composant.
5. **Définir les mesures de protection :** prioriser les actions selon la gravité, la probabilité et l'exposition.
6. **Tester et réévaluer :** vérifier l'efficacité des contrôles et mettre à jour l'analyse lorsque l'architecture évolue.

## 6. À retenir

Le Threat Modeling d'un système LLM devient plus concret lorsqu'on associe les menaces à des composants précis.

- STRIDE-AI fournit une structure pour identifier les menaces.
- MITRE ATLAS apporte un catalogue de techniques d'attaque spécifiques à l'IA.
- OWASP LLM Top 10 aide à examiner les risques de sécurité propres aux applications LLM.

**L'objectif n'est pas simplement de connaître les dix risques, mais de savoir où ils apparaissent dans une architecture, comment ils peuvent être exploités et quelles mesures permettent de les réduire.**

## Références

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OWASP Top 10 for Web Applications 2025](https://owasp.org/Top10/2025/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [MITRE ATT&CK](https://attack.mitre.org/)
