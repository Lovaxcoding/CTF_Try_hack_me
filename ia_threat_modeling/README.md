# Threat Modeling (Modélisation des menaces)

## 1. Définition

Le **Threat Modeling** est une méthode qui permet d'identifier les menaces potentielles contre un système, d'évaluer les risques et de définir des mesures de sécurité avant qu'une attaque ne se produise.

L'objectif est d'anticiper les actions possibles d'un attaquant afin de mieux protéger les données, les utilisateurs et les services.

Dans le cas des systèmes d'intelligence artificielle, cette démarche doit prendre en compte les modèles, les données d'entraînement, les embeddings, les prompts système et les outils auxquels un modèle peut accéder. Une application d'IA ne se résume pas à une application traditionnelle à laquelle on aurait simplement ajouté un modèle.

## 2. Les étapes principales

1. **Définir le système :** comprendre son architecture, ses composants et ses interactions.
2. **Identifier les actifs :** déterminer ce qui doit être protégé, comme les données sensibles, les comptes, les clés d'accès et les modèles.
3. **Cartographier les flux de données :** comprendre comment les données circulent entre les différentes étapes et composants.
4. **Identifier les menaces :** rechercher les moyens possibles d'attaquer le système.
5. **Évaluer et prioriser les risques :** estimer leur probabilité, leur impact et leur gravité.
6. **Définir les protections :** proposer des mesures pour réduire les risques identifiés.
7. **Valider les mesures :** effectuer des tests et réévaluer les risques après chaque changement important.

Ce processus est itératif. Il doit être repris lorsqu'un modèle est remplacé, qu'une nouvelle source de données est ajoutée ou que des capacités autonomes sont introduites.

## 3. La méthode STRIDE

STRIDE est un modèle qui classe les menaces en six catégories :

| Catégorie | Description | Exemple dans un système d'IA |
|---|---|---|
| **Spoofing** | Usurpation d'identité | Une source malveillante se fait passer pour une source de données fiable. |
| **Tampering** | Modification non autorisée | Des données d'entraînement sont empoisonnées ou un modèle est modifié. |
| **Repudiation** | Contestation d'une action effectuée | Des journaux insuffisants empêchent de retracer une action réalisée par un agent IA. |
| **Information Disclosure** | Divulgation d'informations sensibles | Le modèle révèle des données confidentielles ou des informations issues de son entraînement. |
| **Denial of Service** | Indisponibilité d'un service | Des requêtes coûteuses épuisent les ressources ou le budget de l'API. |
| **Elevation of Privilege** | Obtention de privilèges excessifs | Une manipulation conduit un agent à utiliser un outil avec des permissions inappropriées. |

STRIDE fournit une classification générale. Dans les systèmes d'IA, il faut adapter chaque catégorie au contexte technique. Une même attaque peut toucher plusieurs catégories selon ses conséquences.

## 4. Les actifs spécifiques aux systèmes d'IA

L'analyse doit dépasser les composants classiques d'une application web.

| Actif | Rôle | Risque potentiel |
|---|---|---|
| Données d'entraînement | Données utilisées pour entraîner le modèle | Empoisonnement, fuite de données sensibles |
| Poids du modèle | Paramètres appris pendant l'entraînement | Vol, modification ou remplacement du modèle |
| Embeddings | Représentations vectorielles de données | Extraction d'informations ou manipulation de la base vectorielle |
| Prompts système | Instructions définissant le comportement attendu | Divulgation ou contournement des instructions |
| Feature stores | Stockage des caractéristiques utilisées par les modèles | Modification ou exposition de caractéristiques |
| Registres de modèles | Inventaire et gestion des modèles et versions | Déploiement d'un modèle non fiable |
| Sources RAG | Documents récupérés pour enrichir les réponses | Injection de contenu malveillant ou récupération de données non autorisées |
| Outils et API | Actions externes accessibles au modèle | Actions non autorisées et permissions excessives |

Ces actifs peuvent appartenir à différentes étapes du cycle de vie de l'IA. Leur inventaire aide à déterminer ce qui doit être protégé et où les contrôles sont nécessaires.

## 5. Cartographier la chaîne d'approvisionnement des données

Un système d'IA dépend d'une chaîne de traitement qui va de la collecte des données jusqu'à leur utilisation en production.

**Flux simplifié :**

1. **Collecte :** récupération des données provenant de sources internes ou externes.
2. **Nettoyage et étiquetage :** préparation et annotation des données.
3. **Entraînement :** utilisation des données pour apprendre les paramètres du modèle.
4. **Validation et empaquetage :** évaluation, versionnement et préparation du modèle.
5. **Déploiement et inférence :** utilisation du modèle pour produire des réponses ou des prédictions.
6. **Récupération de contexte :** si le système utilise le RAG, recherche de documents ou d'embeddings pour enrichir les réponses.

Chaque étape possède ses propres risques. Par exemple, des données malveillantes introduites lors de la collecte peuvent influencer le modèle après l'entraînement. Dans un système RAG, un document malveillant peut également manipuler le contexte fourni au modèle sans que les poids de celui-ci soient modifiés.

Il faut donc examiner les sources, les accès, les transformations, la provenance des données et les mécanismes de validation à chaque étape.

## 6. Compléter STRIDE avec MITRE ATLAS

**MITRE ATLAS** (*Adversarial Threat Landscape for Artificial-Intelligence Systems*) est un référentiel consacré aux techniques d'attaque visant les systèmes d'intelligence artificielle.

STRIDE aide à identifier le type de menace. ATLAS permet ensuite d'approfondir l'analyse à l'aide de techniques d'attaque documentées, de leurs identifiants et des mesures d'atténuation associées.

| Technique d'attaque | Exemple | Catégorie STRIDE possible |
|---|---|---|
| Data Poisoning | Altération des données d'entraînement | Tampering |
| Model Extraction | Reconstitution d'un modèle à partir de ses sorties | Information Disclosure |
| Evasion | Modification d'une entrée pour tromper un modèle | Dépend du scénario et de ses conséquences |
| LLM Prompt Injection | Manipulation des instructions ou du contexte d'un LLM | Souvent Tampering, selon le scénario |
| Model Backdoor | Introduction d'un comportement malveillant déclenché par une entrée particulière | Tampering |

Ces correspondances sont indicatives, et non des équivalences absolues. La classification dépend de l'architecture, des objectifs de l'attaquant et des effets de l'attaque.

**Méthode :**
1. Identifier une menace avec STRIDE.
2. Rechercher dans MITRE ATLAS les techniques correspondant au scénario.
3. Examiner les prérequis, les techniques associées et les mitigations.
4. Documenter les contrôles à mettre en place et les tests permettant de les vérifier.

Référence : https://atlas.mitre.org/

## 7. Utiliser l'OWASP LLM Top 10

L'**OWASP Top 10 for LLM Applications** fournit une classification des principaux risques de sécurité liés aux applications utilisant des grands modèles de langage.

Contrairement à STRIDE, qui classe les menaces selon leur nature, l'OWASP LLM Top 10 aide à repérer des catégories de risques spécifiques aux LLM dans les composants d'une architecture.

| Risque | Description | Composants à examiner |
|---|---|---|
| LLM01 – Prompt Injection | Manipulation des instructions par une entrée ou un contenu récupéré | Entrées utilisateur, contexte RAG, agents |
| LLM02 – Sensitive Information Disclosure | Exposition d'informations sensibles | Modèle, journaux, sources de données |
| LLM03 – Supply Chain | Compromission de dépendances, modèles ou données | Dépendances, modèles, pipelines |
| LLM04 – Data and Model Poisoning | Altération malveillante des données ou du modèle | Données d'entraînement, pipeline, modèle |
| LLM05 – Improper Output Handling | Traitement dangereux des sorties du modèle | Backend, interfaces, interpréteurs, outils |
| LLM06 – Excessive Agency | Permissions ou autonomie excessives | Agents, outils, API |
| LLM07 – System Prompt Leakage | Divulgation des instructions système | Prompts et réponses du modèle |
| LLM08 – Vector and Embedding Weaknesses | Faiblesses liées aux embeddings et aux bases vectorielles | Base vectorielle, pipeline RAG |
| LLM09 – Misinformation | Réponses fausses ou trompeuses pouvant entraîner des conséquences | Modèle, interface, processus de décision |
| LLM10 – Unbounded Consumption | Consommation excessive de ressources ou de budget | Endpoint d'inférence, API, infrastructure |

La présence d'un composant ne signifie pas automatiquement qu'il est vulnérable. Il faut examiner son implémentation, ses permissions, ses protections et les conséquences possibles d'une exploitation.

## 8. Exemple pratique : application web traditionnelle

Pour une application web connectée à une base de données, un Threat Modeling peut révéler plusieurs risques :

- Un attaquant utilise des identifiants volés pour accéder à un compte.
- Une injection SQL permet de manipuler des requêtes.
- Un contrôle d'accès insuffisant expose les données d'autres utilisateurs.
- Un nombre excessif de requêtes rend le service indisponible.

Les mesures de protection peuvent inclure une authentification robuste, des requêtes SQL paramétrées, la vérification des autorisations côté serveur et la limitation du nombre de requêtes.

Cet exemple illustre les principes généraux. Les systèmes d'IA nécessitent une analyse supplémentaire de leurs modèles, de leurs données et de leurs capacités d'action.

## 9. Application à la sécurité des LLM

Dans un système utilisant un modèle de langage, il faut notamment examiner :

- Les données sensibles accessibles au modèle.
- Les risques de prompt injection et de fuite d'informations.
- La fiabilité des documents récupérés par le système RAG.
- Les permissions accordées aux outils que le modèle peut utiliser.
- Les actions qui peuvent être exécutées sans validation humaine.
- La consommation de ressources et les coûts associés aux requêtes.
- La traçabilité des actions et la gestion des versions du modèle.
- Les conséquences possibles d'une réponse erronée ou d'une manipulation du modèle.

Il faut également distinguer les erreurs de génération des vulnérabilités exploitables. Une réponse incorrecte n'est pas automatiquement une faille de sécurité, mais elle peut le devenir si elle déclenche une action dangereuse ou influence une décision critique sans contrôle adapté.

## 10. Workflow complet de modélisation des menaces IA

Le processus étudié dans cette room peut être résumé ainsi :

1. **Inventorier les actifs IA :** données, poids du modèle, embeddings, prompts, registres et outils.
2. **Cartographier l'architecture et les flux :** identifier les composants, les échanges et les frontières de confiance.
3. **Appliquer STRIDE :** identifier les catégories de menaces pertinentes pour chaque composant.
4. **Enrichir l'analyse avec MITRE ATLAS :** associer les scénarios à des techniques d'attaque documentées et étudier leurs mitigations.
5. **Cartographier les risques avec l'OWASP LLM Top 10 :** relier les risques spécifiques aux composants concernés.
6. **Évaluer et prioriser :** tenir compte de la vraisemblance, de l'impact, de l'exposition et de l'efficacité des contrôles existants.
7. **Définir les mesures de sécurité :** attribuer des actions concrètes aux risques prioritaires.
8. **Tester et réévaluer :** vérifier les protections et reprendre l'analyse lorsque le système évolue.

### Application au scénario MegaCorp

Pour MegaCorp, l'objectif est d'évaluer les composants réels de l'architecture étudiée, de repérer les risques OWASP pertinents, de les analyser avec STRIDE et d'utiliser ATLAS pour préciser les méthodes d'attaque possibles.

Le résultat attendu est une évaluation priorisée qui relie chaque risque à un composant, à ses conséquences et à des mesures de protection. Les priorités doivent être fondées sur les éléments de l'architecture et les résultats de l'analyse, plutôt que sur des suppositions.

## 11. À retenir

- **Les systèmes d'IA ont une surface d'attaque spécifique.** Les données d'entraînement, les modèles, les embeddings, les prompts et les outils élargissent les actifs à protéger.
- **STRIDE classe les menaces.** Il fournit une structure pour identifier les catégories de risques, à adapter au contexte de l'IA.
- **MITRE ATLAS décrit les techniques d'attaque.** Il permet d'aller des catégories générales aux méthodes documentées et aux mesures d'atténuation.
- **L'OWASP LLM Top 10 aide à localiser les risques.** Il facilite l'analyse des composants et des faiblesses propres aux applications LLM.
- **La priorisation rend l'analyse exploitable.** Chaque risque doit être relié à un composant, à un impact et à des mesures de sécurité.
- **Le processus doit être répété.** Une modification du modèle, des sources de données ou des capacités d'un agent peut changer le profil de risque.

Le Threat Modeling complète le pentest : la modélisation identifie et priorise les scénarios de risque, tandis que les tests vérifient les faiblesses et les protections dans des conditions définies.

## Références

- OWASP Threat Modeling : https://owasp.org/www-community/Threat_Modeling
- Microsoft STRIDE : https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- OWASP Top 10 for LLM Applications : https://genai.owasp.org/llm-top-10/
- MITRE ATLAS : https://atlas.mitre.org/
- MITRE ATT&CK : https://attack.mitre.org/
