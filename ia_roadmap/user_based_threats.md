# User-Based Threats : Social Engineering et Trust Exploitation

## Introduction

La sécurité des LLM ne concerne pas uniquement les modèles, leurs données ou leur intégration dans un système. Elle concerne également les personnes qui interagissent avec eux.

Les modèles de langage peuvent produire des textes convaincants, imiter différents styles de communication et exploiter des informations contextuelles pour influencer les décisions humaines. Ces capacités peuvent être détournées pour améliorer des attaques de phishing, faciliter des fraudes ou encourager des utilisateurs à faire confiance à des informations incorrectes.

Deux menaces importantes sont étudiées ici :

- LLM-Powered Social Engineering
- Trust Exploitation (LLM09:2025, Misinformation)

## 1. LLM-Powered Social Engineering

L'ingénierie sociale consiste à manipuler une personne afin de l'inciter à divulguer des informations, à effectuer une action ou à contourner une procédure de sécurité.

Les LLM peuvent renforcer ces attaques en générant des messages personnalisés, crédibles et adaptés au contexte de la victime.

### Comment l'IA renforce-t-elle l'ingénierie sociale ?

Traditionnellement, les messages frauduleux pouvaient contenir des fautes d'orthographe, des formulations maladroites ou des signes d'urgence faciles à repérer.

Les LLM permettent de produire des messages plus naturels et d'adapter leur ton à une situation professionnelle ou personnelle. Les attaquants peuvent notamment exploiter :

- **L'OSINT :** informations publiquement accessibles sur une personne ou une organisation.
- **L'usurpation d'identité :** imitation du style ou du rôle d'un collègue, d'un responsable ou d'un prestataire.
- **La personnalisation :** utilisation d'informations sur un projet, une fonction ou une relation professionnelle.
- **L'automatisation :** génération rapide de nombreuses variantes de messages frauduleux.

Une attaque peut devenir particulièrement crédible lorsque l'attaquant combine des informations publiques avec des données internes divulguées par un système d'IA compromis.

### Exemple de scénario

Un attaquant rassemble des informations publiques sur un responsable informatique et découvre qu'une entreprise travaille sur un nouveau projet.

Il utilise ensuite un LLM pour rédiger un message imitant le ton d'un collègue et faisant référence au projet. Le message demande à son destinataire de consulter un document ou de communiquer des informations confidentielles.

Le message peut sembler légitime même s'il provient d'un attaquant.

### En résumé

- **Cible :** jugement humain et processus de prise de décision.
- **Entrée :** informations personnelles, professionnelles ou contextuelles.
- **Résultat recherché :** manipulation d'un utilisateur, divulgation d'informations ou exécution d'une action non autorisée.
- **Risques :** phishing, fraude, compromission de comptes et fuite de données.

### Mesures de défense

- Vérifier l'identité de l'expéditeur par un canal indépendant.
- Confirmer toute demande sensible par une procédure officielle.
- Ne pas se fier uniquement à la qualité rédactionnelle d'un message.
- Utiliser l'authentification multifacteur et des contrôles d'accès adaptés.
- Sensibiliser les employés aux attaques personnalisées et assistées par l'IA.
- Limiter les données internes accessibles aux assistants d'IA et contrôler leur éventuelle divulgation.

**Point essentiel :** un message grammaticalement parfait n'est pas une preuve de légitimité.

## 2. Trust Exploitation (LLM09:2025, Misinformation)

La *Trust Exploitation* consiste à tirer parti de la confiance excessive accordée aux réponses d'un système d'IA.

Les LLM peuvent produire des réponses fluides, détaillées et formulées avec assurance, même lorsque certaines informations sont fausses. Ces erreurs, souvent appelées *hallucinations*, peuvent devenir dangereuses lorsque les utilisateurs prennent des décisions sans vérifier les résultats.

Un attaquant peut exploiter ce phénomène en encourageant l'utilisation d'informations incorrectes ou en tirant parti des erreurs prévisibles d'un modèle.

### Exemple : Package Hallucination

Un développeur demande à un assistant IA de recommander une bibliothèque logicielle pour sécuriser une application.

Le modèle recommande un paquet qui n'existe pas, par exemple `secure-utils-xtools`.

Le développeur suppose que la recommandation est fiable et recherche le paquet dans un registre public. Un attaquant qui a anticipé cette erreur peut avoir publié un paquet malveillant portant ce nom.

Si le développeur installe ce paquet sans vérifier son origine et sa légitimité, il risque d'introduire du code malveillant dans son projet.

Ce scénario illustre comment une hallucination peut être transformée en vecteur d'attaque de la chaîne d'approvisionnement logicielle (*software supply chain*).

### En résumé

- **Cible :** confiance et capacité de jugement de l'utilisateur.
- **Entrée :** recommandations erronées, informations trompeuses ou contenu malveillant.
- **Résultat recherché :** acceptation d'une information fausse ou exécution d'une action dangereuse.
- **Risques :** installation de logiciels malveillants, décisions incorrectes et compromission d'un environnement informatique.

### Mesures de défense

- Vérifier l'existence et l'origine des paquets recommandés par une IA.
- Consulter les registres officiels, la documentation et les dépôts des projets.
- Examiner le nom, le mainteneur, les versions et l'historique d'un paquet avant installation.
- Utiliser des fichiers de verrouillage des dépendances et des outils d'analyse de sécurité.
- Ne jamais exécuter une commande ou un script uniquement parce qu'un LLM le recommande.
- Traiter les réponses du modèle comme des hypothèses à vérifier, et non comme des preuves.

**Point essentiel :** la confiance doit dépendre de la vérification des faits, pas de l'assurance avec laquelle ils sont présentés.

## 3. Comparaison des menaces

| Menace | Mécanisme exploité | Objectif de l'attaque | Exemple |
|---|---|---|---|
| LLM-Powered Social Engineering | Manipulation psychologique et personnalisation | Faire agir la victime | E-mail de phishing imitant un collègue |
| Trust Exploitation | Confiance excessive dans les réponses de l'IA | Faire accepter une information fausse ou dangereuse | Installation d'un paquet inexistant recommandé par un LLM |

Ces menaces peuvent se combiner. Un attaquant peut, par exemple, utiliser un LLM pour rédiger un message de phishing qui recommande ensuite l'installation d'un paquet malveillant.

## 4. Bonnes pratiques pour les utilisateurs et les développeurs

### Pour les utilisateurs

- Vérifier les demandes sensibles par un canal indépendant.
- Confirmer les informations importantes auprès de sources fiables.
- Se méfier des demandes inhabituelles, même lorsqu'elles semblent provenir d'une personne connue.
- Éviter de transmettre des informations confidentielles à des assistants non autorisés.

### Pour les développeurs

- Vérifier chaque dépendance suggérée par une IA avant de l'installer.
- Examiner les commandes et le code générés avant exécution.
- Utiliser des environnements isolés pour tester du code non fiable.
- Appliquer des contrôles de sécurité automatisés à la chaîne d'approvisionnement logicielle.
- Documenter les décisions techniques importantes et leurs sources de validation.

## Conclusion

Les LLM changent la manière dont les attaques peuvent cibler les personnes. Ils permettent de produire des messages frauduleux plus crédibles et peuvent renforcer des erreurs de jugement lorsque leurs réponses sont acceptées sans vérification.

La défense repose sur deux principes complémentaires : vérifier l'identité et la légitimité des demandes humaines, puis vérifier l'exactitude et la sécurité des recommandations produites par l'IA.

Un LLM peut être un excellent assistant, mais il ne remplace ni la vérification des faits ni les contrôles de sécurité.

### Références

- OWASP GenAI Security Project : https://genai.owasp.org/
- MITRE ATLAS : https://atlas.mitre.org/
