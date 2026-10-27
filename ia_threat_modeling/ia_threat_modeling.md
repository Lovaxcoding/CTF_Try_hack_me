# AI Threat Modeling

## 1. Introduction

Le **Threat Modeling appliqué à l'intelligence artificielle** consiste à identifier les actifs critiques d'un système IA, les points d'entrée possibles pour un attaquant et les menaces qui peuvent compromettre son fonctionnement, ses données ou sa sécurité.

Contrairement aux applications traditionnelles, les systèmes IA possèdent des actifs spécifiques, comme les données d'entraînement, les poids du modèle, les embeddings et les prompts système. Leur chaîne d'approvisionnement présente également des risques particuliers.

## 2. Les actifs critiques d'un système IA

| Actif | Description | Risque principal |
|---|---|---|
| **Training Data** | Données utilisées pour entraîner le modèle. | Le data poisoning peut corrompre les données et influencer le comportement appris. |
| **Model Weights / Parameters** | Valeurs numériques représentant les paramètres appris par le modèle. | Leur vol peut permettre de reproduire une grande partie des capacités du modèle. |
| **Embedding Vectors** | Représentations numériques de données utilisées pour mesurer leur similarité. | Leur manipulation peut altérer les résultats de recherche ou le contexte fourni au modèle. |
| **System Prompts** | Instructions qui orientent le comportement du modèle. | Leur divulgation peut révéler des règles internes et faciliter certaines tentatives de contournement. |
| **Feature Stores** | Dépôts de caractéristiques préparées pour alimenter les modèles. | Leur altération peut fausser les prédictions sans modifier directement le modèle. |
| **Model Registry / Artifacts** | Emplacements où sont stockées les versions des modèles et leurs artefacts. | Leur compromission peut permettre de remplacer un modèle légitime par un modèle malveillant. |

## 3. La chaîne d'approvisionnement des données IA

La chaîne d'approvisionnement IA (*AI Data Supply Chain*) regroupe les étapes qui transforment des données brutes en un modèle déployé en production.

### Étape 1 : Collecte des données

Les données proviennent notamment du Web, de bases de données internes, des utilisateurs ou de fournisseurs externes.

**Menace :** un attaquant peut tenter d'introduire des données malveillantes dans une source utilisée par le système.

### Étape 2 : Nettoyage et étiquetage

Les données sont filtrées, transformées et associées à des étiquettes.

**Menace :** des données mal étiquetées ou des étiquettes volontairement corrompues peuvent conduire le modèle à apprendre des associations incorrectes.

### Étape 3 : Entraînement du modèle

Le modèle apprend des régularités à partir des données préparées. Une partie des effets d'un empoisonnement peut alors se retrouver dans ses paramètres.

**Menace :** un modèle entraîné sur des données compromises peut adopter un comportement incorrect ou malveillant dans certaines conditions.

La correction peut nécessiter une nouvelle préparation des données et un réentraînement, selon la nature et l'étendue de la compromission.

### Étape 4 : Validation et stockage

Le modèle est évalué, versionné et enregistré avant son déploiement.

**Menace :** si le registre ou les artefacts sont compromis, un attaquant peut tenter de remplacer le modèle validé par une version modifiée.

Un modèle comportant une porte dérobée (*backdoor*) peut réussir les tests habituels si les entrées déclenchant son comportement malveillant sont absentes des données de validation.

### Étape 5 : Inférence en production

Le modèle reçoit des entrées et produit des réponses ou des prédictions.

Dans les systèmes utilisant la génération augmentée par récupération (*RAG*), des documents supplémentaires sont récupérés depuis une base documentaire ou vectorielle.

**Menace :** des documents malveillants ou manipulés peuvent influencer le contexte transmis au modèle au moment de la requête.

### Exemple : système de détection de fraude

Une entreprise réentraîne son modèle chaque mois à partir de transactions récentes. Si des données frauduleuses ou des étiquettes incorrectes contaminent progressivement le processus d'entraînement, le modèle peut apprendre des associations erronées et devenir moins efficace pour détecter certains scénarios de fraude.

Cet exemple illustre l'importance de contrôler les sources, la qualité des données, les étiquettes et les résultats du modèle après chaque réentraînement.

## 4. Pourquoi STRIDE doit être adapté à l'IA

STRIDE est un modèle de classification des menaces comprenant six catégories.

| Catégorie | Signification | Exemple dans un système IA |
|---|---|---|
| **Spoofing** | Usurpation d'identité | Un attaquant se fait passer pour un utilisateur autorisé. |
| **Tampering** | Altération | Modification des données d'entraînement ou des paramètres du modèle. |
| **Repudiation** | Contestation d'une action | Absence de journaux fiables permettant de retracer une action effectuée par un agent IA. |
| **Information Disclosure** | Divulgation d'informations | Fuite de données sensibles ou extraction non autorisée des paramètres du modèle. |
| **Denial of Service** | Déni de service | Requêtes excessives consommant les ressources du système IA. |
| **Elevation of Privilege** | Élévation de privilèges | Un agent IA exploite des permissions excessives pour effectuer une action non autorisée. |

### Les limites de STRIDE dans le contexte IA

**1. L'intégrité des données d'entraînement**

La catégorie *Tampering* couvre l'altération des données, mais les effets d'un empoisonnement peuvent apparaître tardivement et rester difficiles à détecter.

**2. La manipulation du comportement du modèle**

Des entrées adversariales peuvent provoquer des erreurs de classification, des réponses dangereuses ou des contournements de protections. Ces scénarios peuvent relever de plusieurs catégories de STRIDE selon le système et l'impact.

**3. Les permissions des agents IA**

Un modèle connecté à des outils peut consulter des bases de données, naviguer sur le Web ou exécuter du code. Si ses permissions sont excessives, une manipulation de ses instructions peut conduire à des actions non autorisées.

**4. Le vol de propriété intellectuelle**

L'extraction des paramètres d'un modèle constitue une menace pour la confidentialité et la propriété intellectuelle. Elle peut exposer une partie importante de l'investissement consacré au développement du modèle, sans nécessairement permettre de récupérer exactement ses paramètres à partir de simples requêtes API.

**Conclusion :** STRIDE reste utile pour structurer l'analyse des menaces, mais il doit être complété par une analyse propre aux données, à l'entraînement, aux modèles et aux mécanismes d'inférence.

## 5. Mesures de protection

Pour réduire les risques associés à la chaîne d'approvisionnement IA :

- Vérifier la provenance et l'intégrité des données.
- Contrôler les processus de nettoyage et d'étiquetage.
- Sécuriser les paramètres, les artefacts et les registres de modèles.
- Évaluer les modèles avec des scénarios adversariaux adaptés.
- Contrôler les documents récupérés dans les pipelines RAG.
- Appliquer le principe du moindre privilège aux outils accessibles aux agents IA.
- Journaliser les actions importantes et surveiller les comportements anormaux.
- Réévaluer les risques après chaque modification importante du modèle ou de son environnement.

## 6. À retenir

Le Threat Modeling d'un système IA ne se limite pas à protéger une application ou une API. Il faut également protéger les données qui enseignent au modèle, les paramètres qui encodent ses capacités, les artefacts utilisés pour le déployer et les informations qu'il reçoit en production.

**Un système IA peut être compromis sans que son code applicatif soit directement modifié.** Une source de données empoisonnée, un registre compromis ou un document malveillant dans un pipeline RAG peut suffire à créer un risque important.

L'objectif du Threat Modeling est donc d'identifier ces points de défaillance, d'évaluer leurs conséquences et de mettre en place des contrôles adaptés à chaque étape.

## Références

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [Microsoft Threat Modeling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [MITRE ATLAS](https://atlas.mitre.org/)

## Notes du laboratoire

- **Actifs identifiés :** données d'entraînement, paramètres du modèle, embeddings, prompts système, feature stores et registres de modèles.
- **Concept clé :** la chaîne d'approvisionnement IA introduit des risques qui ne sont pas entièrement couverts par une analyse classique de l'application.
- **Point à retenir :** STRIDE est un point de départ, pas une analyse exhaustive des menaces propres à l'IA.


