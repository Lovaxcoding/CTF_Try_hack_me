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



