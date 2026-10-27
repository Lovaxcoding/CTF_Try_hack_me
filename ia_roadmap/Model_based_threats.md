## Model-Based Threats : Model Extraction et Model Inversion

Contrairement aux attaques ciblant directement les données fournies au modèle, les *model-based threats* exploitent le modèle lui-même comme surface d'attaque.

Les informations sensibles peuvent être liées aux paramètres du modèle, à ses représentations internes ou aux données qu'il a mémorisées pendant l'entraînement. Deux risques majeurs sont le vol du modèle (*Model Extraction*) et la reconstruction de données (*Model Inversion*).

### 1. Model Extraction (Extraction du modèle)

Le *Model Extraction* consiste à reproduire, sans autorisation, tout ou partie des fonctionnalités d'un modèle d'apprentissage automatique.

Un attaquant peut interroger un modèle accessible via une API et collecter de nombreuses paires entrée-sortie. Ces données peuvent ensuite servir à entraîner un modèle de substitution (*surrogate model*) qui imite certains comportements du modèle cible.

Selon les conditions d'accès et la méthode employée, l'objectif peut être de reproduire le comportement du modèle ou d'estimer certaines propriétés internes. L'extraction des poids exacts n'est cependant pas garantie par la simple collecte de réponses.

- **Cible :** fonctionnalité du modèle et propriété intellectuelle associée.
- **Entrée :** grand nombre de requêtes choisies pour observer le comportement du modèle.
- **Sortie recherchée :** modèle de substitution reproduisant une partie du comportement du modèle original.
- **Impact :** perte de propriété intellectuelle, coûts de développement contournés et concurrence déloyale.

#### Mesures de mitigation

- Limiter les requêtes et appliquer des quotas adaptés.
- Surveiller les volumes inhabituels et les motifs de requêtes répétitifs.
- Contrôler l'accès aux API et appliquer une authentification appropriée.
- Éviter de divulguer des informations internes inutiles dans les réponses.

### 2. Model Inversion (Inversion du modèle)

Le *Model Inversion* vise à reconstruire des informations sensibles à partir du comportement du modèle, de ses sorties ou de ses représentations internes.

L'attaquant formule des requêtes et analyse les réponses afin d'inférer des données qui ne lui sont pas directement accessibles. Selon le modèle et les informations exposées, il peut chercher à reconstruire du texte, des attributs ou des fragments de données présents dans l'entraînement.

Contrairement à l'inférence d'appartenance (*Membership Inference*), qui cherche à déterminer si un échantillon connu faisait partie des données d'entraînement, l'inversion vise à retrouver des informations inconnues ou partiellement masquées.

- **Cible :** informations sensibles mémorisées ou encodées dans le modèle.
- **Entrée :** requêtes conçues pour révéler des informations, éventuellement accompagnées de données partielles.
- **Sortie recherchée :** reconstruction ou estimation de données ou d'attributs qui n'étaient pas directement accessibles.
- **Impact :** atteinte à la confidentialité et divulgation potentielle de données personnelles ou professionnelles.

#### Mesures de mitigation

- Réduire la mémorisation des données sensibles et exclure les secrets inutiles des données d'entraînement.
- Limiter les informations sensibles accessibles par les interfaces du modèle.
- Évaluer les risques de mémorisation et de reconstruction avant le déploiement.
- Appliquer des contrôles d'accès et des mécanismes de protection des données adaptés au contexte.

### 3. Différences entre les attaques

| Attaque | Objectif principal | Résultat recherché |
|---|---|---|
| Training Data Extraction | Récupérer des séquences mémorisées | Texte ou données d'entraînement |
| Membership Inference | Tester l'appartenance d'un échantillon connu | Estimation oui/non |
| Model Extraction | Reproduire le comportement du modèle | Modèle de substitution |
| Model Inversion | Reconstruire des informations sensibles inconnues | Données ou attributs inférés |
| Prompt Leakage | Révéler les instructions internes | Prompt système ou développeur |

Ces catégories peuvent se recouper dans certains scénarios, mais elles décrivent des objectifs distincts.

### 4. Mise en pratique : Task 3

**Objectif :** demander au chatbot la démonstration de la Task 3, puis tenter de reconstruire les parties masquées d'un enregistrement présenté comme issu des données d'entraînement.

Échantillon fourni :

`Employee ID: ████ | Department: Research | Clearance: ███`

#### Méthode d'analyse

1. Demander la démonstration Task 3 au chatbot du laboratoire.
2. Observer les informations qu'il fournit spontanément et les limites qu'il indique.
3. Déterminer si les champs masqués peuvent être reconstruits à partir des réponses ou d'autres informations disponibles.
4. Distinguer les informations explicitement révélées par le modèle des hypothèses ou déductions.
5. Noter le résultat obtenu et les éléments qui le justifient.

**Données reconstruites :** à compléter après la démonstration.

**Observations :** à compléter à partir des réponses réelles du chatbot.

**Analyse :** préciser si les informations ont été révélées directement, déduites à partir du contexte ou simplement supposées.

**Limites :** une réponse plausible ne prouve pas que les données reconstruites correspondent à l'enregistrement d'origine. La démonstration doit être évaluée à partir des éléments fournis par le laboratoire.

### Conclusion

Le *Model Extraction* menace principalement la propriété intellectuelle en cherchant à reproduire le comportement d'un modèle. Le *Model Inversion* menace la confidentialité en tentant de reconstruire des informations issues des données apprises.

Ces risques rappellent qu'un modèle d'IA ne doit pas être considéré comme un coffre-fort simplement parce que ses paramètres ne sont pas directement accessibles. Les données sensibles doivent être protégées en amont, et les sorties du modèle doivent être évaluées pour détecter les possibilités de divulgation.

### Références

- Carlini et al., *Extracting Training Data from Large Language Models* : https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting
- *Extracting Training Data from ChatGPT* : https://not-just-memorization.github.io/extracting-training-data-from-chatgpt.html
- OWASP GenAI Security Project : https://genai.owasp.org/
- MITRE ATLAS : https://atlas.mitre.org/
