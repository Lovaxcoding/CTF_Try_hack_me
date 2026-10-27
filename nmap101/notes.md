# Nmap101 — Host Discovery

## Objectif

La découverte d'hôtes (*Host Discovery*) permet d'identifier les machines actives sur un réseau avant d'effectuer des scans de ports ou d'autres analyses.

Une réponse réseau peut indiquer qu'un hôte est actif, mais l'absence de réponse ne prouve pas qu'il est hors ligne : un pare-feu peut bloquer les sondes.

## 1. Types de découverte

| Méthode | Exemple | Principe |
|---|---|---|
| ARP | `sudo nmap -PR -sn 10.200.6.0/24` | Recherche les hôtes sur le réseau local via ARP. |
| ICMP Echo | `sudo nmap -PE -sn 10.200.6.0/24` | Envoie des requêtes ICMP Echo, similaires au ping. |
| ICMP Timestamp | `sudo nmap -PP -sn 10.200.6.0/24` | Utilise des requêtes ICMP Timestamp. |
| ICMP Address Mask | `sudo nmap -PM -sn 10.200.6.0/24` | Utilise des requêtes ICMP Address Mask. |
| TCP SYN Ping | `sudo nmap -PS22,80,443 -sn 10.200.6.0/30` | Envoie des sondes TCP SYN vers les ports indiqués. |
| TCP ACK Ping | `sudo nmap -PA22,80,443 -sn 10.200.6.0/30` | Envoie des sondes TCP ACK. |
| UDP Ping | `sudo nmap -PU53,161,162 -sn 10.200.6.0/30` | Envoie des sondes UDP vers les ports indiqués. |

**À retenir :** ces méthodes permettent de découvrir des hôtes, mais leur efficacité dépend du réseau, des ports ciblés et des règles de filtrage.

## 2. Options essentielles

| Option | Fonction |
|---|---|
| `-sn` | Découverte d'hôtes uniquement, sans scan de ports. |
| `-n` | Désactive les résolutions DNS. |
| `-R` | Force la résolution DNS inverse pour tous les hôtes ciblés. |
| `-PE` | Utilise ICMP Echo pour la découverte. |
| `-PR` | Utilise ARP pour la découverte. |
| `-PS` | Utilise des sondes TCP SYN. |
| `-PA` | Utilise des sondes TCP ACK. |
| `-PU` | Utilise des sondes UDP. |
| `-PP` | Utilise ICMP Timestamp. |
| `-PM` | Utilise ICMP Address Mask. |

## 3. Comprendre les paramètres réseau

- `/24` : représente généralement 256 adresses IPv4 au total, dont 254 adresses utilisables dans un sous-réseau classique.
- `/30` : représente 4 adresses IPv4 au total, généralement 2 adresses utilisables dans un sous-réseau classique.
- `-PS22,80,443` : cible les ports TCP 22, 80 et 443 avec des sondes SYN.

Les exemples utilisent des adresses de laboratoire. Il faut adapter le réseau ciblé à son environnement autorisé.

## 4. Quel type de scan choisir ?

- **Réseau local :** ARP est souvent efficace pour découvrir les machines IPv4 du même segment réseau.
- **Réseau distant :** ICMP, TCP ou UDP peuvent être utilisés selon les réponses attendues et les filtrages.
- **Découverte rapide :** ajouter `-sn` pour éviter le scan de ports.
- **Résolution DNS inutile :** ajouter `-n` pour éviter les requêtes DNS et accélérer potentiellement le scan.

## 5. Exercices pratiques

Sur une machine ou un réseau de laboratoire autorisé :

1. Comparer `nmap -sn` avec et sans `-n`.
2. Comparer les résultats de `-PE` et `-PS22,80,443`.
3. Observer les paquets générés avec Wireshark.
4. Expliquer pourquoi certains hôtes répondent à une méthode, mais pas à une autre.

## Conclusion

La découverte d'hôtes est une étape de reconnaissance. Le choix de la méthode doit dépendre de la topologie du réseau et des réponses attendues, pas d'une simple collection de commandes à mémoriser.

**Principe d'apprentissage :** comprendre la sonde envoyée, la réponse attendue et les raisons possibles d'une absence de réponse.
