# System-Based Threats Against LLMs

Les *system-based threats* ciblent la manière dont un modèle de langage traite le contexte, les instructions et les informations persistantes d'une application.

Contrairement aux attaques visant directement les données d'entraînement ou les paramètres du modèle, ces attaques exploitent principalement son intégration dans un système : gestion du contexte, hiérarchie des instructions, consommation des ressources et mémoire conversationnelle.

Trois menaces importantes sont étudiées ici :

- Prompt Injection
- Context Overflow, associé à l'Unbounded Consumption
- Memory Poisoning

## 1. Prompt Injection

La *prompt injection* consiste à manipuler les entrées d'un modèle pour influencer son comportement et l'amener à s'écarter de l'objectif ou des règles définis par les développeurs.

Un LLM peut recevoir plusieurs types de contenu dans son contexte : instructions système, messages utilisateur, documents récupérés, résultats d'outils et historique de conversation. Le contenu non fiable peut contenir des instructions malveillantes qui tentent de prendre le dessus sur les consignes prévues par l'application.

Par exemple, un assistant bancaire peut recevoir un document contenant des instructions destinées non pas à informer l'assistant, mais à le manipuler pour qu'il ignore ses règles.

La difficulté vient du fait que le modèle traite ces contenus au sein d'un même processus de génération. Il ne dispose pas, à lui seul, d'une frontière de sécurité fiable qui garantit que chaque instruction non fiable sera ignorée.

### En résumé

- **Cible :** contexte du LLM et hiérarchie des instructions.
- **Entrée :** texte contrôlé par un utilisateur ou contenu externe récupéré par l'application.
- **Résultat recherché :** modification du comportement, contournement de règles ou exécution d'actions non prévues.
- **Risque :** divulgation d'informations ou utilisation abusive des fonctionnalités et outils accessibles au modèle.

### Mesures de défense

- Traiter les messages utilisateur et les documents externes comme des données non fiables.
- Séparer les instructions des données dans l'architecture applicative autant que possible.
- Valider les actions sensibles en dehors du modèle.
- Appliquer des contrôles d'autorisation indépendants des réponses du LLM.
- Tester les entrées directes et indirectes susceptibles de contenir des instructions malveillantes.

**Point essentiel :** un prompt système ne constitue pas, à lui seul, un mécanisme de contrôle d'accès.

## 2. Context Overflow (LLM10:2025, Unbounded Consumption)

Une fenêtre de contexte représente la quantité de tokens qu'un modèle peut traiter dans une requête, en tenant compte des contraintes propres à son architecture et à son implémentation.

Elle peut contenir les instructions, l'historique, les documents récupérés et la réponse générée. Lorsque le volume de contenu devient excessif, le système peut atteindre ses limites de contexte ou de ressources.

Une attaque par *context overflow* cherche à exploiter ces limites en soumettant de très grandes quantités de contenu. Selon l'implémentation, cela peut provoquer une troncature, une dégradation des réponses, une augmentation des coûts ou une indisponibilité du service.

Il faut toutefois éviter une simplification : les modèles ne suppriment pas tous automatiquement les premiers tokens selon une stratégie FIFO. Le comportement dépend de l'application, de la gestion de l'historique et des mécanismes de troncature utilisés.

### En résumé

- **Cible :** fenêtre de contexte, ressources de calcul et budget de consommation.
- **Entrée :** prompts, historiques ou documents excessivement volumineux.
- **Résultat recherché :** dépassement des limites, dégradation du service ou consommation excessive.
- **Risques :** ralentissement, déni de service et hausse des dépenses d'inférence.

### Denial of Wallet

Le *Denial of Wallet* désigne une attaque qui exploite la facturation à l'usage pour générer des coûts anormalement élevés.

Un attaquant peut, par exemple, multiplier les requêtes volumineuses sur une API d'IA. Si les contrôles sont insuffisants, le coût de traitement peut augmenter rapidement, même sans compromettre directement les données.

### Mesures de défense

- Définir des limites de tokens en entrée et en sortie.
- Appliquer des quotas et une limitation du débit par utilisateur.
- Limiter la taille des documents et la quantité d'historique conservée.
- Surveiller les coûts, la latence et les volumes de requêtes.
- Configurer des alertes budgétaires et des mécanismes d'arrêt adaptés.
- Prévoir une gestion explicite des erreurs lorsque les limites sont dépassées.

## 3. Memory Poisoning

Le *memory poisoning* consiste à introduire des informations fausses ou malveillantes dans une mémoire conversationnelle persistante afin d'influencer les réponses ultérieures du modèle.

Contrairement à une prompt injection ponctuelle, cette attaque peut se dérouler sur plusieurs interactions. Le système peut conserver des affirmations fournies par l'utilisateur dans son historique ou dans une mémoire réutilisée par la suite.

### Exemple pédagogique

Un utilisateur affirme que le mot « chat » signifie désormais « chien ». Si l'assistant accepte cette affirmation comme une règle générale et la réutilise sans tenir compte du contexte, il risque de produire des réponses incorrectes.

L'objectif de l'exemple est de montrer qu'une information persistante peut influencer des réponses futures, même lorsque cette information est fausse.

### En résumé

- **Cible :** mémoire conversationnelle ou état persistant de l'application.
- **Entrée :** affirmations trompeuses destinées à être conservées et réutilisées.
- **Résultat recherché :** altération durable du comportement ou des réponses.
- **Risques :** désinformation persistante, décisions erronées et perte de confiance dans l'assistant.

### Mesures de défense

- Ne pas enregistrer automatiquement toute affirmation utilisateur comme un fait fiable.
- Distinguer les préférences utilisateur des faits vérifiés.
- Contrôler les informations qui sont enregistrées dans la mémoire persistante.
- Permettre la correction et la suppression des données mémorisées.
- Réévaluer la fiabilité et la pertinence d'un souvenir avant de le réutiliser.
- Empêcher qu'une information mémorisée puisse modifier les autorisations de sécurité du système.

## 4. Comparaison des trois menaces

| Menace | Surface d'attaque | Objectif | Effet potentiel |
|---|---|---|---|
| Prompt Injection | Contexte et instructions | Influencer le comportement du modèle | Contournement de règles ou actions non prévues |
| Context Overflow | Fenêtre de contexte et ressources | Exploiter les limites de traitement | Troncature, ralentissement, coûts excessifs |
| Memory Poisoning | Mémoire persistante | Corrompre les informations réutilisées | Réponses futures incorrectes |

La différence principale réside dans la durée et le mécanisme de l'attaque : la prompt injection manipule le contexte courant, le context overflow exploite les limites de capacité, tandis que le memory poisoning cherche à influencer les interactions futures.

## 5. Mise en pratique : Task 4

**Objectif :** demander au chatbot la démonstration Task 4, puis observer si une affirmation répétée ou enregistrée dans le contexte peut influencer ses réponses ultérieures.

Le scénario du laboratoire demande de convaincre le modèle qu'un chat est un chien.

### Démarche d'analyse

1. Demander la démonstration Task 4 au chatbot.
2. Observer comment il réagit à l'affirmation initiale.
3. Vérifier si le modèle reprend cette affirmation dans une réponse ultérieure.
4. Distinguer une simple acceptation dans le cadre d'un jeu de rôle d'une modification persistante de son comportement.
5. Consigner les résultats réellement observés.

### Résultats

- **Comportement initial :** à compléter.
- **Réponse après l'affirmation :** à compléter.
- **Réponse lors d'une interaction ultérieure :** à compléter.
- **Persistance observée :** à compléter.
- **Analyse :** déterminer si le comportement observé relève d'une simple adaptation au contexte ou d'une véritable mémoire persistante.

### Conclusion de la pratique

Cette démonstration illustre comment une affirmation non vérifiée peut influencer les réponses d'un LLM. Cependant, accepter temporairement une prémisse dans une conversation ne prouve pas nécessairement qu'une mémoire persistante a été empoisonnée.

Pour confirmer un *memory poisoning*, il faut observer que l'information est conservée et réutilisée dans un contexte ultérieur où elle ne devrait pas être considérée comme vraie.

## Conclusion générale

Les menaces au niveau du système rappellent que la sécurité d'une application d'IA ne dépend pas uniquement du modèle. La gestion des instructions, les limites de ressources et la fiabilité de la mémoire sont tout aussi importantes.

Une architecture robuste doit traiter les entrées comme potentiellement hostiles, contrôler les ressources consommées et empêcher les informations non vérifiées de devenir des faits persistants. Les contrôles de sécurité doivent être appliqués par le système lui-même, et non reposer uniquement sur la capacité du modèle à suivre ses instructions.

### Références

- OWASP GenAI Security Project : https://genai.owasp.org/
- AWS Security Blog, Context Window Overflow : https://aws.amazon.com/blogs/security/context-window-overflow-breaking-the-barrier/
- MITRE ATLAS : https://atlas.mitre.org/
