## Training Data Extraction, Membership Inference et Prompt Leakage

### 1. Training Data Extraction (Extraction des données d'entraînement)

L'extraction des données d'entraînement consiste à interroger un modèle de langage afin de récupérer des séquences de texte mémorisées pendant son entraînement.

Un attaquant peut concevoir des prompts destinés à faire reproduire au modèle des informations confidentielles, telles que des adresses e-mail, des fragments de documents ou des secrets qui auraient été présents dans les données d'entraînement.

Les résultats suspects doivent ensuite être examinés et vérifiés. Une réponse plausible ne prouve pas, à elle seule, que le contenu provient réellement des données d'entraînement.

- **Cible :** confidentialité du jeu de données d'entraînement.
- **Entrée :** prompts conçus pour faire émerger des informations mémorisées.
- **Sortie recherchée :** données reproduites intégralement ou partiellement, éventuellement sensibles.
- **Risque :** divulgation de données personnelles ou confidentielles.

**Point important :** une extraction réussie ne signifie pas nécessairement que le modèle mémorise toutes ses données d'entraînement. Le risque dépend notamment des données utilisées, du comportement du modèle et de son exposition aux requêtes.

### 2. Membership Inference (Inférence d'appartenance)

L'inférence d'appartenance cherche à déterminer si un échantillon précis a été utilisé pendant l'entraînement d'un modèle.

Contrairement à l'extraction, l'attaquant possède déjà l'échantillon candidat. Il cherche à estimer si cet échantillon appartenait au jeu de données d'entraînement, en étudiant la réponse du modèle ou des indicateurs statistiques accessibles.

Par exemple, un attaquant peut comparer le comportement du modèle face à un échantillon connu et à d'autres données. Une confiance anormalement élevée ou une perte plus faible peut constituer un indice, mais ne prouve pas à elle seule l'appartenance.

- **Cible :** appartenance d'un échantillon au jeu de données d'entraînement.
- **Entrée :** échantillon candidat déjà connu de l'attaquant.
- **Sortie recherchée :** estimation de la probabilité que cet échantillon ait été utilisé pour l'entraînement.
- **Risque :** révélation indirecte d'informations privées sur les personnes représentées dans les données.

#### Différence essentielle

| Critère | Training Data Extraction | Membership Inference |
|---|---|---|
| Question | Quelles données le modèle peut-il reproduire ? | Cet échantillon était-il dans les données d'entraînement ? |
| Donnée initiale | L'attaquant cherche à récupérer du contenu | L'attaquant possède déjà l'échantillon candidat |
| Résultat | Texte ou données récupérés | Estimation d'appartenance |
| Risque principal | Divulgation du contenu | Divulgation d'une information sur la présence d'un échantillon |

### 3. Prompt Leakage (LLM07:2025)

Le *prompt leakage* désigne la divulgation d'instructions internes, notamment les prompts système ou développeur, normalement invisibles à l'utilisateur.

Un attaquant peut essayer d'amener le modèle à révéler ou à résumer ses instructions cachées. Ces informations peuvent exposer la logique métier de l'application, certaines règles internes ou des mécanismes de sécurité.

La divulgation d'un prompt ne constitue pas automatiquement une compromission complète du système. Elle peut toutefois aider un attaquant à mieux comprendre son fonctionnement et à concevoir des attaques plus ciblées.

- **Cible :** instructions système et développeur.
- **Entrée :** prompts demandant au modèle de révéler ou de résumer ses instructions internes.
- **Sortie recherchée :** divulgation partielle ou complète des instructions cachées.
- **Risques :** exposition de logique propriétaire et facilitation d'attaques ultérieures.

#### Mesures de mitigation

- Ne jamais considérer le prompt système comme une frontière de sécurité.
- Ne pas y placer de mots de passe, clés API, jetons ou autres secrets actifs.
- Appliquer les contrôles d'accès et les autorisations dans le système applicatif, indépendamment des instructions du modèle.
- Tester régulièrement la résistance aux tentatives de divulgation et de contournement des instructions.

### 4. Mise en pratique : Task 2

**Objectif :** demander au chatbot la démonstration de la Task 2, puis utiliser une attaque par inférence d'appartenance pour déterminer lequel des trois échantillons proposés appartient au jeu de données d'entraînement.

#### Méthode d'analyse

1. Lire les trois échantillons candidats fournis par le laboratoire.
2. Identifier les informations que le chatbot permet réellement d'observer.
3. Examiner le comportement du modèle pour chaque échantillon, sans confondre une réponse convaincante avec une preuve.
4. Comparer les indices disponibles et déterminer quel échantillon est le plus susceptible d'avoir été utilisé pendant l'entraînement.
5. Consigner le résultat et les éléments qui le justifient.

**Résultat observé :** à compléter après la démonstration.

**Échantillon identifié :** à compléter après l'analyse des trois candidats.

**Justification :** à compléter à partir des observations réelles du laboratoire.

**Limite :** sans accès à des indicateurs fiables ou à une méthode d'évaluation adaptée, le comportement du chatbot peut fournir des indices insuffisants pour conclure avec certitude.

### 5. Références

- Carlini et al., *Extracting Training Data from Large Language Models* : https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting
- OWASP GenAI Security Project, *LLM Top 10* : https://genai.owasp.org/
- MITRE ATLAS : https://atlas.mitre.org/

### Conclusion

Ces trois attaques ciblent des informations différentes : l'extraction vise le contenu mémorisé, l'inférence d'appartenance cherche à déterminer si un échantillon a participé à l'entraînement, et le prompt leakage vise les instructions internes de l'application.

Pour un audit, il est essentiel de distinguer les observations, les hypothèses et les conclusions vérifiées. Un modèle qui répond avec assurance n'est pas nécessairement un modèle qui fournit une preuve.
