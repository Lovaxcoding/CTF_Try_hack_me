# Sécurisation des systèmes d'IA : Defence in Depth, Least Privilege et MLSecOps

## 1. Defence in Depth (Défense en profondeur)

La **défense en profondeur** consiste à déployer plusieurs couches de sécurité indépendantes afin qu'une attaque qui contourne un contrôle puisse encore être bloquée par un autre.

Dans un système d'IA, les contrôles doivent être placés à chaque frontière de confiance identifiée dans l'architecture.

### Contrôles de sécurité par frontière de confiance

| Frontière | Contrôles de sécurité |
|---|---|
| **User-to-System** | Validation de la longueur des entrées, limitation du débit (*rate limiting*), filtrage du contenu et authentification. |
| **System-to-LLM** | Détection des tentatives de prompt injection, renforcement des instructions système et limitation de la taille du contexte. |
| **LLM-to-Tools** | Requêtes paramétrées, permissions minimales pour les outils et approbation des opérations d'écriture. |
| **System-to-External-Data** | Validation des sources documentaires récupérées et assainissement du contenu avant son inclusion dans le prompt. |
| **System-to-User** | Assainissement des sorties, masquage des données personnelles (PII), limitation de la longueur des réponses et filtrage de sécurité du contenu. |

### Exemple : une attaque bloquée à plusieurs niveaux

Un attaquant tente une prompt injection à travers l'interface de chat.

1. Le filtre d'entrée ne détecte pas la tentative.
2. Le modèle reçoit la requête et génère une demande d'utilisation d'un outil.
3. La couche des outils vérifie les permissions et exige une approbation humaine pour l'opération sensible.
4. L'action non autorisée est bloquée.

Même si le premier contrôle échoue, les couches suivantes peuvent empêcher l'attaque d'aboutir.

**Principe essentiel :** aucun contrôle isolé ne doit être considéré comme une protection suffisante.

---

## 2. Associer les menaces aux contrôles de sécurité

Chaque catégorie de menace étudiée précédemment nécessite des mesures de protection adaptées.

| Menace OWASP | Risque | Contrôle principal |
|---|---|---|
| **LLM02 - Sensitive Information Disclosure** | Divulgation d'informations sensibles. | Masquage des PII, contrôle d'accès aux données et chiffrement du stockage des journaux. |
| **LLM05 - Improper Output Handling** | Utilisation dangereuse des sorties du modèle par les composants en aval. | Validation des sorties, requêtes paramétrées et assainissement contextuel. |
| **LLM06 - Excessive Agency** | Privilèges ou autonomie excessifs. | Principe du moindre privilège et approbation des opérations sensibles. |
| **LLM07 - System Prompt Leakage** | Divulgation des instructions système. | Réduction des informations confidentielles dans le prompt et contrôles d'accès indépendants. |
| **LLM10 - Unbounded Consumption** | Consommation excessive de ressources ou augmentation incontrôlée des coûts. | Limitation du débit, validation de la taille des entrées et quotas de consommation. |

**Attention :** le renforcement du prompt peut réduire certains risques de divulgation, mais ne garantit pas la confidentialité. Les données sensibles doivent être protégées par des contrôles d'accès et des mécanismes de sécurité indépendants du modèle.

---

## 3. Least Privilege (Principe du moindre privilège)

Le principe du moindre privilège consiste à attribuer à chaque composant uniquement les permissions nécessaires à l'accomplissement de sa tâche.

Un LLM ne doit pas disposer de privilèges étendus simplement parce qu'il est capable de demander des actions.

### Application aux composants d'IA

#### Accès aux bases de données

- Utiliser un accès en lecture seule par défaut.
- Autoriser les écritures uniquement lorsqu'elles sont justifiées.
- Limiter les opérations aux ressources nécessaires.
- Utiliser des requêtes paramétrées pour éviter les injections SQL.

#### Jetons d'API (API tokens)

- Limiter les jetons aux endpoints et aux opérations nécessaires.
- Éviter les jetons disposant de privilèges administratifs ou root.
- Protéger les secrets et permettre leur révocation.
- Ne jamais exposer les jetons dans les prompts ou les réponses du modèle.

#### Liste d'autorisation des outils (Tool Allowlisting)

- Autoriser uniquement les fonctions explicitement enregistrées.
- Bloquer les tentatives d'appel de fonctions non autorisées.
- Journaliser les appels d'outils et les tentatives bloquées.
- Valider les paramètres de chaque appel avant son exécution.

#### Intervention humaine (Human-in-the-Loop)

Toute opération sensible modifiant l'état d'un système peut nécessiter une approbation humaine avant son exécution.

Exemples :
- Déployer du code.
- Modifier ou supprimer des enregistrements.
- Envoyer des communications.
- Modifier des permissions ou des configurations critiques.

L'approbation doit être appliquée par le système d'exécution, et non simplement demandée au modèle dans son prompt.

---

## 4. Validation des entrées et des sorties

Les systèmes d'IA acceptent souvent du langage naturel libre plutôt que des données strictement structurées. La validation reste indispensable, mais doit tenir compte du comportement particulier des LLM.

### Validation des entrées (Input Validation)

À la frontière d'entrée, le système peut appliquer les contrôles suivants :

- Limiter la longueur des requêtes.
- Appliquer des limites de fréquence.
- Détecter et examiner les motifs connus de prompt injection.
- Authentifier les utilisateurs et vérifier leurs permissions.
- Séparer clairement les instructions de confiance des données non fiables.

**Limite importante :** les filtres fondés sur des motifs connus ne détectent pas toutes les prompt injections. Une entrée qui passe le filtrage ne doit donc pas être considérée comme sûre par défaut.

### Validation des sorties (Output Validation)

Les sorties du LLM doivent être considérées comme des données non fiables.

Ne jamais transmettre directement du texte généré par le modèle à un interpréteur de commandes, une requête SQL ou un template HTML sans les contrôles adaptés.

Bonnes pratiques :

- Extraire uniquement les champs attendus.
- Valider les types, les valeurs et le format des données.
- Utiliser des schémas de sortie définis lorsque cela est possible.
- Appliquer un échappement adapté au contexte, notamment HTML.
- Utiliser des requêtes paramétrées pour les bases de données.
- Interdire l'exécution directe de commandes générées sans validation et autorisation indépendantes.

Les schémas de sortie structurés réduisent les possibilités de sortie inattendue, mais ne remplacent pas les contrôles de sécurité.

---

## 5. Monitoring and Observability (Surveillance et observabilité)

Les contrôles de sécurité cherchent à prévenir ou à bloquer les attaques. La surveillance permet de détecter les comportements suspects, les anomalies et les tentatives qui franchissent les premières protections.

### Éléments à surveiller

| Élément surveillé | Objectif |
|---|---|
| **Request Patterns** | Détecter les sondages automatisés, les pics inhabituels de requêtes et les volumes de requêtes anormaux. |
| **Token Consumption** | Repérer les hausses de coûts, les processus incontrôlés et les consommations excessives. |
| **Tool Invocations** | Détecter les appels d'outils inattendus, notamment les opérations d'écriture. |
| **Response Anomalies** | Identifier les changements inhabituels dans la longueur, le contenu ou le comportement des réponses. |
| **System Prompt Extraction Attempts** | Journaliser et examiner les tentatives suspectées d'extraction des instructions système. |
| **Cost Metrics** | Définir des alertes budgétaires et des mécanismes d'arrêt automatique en cas de dépassement. |

### Exemple de politique de surveillance

Un système peut déclencher une alerte lorsque :
- Le nombre de requêtes dépasse un seuil défini.
- La consommation de tokens augmente brutalement.
- Un agent tente d'appeler un outil rarement utilisé.
- Des opérations d'écriture sont demandées de façon inhabituelle.
- Les coûts dépassent le budget autorisé.

Les seuils doivent être adaptés à l'utilisation normale du système afin de limiter les faux positifs.

### Journalisation et confidentialité

Les journaux doivent permettre d'analyser les incidents sans devenir une nouvelle source de fuite de données.

Il convient notamment de :
- Limiter l'enregistrement des données sensibles.
- Contrôler l'accès aux journaux.
- Masquer les secrets et les données personnelles lorsque nécessaire.
- Définir une durée de conservation adaptée.
- Protéger l'intégrité des traces d'audit.

---

## 6. MLSecOps

**MLSecOps** signifie *Machine Learning Security Operations*.

Cette approche intègre la sécurité tout au long du cycle de vie d'un système de machine learning : développement, tests, déploiement et exploitation.

Elle applique le principe du **Shift Left**, qui consiste à prendre en compte la sécurité le plus tôt possible plutôt que d'attendre la mise en production.

### Étapes de MLSecOps

1. **Développement :** identifier les risques liés aux modèles, aux données et à l'architecture.
2. **Tests :** évaluer la résistance aux entrées malveillantes, les permissions et les risques de fuite.
3. **Déploiement :** configurer les accès, les quotas et les contrôles de sécurité.
4. **Exploitation :** surveiller les requêtes, les appels d'outils, les coûts et les anomalies.
5. **Amélioration continue :** analyser les incidents, corriger les faiblesses et adapter les protections.

MLSecOps ne cherche pas uniquement à répondre à la question « L'application est-elle sécurisée ? », mais aussi à vérifier que le modèle se comporte comme prévu et que le système empêche son utilisation abusive.

---

## 7. Checklist de sécurité pour un système d'IA

- [ ] Des contrôles sont placés à chaque frontière de confiance.
- [ ] Les entrées sont soumises à des limites de taille et de fréquence.
- [ ] Les prompts et les documents récupérés sont traités selon leur niveau de confiance.
- [ ] Les outils disposent uniquement des permissions nécessaires.
- [ ] Les appels d'outils sont autorisés et leurs paramètres sont validés.
- [ ] Les opérations sensibles nécessitent une approbation appropriée.
- [ ] Les sorties du modèle sont validées avant leur utilisation par d'autres composants.
- [ ] Les données personnelles et les secrets sont protégés.
- [ ] Les tokens, les coûts et les appels d'outils sont surveillés.
- [ ] Des alertes et des mécanismes de limitation ou d'arrêt sont configurés.
- [ ] Les journaux sont protégés contre les accès non autorisés.
- [ ] La sécurité est intégrée à l'ensemble du cycle de vie du système.

## Conclusion

La sécurisation d'un système d'IA repose sur plusieurs principes complémentaires :

- **Defence in Depth :** multiplier les couches de protection.
- **Least Privilege :** limiter les permissions de chaque composant.
- **Input and Output Validation :** contrôler les données avant leur utilisation.
- **Monitoring and Observability :** détecter les comportements anormaux.
- **MLSecOps :** intégrer la sécurité tout au long du cycle de vie.

**À retenir :** le LLM peut proposer une action, mais le système doit décider si cette action est autorisée, la limiter à ce qui est nécessaire et en surveiller l'exécution.
