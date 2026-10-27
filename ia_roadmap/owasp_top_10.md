# Référentiels de sécurité de l'IA : OWASP, MITRE ATLAS et NIST

## 1. OWASP LLM Top 10 (2025)

L'**OWASP Top 10 for LLM Applications (2025)** classe dix catégories de risques majeurs liés aux applications utilisant des grands modèles de langage (LLM).

Cinq catégories sont particulièrement importantes lors d'une revue de sécurité de l'architecture avant le déploiement : elles découlent principalement de la conception du système, de ses intégrations et des permissions accordées à ses composants.

| ID | Catégorie | Description | Module associé selon la room |
|---|---|---|---|
| **LLM01** | Prompt Injection | Manipulation du comportement du LLM à l'aide d'entrées spécialement conçues. | Prompt Security |
| **LLM02** | Sensitive Information Disclosure | Divulgation de données confidentielles, de données personnelles ou d'informations internes. | Cette room et Data Poisoning |
| **LLM03** | Supply Chain | Compromission des modèles préentraînés, des jeux de données ou des dépendances tierces. | AI Supply Chain Security |
| **LLM04** | Data and Model Poisoning | Altération des données d'entraînement ou des poids du modèle pour modifier son comportement. | Data Poisoning |
| **LLM05** | Improper Output Handling | Traitement insuffisamment sécurisé des sorties du LLM par les systèmes en aval. | Cette room |
| **LLM06** | Excessive Agency | Attribution de privilèges ou d'un niveau d'autonomie excessifs aux composants d'IA. | Cette room |
| **LLM07** | System Prompt Leakage | Divulgation des instructions système ou de la configuration interne. | Cette room |
| **LLM08** | Vector and Embedding Weaknesses | Exploitation des faiblesses des mécanismes de récupération et des pipelines d'embeddings. | Data Poisoning |
| **LLM09** | Misinformation | Génération de contenus faux ou trompeurs par le modèle. | LLM Security |
| **LLM10** | Unbounded Consumption | Épuisement des ressources, augmentation incontrôlée des coûts ou déni de service. | Cette room |

**Référence officielle :** https://genai.owasp.org/llm-top-10/

### Les cinq catégories étudiées dans cette room

#### LLM02 - Sensitive Information Disclosure

Le système révèle des informations qui devraient rester confidentielles.

Exemples :
- Divulgation de données personnelles.
- Exposition de secrets présents dans le contexte du modèle.
- Révélation d'informations internes à travers les réponses.

Mesures de protection :
- Limiter les données sensibles transmises au modèle.
- Appliquer des contrôles d'accès aux données.
- Filtrer les informations confidentielles dans les réponses.
- Surveiller les tentatives d'extraction de données.

#### LLM05 - Improper Output Handling

Les sorties du LLM sont utilisées par un autre composant sans validation ou neutralisation suffisante.

Exemples :
- Insertion de contenu généré dans une page web sans échappement HTML approprié.
- Transmission d'une sortie non fiable à une commande système.
- Utilisation du texte généré dans une requête SQL construite de manière dangereuse.

Mesures de protection :
- Traiter les sorties du modèle comme des données non fiables.
- Valider les données selon le contexte d'utilisation.
- Utiliser des requêtes paramétrées et des mécanismes d'échappement adaptés.
- Éviter l'exécution directe de commandes générées par le modèle.

#### LLM06 - Excessive Agency

Le système accorde au modèle trop de privilèges ou trop de liberté d'action.

Exemples :
- Un agent peut modifier des fichiers alors qu'il devrait uniquement les lire.
- Un assistant peut exécuter des actions sensibles sans confirmation.
- Un outil dispose de droits administratifs inutiles à sa fonction.

Mesures de protection :
- Appliquer le principe du moindre privilège.
- Limiter les outils et les actions accessibles.
- Vérifier les autorisations indépendamment du LLM.
- Exiger une approbation humaine pour les opérations sensibles lorsque cela est nécessaire.

#### LLM07 - System Prompt Leakage

Le système divulgue ses instructions internes ou des détails de configuration.

Exemples :
- Une réponse révèle les instructions système.
- Le modèle expose des détails internes intégrés à son contexte.
- Des informations confidentielles sont placées directement dans le prompt.

Mesures de protection :
- Ne pas utiliser le prompt système comme mécanisme de contrôle d'accès.
- Éviter d'y intégrer des secrets.
- Appliquer des autorisations côté serveur.
- Limiter les informations internes accessibles au modèle.

**À retenir :** un prompt système n'est pas un coffre-fort. Même s'il est conçu pour rester caché, il ne faut pas compter sur son secret pour protéger des données sensibles.

#### LLM10 - Unbounded Consumption

Le système permet une consommation excessive de ressources, volontaire ou accidentelle.

Exemples :
- Requêtes très longues ou répétées.
- Conversations consommant trop de tokens.
- Appels d'outils en boucle.
- Augmentation incontrôlée des coûts d'utilisation d'une API.

Mesures de protection :
- Limiter la taille des entrées et des sorties.
- Fixer des quotas et des limites de débit.
- Définir des budgets de tokens et de calcul.
- Limiter le nombre d'appels d'outils et la durée des opérations.
- Détecter les comportements anormaux.

---

## 2. MITRE ATLAS

**MITRE ATLAS** signifie *Adversarial Threat Landscape for Artificial-Intelligence Systems*.

Il s'agit d'une base de connaissances consacrée aux tactiques, techniques et études de cas portant sur les attaques contre les systèmes d'intelligence artificielle.

ATLAS est conçu comme un complément à **MITRE ATT&CK**, qui se concentre plus largement sur les systèmes informatiques.

### Différence entre OWASP et MITRE ATLAS

| Référentiel | Question principale | Utilité |
|---|---|---|
| **OWASP LLM Top 10** | Quels sont les principaux risques de sécurité des applications LLM ? | Identifier et classer les catégories de vulnérabilités. |
| **MITRE ATLAS** | Comment les adversaires attaquent-ils les systèmes d'IA ? | Étudier les tactiques, les techniques et les scénarios d'attaque. |

### Progression possible d'une attaque contre un système d'IA

Le parcours suivant est un modèle conceptuel simplifié, et non une séquence obligatoire pour toutes les attaques.

1. **Reconnaissance :** recueillir des informations sur le modèle, les interfaces et les composants exposés.
2. **Accès initial :** atteindre le système par une interface ou exploiter un composant compromis.
3. **Exécution :** déclencher un comportement malveillant à l'aide d'entrées adversariales ou de techniques de prompt injection.
4. **Persistance :** maintenir un accès ou un comportement malveillant, par exemple au moyen d'un modèle compromis.
5. **Impact :** provoquer une fuite de données, perturber le service ou manipuler les résultats du modèle.

Pour TryAssist, l'analyse porte particulièrement sur la manière dont une requête malveillante reçue par l'interface de chat peut traverser les composants du système et produire un impact réel.

ATLAS répertorie de nombreuses techniques et tactiques, accompagnées d'exemples et d'études de cas. Sa base évolue à mesure que de nouvelles techniques d'attaque sont documentées.

**Référence officielle :** https://atlas.mitre.org/

---

## 3. NIST AI Risk Management Framework (AI RMF)

Le **NIST AI RMF** est un cadre de gestion des risques liés à l'intelligence artificielle. Contrairement à OWASP et à MITRE ATLAS, il adopte une approche organisationnelle : il aide les organisations à identifier, évaluer, gérer et surveiller les risques associés à leurs systèmes d'IA.

Il repose sur quatre fonctions principales.

| Fonction | Signification | Objectif |
|---|---|---|
| **Govern** | Gouverner | Définir les politiques, les responsabilités et les mécanismes de supervision. |
| **Map** | Cartographier | Identifier les systèmes d'IA, leur contexte d'utilisation et leurs risques potentiels. |
| **Measure** | Mesurer | Évaluer et surveiller les risques à l'aide de méthodes et de critères adaptés. |
| **Manage** | Gérer | Prioriser les risques et mettre en œuvre des mesures de traitement et d'atténuation. |

### Exemple d'application à TryAssist

- **Govern :** définir qui est responsable de la sécurité de l'assistant et de ses outils.
- **Map :** identifier les données sensibles, les composants, les utilisateurs et les frontières de confiance.
- **Measure :** tester les risques de fuite de données, d'utilisation abusive des outils et de consommation excessive.
- **Manage :** réduire les permissions, renforcer les contrôles et surveiller les comportements suspects.

### NIST AI 100-2

Le document **NIST AI 100-2**, publié en janvier 2025 selon le contenu de la room, présente une taxonomie technique des attaques adversariales contre le machine learning et des mesures d'atténuation associées.

Il complète le cadre de gestion des risques par une approche plus technique des attaques visant les modèles et leurs différentes phases de cycle de vie.

**Références :**
- NIST AI RMF : https://www.nist.gov/itl/ai-risk-management-framework
- Publications NIST sur l'IA : https://www.nist.gov/artificial-intelligence

---

## 4. Combiner les référentiels

Ces trois approches sont complémentaires.

| Étape | Référentiel | Application |
|---|---|---|
| Identifier les risques | OWASP LLM Top 10 | Classer les vulnérabilités possibles de TryAssist. |
| Comprendre les attaques | MITRE ATLAS | Relier les risques à des tactiques et techniques adversariales. |
| Organiser la gestion des risques | NIST AI RMF | Définir les responsabilités, évaluer les risques et suivre les mesures de protection. |

### Exemple : un agent IA disposant de trop de privilèges

1. **OWASP :** classer le problème dans LLM06, Excessive Agency.
2. **MITRE ATLAS :** rechercher les techniques pertinentes selon le scénario d'attaque étudié.
3. **NIST AI RMF :** évaluer l'impact, attribuer les responsabilités et mettre en œuvre des mesures correctives.

---

## 5. Lien avec STRIDE et PASTA

La room TryHackMe consacrée à la modélisation des menaces liées à l'IA aborde également l'utilisation de STRIDE et PASTA.

- **STRIDE :** méthode de classification des menaces selon six catégories : usurpation d'identité, altération, répudiation, divulgation d'informations, déni de service et élévation de privilèges.
- **PASTA :** méthode structurée d'analyse des menaces qui relie les objectifs métier, les composants techniques, les scénarios d'attaque et les risques.

Ces méthodes peuvent compléter les référentiels spécialisés en IA lors d'une revue d'architecture.

---

## 6. Cheatsheet : l'essentiel à mémoriser

| Question | Réponse |
|---|---|
| Quel référentiel classe les risques des applications LLM ? | OWASP LLM Top 10 |
| Quel référentiel décrit les tactiques et techniques d'attaque contre l'IA ? | MITRE ATLAS |
| Quel cadre aide les organisations à gérer les risques liés à l'IA ? | NIST AI RMF |
| Que signifie LLM05 ? | Improper Output Handling |
| Que signifie LLM06 ? | Excessive Agency |
| Que signifie LLM07 ? | System Prompt Leakage |
| Que signifie LLM10 ? | Unbounded Consumption |
| Quelles sont les quatre fonctions du NIST AI RMF ? | Govern, Map, Measure, Manage |
| Quel est le principe clé pour les outils d'un agent IA ? | Le moindre privilège |
| Le prompt système protège-t-il à lui seul les secrets ? | Non. Les secrets doivent être protégés par des contrôles d'accès indépendants. |

## Conclusion

La sécurité d'une application d'IA ne dépend pas uniquement du modèle utilisé. Elle dépend également de son architecture, des données auxquelles il accède, des outils qu'il peut appeler et des contrôles qui encadrent ses actions.

**À retenir : OWASP identifie les risques, MITRE ATLAS aide à comprendre les attaques et NIST AI RMF structure la gestion des risques.**
