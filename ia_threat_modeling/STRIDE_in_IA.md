# STRIDE-AI : Adapter STRIDE à la sécurité de l'intelligence artificielle

## 1. Introduction

STRIDE est un modèle de classification des menaces qui permet d'analyser les risques de sécurité selon six catégories. Plutôt que de remplacer ce modèle pour la sécurité de l'IA, on peut l'adapter aux caractéristiques des systèmes d'intelligence artificielle.

Les systèmes IA introduisent de nouveaux actifs et de nouvelles menaces : empoisonnement des données, extraction de modèles, manipulation des prompts, détournement d'agents et consommation excessive de ressources.

L'objectif de **STRIDE-AI** est donc de conserver les six catégories classiques tout en examinant comment elles se manifestent dans les composants IA.

## 2. Rappel des catégories STRIDE

| Catégorie | Propriété de sécurité | Signification traditionnelle |
|---|---|---|
| **S — Spoofing** | Authenticité | Usurper l'identité d'un utilisateur ou d'un service. |
| **T — Tampering** | Intégrité | Modifier des données ou du code sans autorisation. |
| **R — Repudiation** | Traçabilité des actions | Contester une action lorsqu'il n'existe pas de preuve suffisante pour l'attribuer. |
| **I — Information Disclosure** | Confidentialité | Divulguer des informations à des personnes non autorisées. |
| **D — Denial of Service** | Disponibilité | Rendre un service ou une ressource indisponible. |
| **E — Elevation of Privilege** | Autorisation | Obtenir des privilèges ou des capacités qui ne devraient pas être accessibles. |

## 3. Application de STRIDE aux systèmes IA

### S — Spoofing : usurpation des sources de données

Dans une application traditionnelle, le spoofing consiste notamment à se faire passer pour un utilisateur ou un service légitime.

Dans un système IA, une menace comparable consiste à **faire passer une source de données malveillante pour une source fiable**.

Exemples :
- Injection de faux documents dans une base de connaissances utilisée par un système RAG.
- Déploiement d'une fausse API qui imite un service IA légitime.
- Manipulation d'un système de reconnaissance faciale ou vocale.

**Exemple MegaCorp :** un chatbot utilise une base documentaire interne pour répondre aux clients. Un attaquant parvient à y introduire de fausses politiques commerciales. Le chatbot récupère ces documents et fournit des réponses incorrectes en les présentant comme fiables.

**Risque principal :** le système fonde ses réponses sur des informations dont l'origine ou l'authenticité n'est pas garantie.

### T — Tampering : altération et empoisonnement des données

Le tampering traditionnel consiste à modifier des données, du code ou une configuration sans autorisation.

Dans les systèmes IA, cette catégorie inclut notamment le **Data Poisoning**, qui consiste à contaminer les données d'entraînement pour influencer le comportement appris par le modèle.

Les effets peuvent être ciblés, par exemple provoquer certaines erreurs de classification, ou non ciblés, en dégradant globalement les performances.

Autres menaces :
- Modification directe des paramètres du modèle.
- Remplacement d'un modèle légitime par une version compromise.
- Manipulation des caractéristiques (*features*) utilisées pour produire une prédiction.
- Prompt injection, lorsque l'attaquant manipule les instructions ou le contexte transmis au modèle.

La classification d'une prompt injection dépend toutefois de son objectif et de ses conséquences. Elle peut relever du tampering si l'entrée est manipulée, ou de l'élévation de privilèges si elle permet de contourner des restrictions et d'obtenir des capacités non autorisées.

**Exemple MegaCorp :** le modèle de détection de fraude est réentraîné chaque mois. Des transactions soigneusement conçues contaminent progressivement les données d'entraînement. Le modèle finit par moins bien détecter certains schémas frauduleux.

**Risque principal :** le modèle apprend des associations incorrectes ou adopte un comportement compromis.

Références MITRE ATLAS :
- [Data Poisoning — AML.T0020](https://atlas.mitre.org/)
- [Backdoor ML Model — AML.T0018](https://atlas.mitre.org/)

### R — Repudiation : absence de traçabilité des décisions

La répudiation concerne la difficulté à prouver qu'une action a été effectuée lorsqu'il manque des journaux fiables.

Pour un système IA, il ne suffit pas de conserver la réponse finale. Il faut également pouvoir retracer les éléments qui ont contribué à la décision.

Les informations utiles peuvent inclure :
- Les entrées reçues par le modèle.
- La version du modèle utilisée.
- Les caractéristiques fournies au modèle.
- Les documents récupérés par un pipeline RAG.
- Les outils appelés et les actions exécutées.
- Les horodatages et les résultats produits.

Il faut également protéger les journaux contre les modifications non autorisées et limiter la collecte de données sensibles.

**Exemple MegaCorp :** un régulateur demande pourquoi le système antifraude a approuvé une transaction suspecte trois semaines auparavant. L'équipe ne connaît ni la version du modèle en production, ni les données utilisées, ni le seuil de décision appliqué.

**Risque principal :** l'organisation ne peut pas expliquer, reproduire ou auditer correctement une décision importante.

*Attention :* l'absence d'explicabilité intrinsèque d'un modèle et l'absence de traçabilité sont deux problèmes différents. Une décision peut être correctement journalisée sans que le fonctionnement interne du modèle soit entièrement interprétable.

### I — Information Disclosure : divulgation et extraction du modèle

La divulgation d'informations concerne l'accès non autorisé à des données confidentielles.

Dans les systèmes IA, elle peut prendre plusieurs formes.

- **Model Extraction :** interroger systématiquement une API pour construire un modèle de substitution qui reproduit une partie des fonctionnalités du modèle original.
- **Training Data Extraction :** provoquer la divulgation de données mémorisées pendant l'entraînement.
- **System Prompt Leakage :** obtenir des instructions internes qui n'étaient pas destinées à être divulguées.
- **Embedding Inversion :** tenter de reconstruire des informations sur les données originales à partir de leurs représentations vectorielles.

Ces attaques n'ont pas toutes le même niveau de difficulté. Par exemple, extraire un modèle fonctionnellement similaire ne signifie pas nécessairement récupérer ses paramètres exacts.

**Exemple MegaCorp :** un concurrent envoie de nombreuses requêtes à l'API d'un moteur de recommandation et collecte les résultats. Il utilise ensuite ces observations pour entraîner un modèle de substitution qui reproduit une partie de la logique propriétaire.

**Risque principal :** perte de confidentialité, fuite de données sensibles ou atteinte à la propriété intellectuelle.

Références MITRE ATLAS :
- [Extract ML Model — AML.T0024](https://atlas.mitre.org/)
- [Infer Training Data Membership — AML.T0025](https://atlas.mitre.org/)

### D — Denial of Service : épuisement des ressources et des coûts

Dans une attaque traditionnelle par déni de service, l'objectif est de rendre un service indisponible en épuisant ses ressources.

Les systèmes IA présentent également un risque financier : le **Denial of Wallet**. Un attaquant peut multiplier les requêtes coûteuses et provoquer une forte augmentation des dépenses d'inférence, même si le service reste techniquement accessible.

Autres menaces :
- Saturation des GPU et des capacités de calcul.
- Requêtes complexes consommant beaucoup de ressources.
- Entrées conçues pour augmenter le coût de calcul, parfois appelées *sponge examples*.
- Perturbation des pipelines d'entraînement par l'envoi massif de données inutiles.

**Exemple MegaCorp :** un attaquant envoie des milliers de requêtes conçues pour déclencher de longues réponses du chatbot. Le service reste disponible, mais la facture mensuelle d'inférence passe de 15 000 à 180 000 dollars.

**Risque principal :** indisponibilité du service, dégradation des performances ou pertes financières importantes.

Mesures de protection :
- Limitation du débit et des quotas.
- Plafonds de dépenses et alertes de facturation.
- Limitation de la taille des entrées et des sorties.
- Surveillance de la consommation par utilisateur ou par clé API.

Référence : [OWASP GenAI Security Project](https://genai.owasp.org/).

### E — Elevation of Privilege : jailbreak et capacités excessives

L'élévation de privilèges consiste à obtenir des capacités ou des droits qui ne devraient pas être accessibles.

Dans un système LLM, le **jailbreaking** cherche à contourner les restrictions du modèle. Toutefois, contourner une règle de comportement ne signifie pas automatiquement obtenir des privilèges techniques supplémentaires.

Le risque devient beaucoup plus important lorsqu'un modèle peut utiliser des outils avec des permissions réelles.

Autres menaces :
- **Excessive Agency :** accorder à un agent plus de permissions que nécessaire.
- **Tool Use Exploitation :** manipuler un agent pour lui faire appeler des outils de manière non autorisée.
- **Cross-Plugin Escalation :** exploiter les interactions entre composants ou plugins ayant des niveaux de privilèges différents.

**Exemple MegaCorp :** un chatbot peut consulter une base de données pour fournir le statut des commandes. Ses outils disposent toutefois de permissions trop larges. Si un attaquant manipule le chatbot et que les contrôles côté serveur sont insuffisants, il peut tenter d'obtenir des informations personnelles auxquelles il ne devrait pas accéder.

**Risque principal :** le détournement du modèle peut devenir un accès non autorisé à des systèmes, des données ou des fonctions internes.

Mesures de protection :
- Appliquer le principe du moindre privilège.
- Limiter les outils et les opérations accessibles au modèle.
- Vérifier les autorisations côté serveur pour chaque action.
- Exiger une validation humaine pour les opérations sensibles.
- Séparer les permissions de lecture et d'écriture.

Références :
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)

## 4. Tableau récapitulatif STRIDE-AI

| Catégorie | Menace IA principale | Exemple |
|---|---|---|
| Spoofing | Usurpation d'une source de données | Faux documents ajoutés à une base RAG. |
| Tampering | Data Poisoning | Données d'entraînement contaminées. |
| Repudiation | Traçabilité insuffisante | Décision impossible à auditer correctement. |
| Information Disclosure | Model Extraction | Modèle de substitution construit à partir des sorties d'une API. |
| Denial of Service | Épuisement des ressources ou des coûts | Requêtes provoquant une facture d'inférence excessive. |
| Elevation of Privilege | Jailbreak et permissions excessives | Agent manipulé pour tenter d'accéder à des données protégées. |

## 5. Ce que STRIDE ne couvre pas entièrement

Même adapté aux systèmes IA, STRIDE ne permet pas à lui seul de décrire tous les risques.

### Adversarial Examples

Des entrées spécialement conçues peuvent provoquer une mauvaise classification ou une réponse inattendue. Leur classification dépend du contexte : altération des entrées, usurpation ou contournement des restrictions peuvent être en jeu.

### Biais et équité

Un modèle peut produire des résultats injustes ou discriminatoires sans qu'un attaquant l'ait nécessairement compromis. Ces problèmes ont des implications importantes en matière de conformité et de responsabilité, mais ne correspondent pas directement à une catégorie STRIDE classique.

### Comportements émergents

Certains comportements complexes peuvent être difficiles à anticiper lors de la conception. Ils doivent être étudiés au moyen d'évaluations, de tests et d'une surveillance continue.

Pour compléter l'analyse, des référentiels spécialisés comme **MITRE ATLAS** fournissent un catalogue de tactiques et de techniques d'attaque ciblant les systèmes d'apprentissage automatique.

## 6. Conclusion

STRIDE reste un outil utile pour structurer le Threat Modeling des systèmes IA. Il faut cependant adapter l'analyse aux particularités des données d'entraînement, des paramètres, des pipelines RAG, des API et des agents capables d'exécuter des actions.

La classification d'une menace dépend du contexte, de l'actif visé et de l'impact recherché. Une même attaque peut donc concerner plusieurs catégories.

**À retenir :** STRIDE aide à organiser les questions de sécurité ; les référentiels spécialisés comme MITRE ATLAS permettent d'approfondir les techniques d'attaque propres à l'IA.

## Références

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [Microsoft Threat Modeling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
