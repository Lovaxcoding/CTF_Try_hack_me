# Nmap101 — Types de scans de ports

## 1. Objectif

Un scan de ports permet d'identifier les ports accessibles d'une machine et de découvrir les services potentiellement actifs.

Nmap propose plusieurs méthodes pour tester les ports TCP et UDP. Le choix dépend de l'objectif, des privilèges disponibles et du comportement réseau recherché.

## 2. Les trois types de scans

| Type de scan | Commande | Principe |
|---|---|---|
| TCP Connect Scan | `nmap -sT 10.82.142.50` | Établit une connexion TCP complète avec les ports testés. |
| TCP SYN Scan | `sudo nmap -sS 10.82.142.50` | Envoie des sondes SYN sans établir normalement une connexion TCP complète. |
| UDP Scan | `sudo nmap -sU 10.82.142.50` | Envoie des sondes UDP pour identifier les ports UDP ouverts ou filtrés. |

**Attention :** l'adresse IP utilisée est celle de l'exemple du laboratoire. Effectuer ces scans uniquement sur des systèmes que l'on est autorisé à tester.

### TCP Connect Scan — `-sT`

Cette méthode utilise l'appel système `connect()` pour établir une connexion TCP.

- Port ouvert : la connexion TCP peut être établie.
- Port fermé : la cible répond généralement par un paquet RST.
- Port filtré : la connexion peut expirer ou être bloquée.

**À retenir :** la connexion complète peut être journalisée par le service cible.

### TCP SYN Scan — `-sS`

Cette méthode envoie une sonde TCP SYN pour examiner la réponse de la cible.

- SYN-ACK : le port est généralement ouvert.
- RST : le port est généralement fermé.
- Absence de réponse ou réponse ICMP de filtrage : le port peut être filtré.

Nmap n'achève normalement pas la connexion TCP après avoir reçu SYN-ACK.

**À retenir :** ce scan est souvent appelé *half-open scan*. Il nécessite généralement des privilèges élevés sous Linux.

### UDP Scan — `-sU`

UDP ne possède pas de poignée de main comparable à TCP.

- Réponse UDP : le port est généralement ouvert.
- ICMP Port Unreachable : le port est généralement fermé.
- Absence de réponse : le port peut être ouvert, filtré ou ne pas répondre à la sonde.

**À retenir :** les scans UDP peuvent être plus lents, notamment lorsque les réponses sont limitées par la cible ou le réseau.

## 3. Options de sélection des ports

| Option | Fonction |
|---|---|
| `-p-` | Scanne tous les ports, de 1 à 65535. |
| `-p 1-1023` | Scanne les
