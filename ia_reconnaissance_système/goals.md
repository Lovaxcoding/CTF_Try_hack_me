# AI Reconnaissance – Objectifs et plan d'apprentissage

## 1. Présentation

La **reconnaissance d'infrastructures IA** consiste à identifier les composants d'intelligence artificielle présents sur un réseau, à déterminer leur nature et à examiner les informations qu'ils exposent.

Lorsqu'une organisation ajoute des fonctionnalités IA à son infrastructure, elle peut déployer de nouveaux services : serveurs d'inférence, registres de modèles, plateformes de suivi des expériences, notebooks, bases vectorielles et endpoints de métriques.

Ces composants peuvent utiliser des ports, des API et des formats de réponse qui ne sont pas toujours identifiés par les méthodes de reconnaissance traditionnelles.

L'objectif est de découvrir ces services, de les identifier et de comprendre leur exposition, sans perturber leur fonctionnement.

## 2. Pourquoi cette reconnaissance est importante

Les infrastructures IA peuvent introduire de nouveaux risques :

- **Services exposés :** interfaces accessibles depuis des réseaux qui ne devraient pas y avoir accès.
- **Authentification insuffisante :** endpoints permettant de consulter des informations sans contrôle d'accès adapté.
- **Fuite de métadonnées :** noms de modèles, versions, expériences, paramètres ou configurations de déploiement.
- **Exposition de données sensibles :** informations internes ou secrets accessibles par des API mal protégées.
- **Dépendances internes :** communication entre les serveurs d'inférence, les bases de données, le stockage et les autres services.
- **Surveillance insuffisante :** activités de reconnaissance qui ne sont pas correctement détectées ou journalisées.

La présence d'un service exposé ne prouve pas automatiquement qu'il est vulnérable. Il faut examiner les accès autorisés, les données retournées et les protections réellement en place.

## 3. Scénario : Cyphira

Cyphira est une entreprise fintech de taille moyenne qui a déployé plusieurs fonctionnalités basées sur l'IA sans revue de sécurité préalable.

En tant qu'ingénieur sécurité, la mission consiste à répondre aux questions suivantes :

1. Quels composants IA sont présents dans l'infrastructure ?
2. Quels ports, protocoles et endpoints permettent de les identifier ?
3. Quelles informations ces services exposent-ils ?
4. Comment un attaquant pourrait-il découvrir ces services ?
5. Quelles traces cette reconnaissance laisse-t-elle dans les journaux et les systèmes de surveillance ?

**Périmètre :** la mission porte sur la découverte et l'énumération. Les vérifications doivent rester dans le périmètre autorisé et ne doivent pas perturber les services.

## 4. Objectifs d'apprentissage

À la fin de cette room, je dois être capable de :

- Identifier les composants courants d'une infrastructure IA/ML de production.
- Reconnaître les ports, protocoles et chemins d'API associés à ces composants.
- Identifier des services IA en analysant les en-têtes HTTP, les structures de réponse, les messages d'erreur et les noms d'endpoints.
- Examiner les métadonnées des modèles, les historiques d'expériences et les configurations accessibles.
- Comprendre comment les services IA élargissent la surface d'attaque d'un réseau traditionnel.
- Utiliser des outils de reconnaissance existants avec des vérifications adaptées aux infrastructures IA.
- Repérer les traces réseau et les événements de journalisation pouvant révéler une activité de reconnaissance ciblant ces services.

## 5. Composants à rechercher

| Composant | Fonction | Informations à examiner |
|---|---|---|
| Serveur d'inférence | Exécute un modèle et fournit des prédictions | Modèles disponibles, versions, endpoints et état du service |
| MLflow Tracking Server | Suit les expériences et les exécutions ML | Expériences, paramètres, métriques et artefacts accessibles |
| Serveur de notebooks | Fournit un environnement interactif de développement | Interfaces exposées, authentification et informations de configuration accessibles |
| Base vectorielle | Stocke et recherche des embeddings | Endpoints accessibles, collections et contrôles d'accès |
| Stockage d'objets | Stocke les modèles, datasets et artefacts | Conteneurs, objets et permissions d'accès |
| Endpoint de métriques | Expose des données de surveillance | Métriques, noms de services et informations opérationnelles |

Ces composants peuvent être déployés sur des ports différents selon leur configuration. Un port ou un nom de service constitue un indice, pas une preuve définitive de l'identité du logiciel.

## 6. Outils de reconnaissance

### Nmap

Nmap sert à découvrir les hôtes accessibles, à identifier les ports ouverts et à recueillir des indices sur les services qui les utilisent.

Pendant les exercices, je dois comprendre :

- Ce que chaque type de scan envoie sur le réseau.
- Comment interpréter les états `open`, `closed` et `filtered`.
- Comment la détection de versions aide à identifier un service.
- Pourquoi un port ouvert ne suffit pas à confirmer qu'un service est une infrastructure IA.

### curl

curl permet d'envoyer des requêtes HTTP et HTTPS directement à un service.

Il sera utilisé pour examiner :

- Les codes de statut HTTP.
- Les en-têtes de réponse.
- Les formats JSON et les messages d'erreur.
- Les chemins d'API accessibles.
- Les informations retournées sans authentification.

L'objectif n'est pas d'envoyer des requêtes au hasard, mais de formuler une hypothèse, de la tester et d'interpréter la réponse.

### Autres outils

Selon les besoins de la room, d'autres outils pourront compléter l'analyse, notamment Wireshark pour observer les échanges réseau et des outils de recherche d'endpoints pour vérifier les interfaces documentées.

Je privilégie l'apprentissage approfondi d'un petit nombre d'outils plutôt que l'accumulation de commandes dont je ne comprends pas le fonctionnement.

## 7. Méthodologie de reconnaissance

Pour chaque service étudié, je suivrai cette démarche :

1. **Découverte :** identifier les hôtes et les ports accessibles dans le périmètre autorisé.
2. **Fingerprinting :** collecter des indices permettant d'identifier le service et sa technologie.
3. **Énumération :** consulter les endpoints documentés ou connus et examiner les informations accessibles.
4. **Analyse de l'exposition :** déterminer si les données retournées sont publiques, sensibles ou accessibles sans autorisation appropriée.
5. **Documentation :** enregistrer les commandes, les observations, les limites et les conclusions.
6. **Détection défensive :** identifier les journaux et événements qui pourraient permettre de détecter les mêmes activités.

Chaque observation doit être distinguée de son interprétation. Par exemple, une réponse JSON contenant des informations sur un modèle peut suggérer la présence d'un serveur d'inférence, mais d'autres éléments sont nécessaires pour confirmer cette hypothèse.

## 8. Reconnaissance et défense

La reconnaissance peut laisser plusieurs traces :

- Connexions répétées vers de nombreux ports.
- Requêtes HTTP vers des chemins d'API inhabituels.
- Tentatives d'accès à des endpoints de métadonnées.
- Requêtes répétées vers plusieurs services d'une même infrastructure.
- Codes HTTP inhabituels ou séquences de réponses révélant une énumération.

Ces signes ne sont pas nécessairement malveillants pris individuellement. Leur fréquence, leur séquence, leur origine et leur contexte aident à déterminer s'ils correspondent à une activité suspecte.

Du côté défensif, les mesures utiles comprennent la journalisation des requêtes, la restriction des accès réseau, l'authentification, la limitation des accès aux métadonnées et la surveillance des endpoints sensibles.

## 9. Notes et résultats des exercices

Pour chaque exercice, je documenterai :

- **Objectif :** ce que je cherche à découvrir.
- **Commande :** la commande exécutée et le rôle de ses options.
- **Observation :** les résultats réellement obtenus.
- **Interprétation :** ce que les résultats permettent de conclure.
- **Limites :** ce que les résultats ne permettent pas d'affirmer.
- **Sécurité :** les risques constatés et les mesures de protection possibles.

Les résultats ne seront ajoutés qu'après vérification pendant les exercices. Une hypothèse n'est pas un résultat, même lorsqu'elle semble particulièrement convaincante.

## 10. À retenir

La reconnaissance d'infrastructures IA reprend les fondamentaux de la reconnaissance réseau, mais les applique à de nouveaux composants et à leurs interfaces spécifiques.

- **Nmap** aide à découvrir les services accessibles.
- **curl** permet d'examiner leurs réponses HTTP et leurs API.
- **L'analyse des réponses** aide à identifier les technologies et les informations exposées.
- **La documentation** permet de distinguer les faits des hypothèses.
- **La surveillance défensive** aide à détecter les tentatives de reconnaissance.

Le but n'est pas simplement de trouver un port ouvert. Il est de comprendre quel service se trouve derrière, ce qu'il révèle et pourquoi cette exposition compte pour la sécurité.


