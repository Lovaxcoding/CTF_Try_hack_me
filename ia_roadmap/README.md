# AI Security Roadmap : Comprendre les surfaces d'attaque des LLM

## Présentation

Cette roadmap rassemble mes notes et apprentissages sur la sécurité des grands modèles de langage (*Large Language Models*, ou LLM).

L'objectif est de comprendre comment les LLM introduisent de nouvelles surfaces d'attaque, comment ces vulnérabilités peuvent être exploitées et quelles mesures permettent de réduire les risques lors de leur intégration dans une application.

L'approche repose sur quatre catégories de menaces : **Data-Based, Model-Based, System-Based et User-Based Threats**.

## Les quatre familles de menaces

### 1. Data-Based Threats

Ces attaques ciblent les données d'entraînement, leur confidentialité ou les informations liées à leur utilisation.

- **Training Data Extraction :** récupérer des séquences potentiellement mémorisées par le modèle.
- **Membership Inference :** estimer si un échantillon connu appartenait aux données d'entraînement.
- **Prompt Leakage :** tenter de révéler les instructions système ou développeur cachées.

**Risque principal :** divulgation de données sensibles ou d'informations internes.

### 2. Model-Based Threats

Ces attaques ciblent le modèle lui-même, notamment sa propriété intellectuelle et les informations qu'il peut avoir mémorisées.

- **Model Extraction :** reproduire le comportement d'un modèle à partir de ses réponses.
- **Model Inversion :** tenter de reconstruire des données ou des attributs sensibles à partir des sorties ou représentations du modèle.

**Risque principal :** vol de propriété intellectuelle et atteinte à la confidentialité des données.

### 3. System-Based Threats

Ces attaques exploitent la manière dont un LLM traite le contexte, les instructions, les ressources et la mémoire conversationnelle.

- **Prompt Injection :** manipuler le contexte pour influencer le comportement du modèle.
- **Context Overflow / Unbounded Consumption :** exploiter les limites de contexte ou provoquer une consommation excessive de ressources.
- **Memory Poisoning :** introduire des informations trompeuses dans une mémoire persistante pour influencer les réponses futures.

**Risque principal :** contournement des contrôles, actions non prévues, dégradation du service ou altération des réponses futures.

### 4. User-Based Threats

Ces attaques exploitent la confiance humaine et utilisent les capacités des LLM pour rendre la manipulation plus convaincante.

- **LLM-Powered Social Engineering :** produire des messages de phishing et des scénarios de fraude personnalisés.
- **Trust Exploitation / Misinformation :** exploiter des réponses incorrectes ou trompeuses auxquelles les utilisateurs accordent trop de confiance.

**Risque principal :** manipulation des utilisateurs, fraude et compromission de systèmes par des décisions humaines mal informées.

## Tableau récapitulatif

| Catégorie | Menaces principales | Objectif de l'attaque |
|---|---|---|
| Data-Based | Training Data Extraction, Membership Inference, Prompt Leakage | Exposer des données ou des instructions sensibles |
| Model-Based | Model Extraction, Model Inversion | Reproduire un modèle ou reconstruire des informations |
| System-Based | Prompt Injection, Context Overflow, Memory Poisoning | Manipuler le comportement, les ressources ou la mémoire |
| User-Based | Social Engineering, Trust Exploitation | Influencer les décisions et les actions humaines |

## Principes fondamentaux d'un audit de sécurité IA

### Défense en profondeur

Ne pas dépendre d'un seul mécanisme de sécurité. Combiner les contrôles d'accès, la validation des entrées et sorties, la surveillance et les protections au niveau de l'application.

### Principe du moindre privilège

Un assistant IA ne doit disposer que des outils, données et autorisations strictement nécessaires à sa fonction.

### Validation indépendante

Les autorisations et les opérations sensibles doivent être contrôlées par l'application, et non reposer uniquement sur les instructions données au modèle.

### Protection des données

Éviter d'exposer des secrets dans les prompts, limiter l'accès aux données confidentielles et appliquer des règles de conservation et de filtrage adaptées.

### Surveillance et limitation des ressources

Contrôler les volumes de requêtes, la consommation de tokens, les coûts, les erreurs et les comportements inhabituels.

### Vérification des résultats

Une réponse convaincante n'est pas nécessairement exacte. Vérifier les recommandations, les dépendances logicielles, les commandes et les informations sensibles avant de les utiliser.

## Notes d'apprentissage

| Fichier | Sujet |
|---|---|
| `notes.md` | Fondamentaux et architecture de sécurité des systèmes IA |
| `owasp_top_10.md` | Risques liés aux LLM et classification OWASP |
| `defense_in_depth_ia.md` | Défense en profondeur, moindre privilège et contrôles de sécurité |
| `audit_trial.md` | Questions d'audit et observations du laboratoire |
| `system_based_threats.md` | Prompt injection, context overflow et memory poisoning |
| `user_based_threats.md` | Ingénierie sociale et exploitation de la confiance |

## Conclusion

La sécurité des LLM ne se limite pas à protéger un modèle ou à empêcher quelques prompts malveillants. Elle nécessite d'évaluer l'ensemble de l'écosystème : données, modèle, application, outils connectés, ressources et utilisateurs.

La leçon principale est simple : **un LLM ne doit jamais constituer à lui seul une frontière de sécurité**. Les autorisations, la validation, la protection des données et la surveillance doivent être assurées par des mécanismes indépendants et vérifiables.

Ces notes constituent une base de révision et un support pratique pour identifier les risques, analyser les comportements observés en laboratoire et mieux comprendre la sécurité des systèmes d'intelligence artificielle.

### Références

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

**Parcours :** TryHackMe — AI Security  
**Objectif :** comprendre les mécanismes d'attaque, identifier les risques et apprendre à raisonner comme un auditeur de sécurité IA.
