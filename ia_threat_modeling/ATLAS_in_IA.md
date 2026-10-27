# MITRE ATLAS : Référentiel des menaces contre les systèmes IA

## 1. Qu'est-ce que MITRE ATLAS ?

**MITRE ATLAS** (*Adversarial Threat Landscape for Artificial-Intelligence Systems*) est une base de connaissances qui recense les tactiques et les techniques utilisées pour attaquer les systèmes d'intelligence artificielle et de Machine Learning.

Il peut être considéré comme le pendant spécialisé de **MITRE ATT&CK**, qui documente les comportements des attaquants contre les systèmes informatiques traditionnels.

- [MITRE ATT&CK](https://attack.mitre.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)

ATLAS aide les équipes de sécurité à comprendre comment les attaques contre les systèmes IA peuvent se dérouler, à identifier les techniques pertinentes et à choisir des mesures de protection adaptées.

Le nombre de tactiques, de techniques et d'études de cas évolue avec les mises à jour du référentiel. Il est donc préférable de consulter le site officiel pour obtenir les chiffres actuels.

## 2. Comment ATLAS est-il structuré ?

ATLAS utilise une organisation similaire à celle de MITRE ATT&CK.

| Élément | Rôle | Exemple |
|---|---|---|
| **Tactic** | Objectif poursuivi par l'attaquant. | ML Attack Staging |
| **Technique** | Méthode employée pour atteindre cet objectif. | Data Poisoning (AML.T0020) |
| **Sous-technique** | Variante plus précise d'une technique. | Craft Adversarial Data (AML.T0043.004) |
| **Mitigation** | Mesure permettant de prévenir ou de réduire le risque. | Validation des données et suivi de leur provenance |

Les tactiques décrivent principalement le *pourquoi*, tandis que les techniques expliquent le *comment*.

Lors d'un Threat Modeling, on peut partir d'un risque identifié, rechercher les techniques ATLAS correspondantes, puis étudier leurs conditions de réussite et les mesures de protection associées.

## 3. Cinq techniques ATLAS importantes

### 3.1 Data Poisoning — AML.T0020

Le **Data Poisoning** consiste à introduire des données malveillantes ou manipulées dans le processus d'entraînement d'un modèle.

L'objectif est d'influencer le comportement appris par le modèle. L'attaque peut être ciblée, en provoquant certaines erreurs précises, ou non ciblée, en dégradant globalement ses performances.

**Correspondance STRIDE :** Tampering.

**Exemple MegaCorp :** des transactions manipulées contaminent les données utilisées pour réentraîner le système de détection de fraude. Le modèle devient progressivement moins efficace contre certains scénarios frauduleux.

**Mesures de protection :**
- Vérifier la provenance des données.
- Détecter les anomalies dans les données d'entraînement.
- Contrôler la qualité des étiquettes.
- Surveiller les performances du modèle après chaque réentraînement.

### 3.2 Model Extraction — AML.T0024

Le **Model Extraction** consiste à interroger systématiquement un modèle accessible via une API afin de construire un modèle de substitution reproduisant une partie de son comportement.

Cette attaque ne nécessite pas nécessairement un accès direct aux paramètres internes du modèle. Elle exploite les informations obtenues à travers ses entrées et ses sorties.

**Correspondance STRIDE :** Information Disclosure.

**Exemple MegaCorp :** un concurrent interroge le moteur de recommandation avec de nombreuses combinaisons de produits et d'utilisateurs. Il utilise les réponses obtenues pour entraîner un modèle qui reproduit une partie de la logique propriétaire.

**Mesures de protection :**
- Appliquer des quotas et des limites de requêtes.
- Surveiller les comportements d'interrogation systématique.
- Limiter les informations retournées par l'API lorsque cela est justifié.
- Protéger les interfaces de prédiction par une authentification et des autorisations adaptées.

### 3.3 Evade ML Model — AML.T0015

Cette technique consiste à construire des entrées adversariales destinées à empêcher un modèle de reconnaître correctement un élément ou de produire la classification attendue.

Elle peut notamment viser les systèmes de détection de logiciels malveillants, les filtres de contenu ou les systèmes de classification.

**Correspondance STRIDE :** elle dépend du contexte et peut concerner Tampering, Spoofing ou Elevation of Privilege.

**Exemple :** un attaquant modifie certains éléments d'un fichier afin de tenter d'échapper à un modèle de détection de logiciels malveillants.

**Mesures de protection :**
- Évaluer le modèle avec des exemples adversariaux.
- Mesurer ses limites et ses taux d'erreur.
- Combiner plusieurs contrôles de sécurité indépendants.
- Réévaluer régulièrement les performances face à de nouvelles techniques d'évasion.

### 3.4 LLM Prompt Injection — AML.T0051

La **Prompt Injection** consiste à manipuler le comportement d'un modèle de langage en introduisant des instructions malveillantes dans les données qu'il traite.

On distingue deux formes principales.

- **Direct Prompt Injection :** l'attaquant place les instructions malveillantes directement dans son message au modèle.
- **Indirect Prompt Injection :** les instructions sont intégrées dans un contenu externe que le modèle consulte ou traite, comme une page Web, un courriel ou un document récupéré par un système RAG.

**Correspondance STRIDE :** Tampering lorsque l'entrée ou le contexte est manipulé. Si la manipulation conduit à des actions non autorisées, d'autres catégories peuvent également s'appliquer.

**Exemple MegaCorp :** le chatbot récupère des documents depuis une base de connaissances interne. Un document contenant des instructions malveillantes tente de détourner son comportement lorsque celui-ci est utilisé comme contexte.

**Mesures de protection :**
- Traiter les contenus récupérés comme des données non fiables.
- Séparer autant que possible les instructions de confiance des contenus externes.
- Limiter les permissions des outils accessibles au modèle.
- Vérifier les autorisations côté serveur avant toute action sensible.
- Exiger une confirmation humaine pour les opérations à fort impact.

### 3.5 Backdoor ML Model — AML.T0018

Une **Backdoor** est un comportement caché intégré à un modèle, qui ne se manifeste que lorsque certaines conditions ou entrées spécifiques sont présentes.

Le modèle peut sembler fonctionner normalement lors des évaluations classiques, tout en produisant un comportement particulier lorsque le déclencheur prévu apparaît.

**Correspondance STRIDE :** principalement Tampering lorsque le modèle ou son entraînement a été compromis.

**Exemple :** un modèle de classification fonctionne correctement sur les données habituelles, mais classe incorrectement certaines entrées lorsqu'un motif particulier est présent.

**Mesures de protection :**
- Sécuriser les données et les environnements d'entraînement.
- Vérifier l'origine et l'intégrité des modèles récupérés.
- Contrôler les versions stockées dans le registre de modèles.
- Tester des scénarios inhabituels et des entrées susceptibles de déclencher des comportements cachés.

## 4. Combiner STRIDE et MITRE ATLAS

STRIDE et ATLAS remplissent des rôles complémentaires.

1. **Commencer par STRIDE :** analyser chaque composant et identifier les catégories de menaces possibles.
2. **Approfondir avec ATLAS :** rechercher les techniques correspondant aux menaces identifiées.
3. **Étudier les conditions d'attaque :** déterminer les accès, les prérequis et les faiblesses nécessaires à leur réussite.
4. **Appliquer les mesures de protection :** sélectionner les contrôles adaptés et vérifier leur efficacité.

### Exemple : système antifraude de MegaCorp

L'analyse STRIDE révèle un risque de modification malveillante des données d'entraînement.

Le référentiel ATLAS permet ensuite d'identifier la technique **Data Poisoning (AML.T0020)** et d'étudier les conditions dans lesquelles elle peut compromettre le système.

L'équipe peut alors définir des mesures concrètes : contrôle de provenance, détection d'anomalies, surveillance des données et évaluation du modèle après chaque réentraînement.

L'analyse passe ainsi d'une observation générale, « les données d'entraînement peuvent être compromises », à un risque documenté associé à des techniques et à des mesures de protection précises.

## 5. Études de cas réelles

ATLAS comprend des études de cas qui permettent d'examiner des incidents et des démonstrations d'attaques contre des systèmes IA.

### ShadowRay — AML.CS0023

Cette étude porte sur des attaques exploitant des vulnérabilités de l'infrastructure Ray, utilisée pour des charges de travail distribuées, notamment en IA.

Elle illustre le risque que représentent les environnements d'entraînement et les infrastructures qui prennent en charge les modèles.

Référence : [MITRE ATLAS — Studies](https://atlas.mitre.org/studies)

### Morris II Worm — AML.CS0024

Cette étude décrit une démonstration de ver exploitant des mécanismes de prompt injection pour se propager entre des agents IA dans un scénario utilisant des systèmes de courriels et de récupération de contexte.

Elle met en évidence les risques liés aux contenus externes non fiables, à la propagation automatique et à l'accès aux données sensibles.

Référence : [MITRE ATLAS — Studies](https://atlas.mitre.org/studies)

Ces études permettent de relier les techniques documentées à des scénarios concrets, plutôt que de considérer les attaques contre l'IA comme de simples hypothèses théoriques.

## 6. Limites et bonnes pratiques

ATLAS est un référentiel de connaissances, pas un scanner qui détecte automatiquement toutes les vulnérabilités d'un système.

Pour l'utiliser efficacement :
- Choisir les techniques pertinentes pour l'architecture étudiée.
- Vérifier les descriptions et identifiants dans la version actuelle du référentiel.
- Adapter les mitigations au contexte réel.
- Tester les contrôles plutôt que de supposer qu'ils fonctionnent.
- Compléter l'analyse avec d'autres référentiels, notamment STRIDE et OWASP pour les LLM.

## 7. À retenir

**STRIDE aide à classer les menaces ; MITRE ATLAS aide à approfondir les techniques d'attaque spécifiques aux systèmes IA.**

Ensemble, ils permettent d'identifier les risques, de mieux comprendre les méthodes employées par les attaquants et de définir des protections adaptées aux données, aux modèles, aux API et aux agents IA.

## Références

- [MITRE ATLAS](https://atlas.mitre.org/)
- [MITRE ATLAS — Techniques](https://atlas.mitre.org/techniques)
- [MITRE ATLAS — Études de cas](https://atlas.mitre.org/studies)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
