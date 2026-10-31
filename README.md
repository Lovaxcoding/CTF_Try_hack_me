<h1 align="center"> 🎯 TryHackMe CTF Writeups </h1>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-TryHackMe-red?style=for-the-badge&logo=tryhackme&logoColor=white" alt="TryHackMe">
  <img src="https://img.shields.io/badge/CTFs_Total_Resolved-300%2B-brightgreen?style=for-the-badge" alt="CTFs">
  <img src="https://img.shields.io/badge/Repo_Since-October_2026-blue?style=for-the-badge" alt="Since">
  <img src="https://img.shields.io/badge/License-Educational-purple?style=for-the-badge" alt="License">
</p>

<p align="center">
  <i>Collection de writeups, notes et PoCs sur les rooms <a href="https://tryhackme.com">TryHackMe</a>.<br>
  Ce dépôt documente <b>uniquement les CTFs résolus à partir d'octobre 2026</b>, dans un souci de qualité et de rigueur.</i>
</p>

---

## 📚 À propos

J'ai résolu **plus de 300 CTFs** sur TryHackMe depuis mes débuts. Ce dépôt n'a pas vocation à tout recenser — il regroupe uniquement les **writeups documentés à partir d'octobre 2026**, avec une méthodologie constante :

- 📄 Un `README.md` détaillé par room (recon → exploitation → escalade → remédiation)
- 🖼️ Des captures d'écran des étapes clés
- 🧪 Les payloads et commandes reproductibles
- 🛡️ Une section **remédiation** systématique
- 🔬 Des **PoCs** et **notes de recherche** en cybersécurité IA

> ⚠️ **Note légale** : tous les CTFs documentés ici ont été réalisés dans un **cadre légal et éthique**, sur des environnements TryHackMe autorisés. Aucune cible réelle n'a été compromise. Ces writeups sont publiés à des fins **pédagogiques** après résolution complète des rooms.

---

## 🗂️ Index des CTFs

### 🏁 Rooms TryHackMe

| 🏁 Room | 🎚️ Difficulté | 🖥️ OS | 🔑 Thèmes | 🔗 Writeup |
|---------|---------------|--------|-----------|-----------|
| **Silver Platter** | 🟢 Easy | 🐧 Linux | Auth Bypass · IDOR · sudo | [📄 Voir](./silver_platter/) |
| **Pickle Rick** | 🟢 Easy | 🐧 Linux | Web · Command Injection · PrivEsc | [📄 Voir](./pickle-rick/) |
| **Nmap 101** | 🟢 Easy | — | Networking · Reconnaissance | [📄 Voir](./nmap101/) |
| **Nmap 102** | 🟢 Easy | — | Networking · Reconnaissance | [📄 Voir](./nmap102/) |
| **Vulnerability 101** | 🟢 Easy | — | Fundamentals · CVE | [📄 Voir](./vulnerability_101/) |
| **Soup de Code 01** | 🟢 Easy | 🐧 Linux | Web · PrivEsc | [📄 Voir](./soupedecode1/) |
| **Billing** | 🟢 Easy | 🐧 Linux | Web · PrivEsc | [📄 Voir](./billing/) |
| **Grand Larceny Auto II** | 🟡 Medium | 🪟 Windows | Forensics · AD | [📄 Voir](./grandlarcenyautoii/) |
| **Malware Analysis** | 🟡 Medium | 🪟 Windows | Reverse · Static/Dynamic | [📄 Voir](./malware_analysis/) |
| **FOODCTF** | 🎯 CTF | — | Multi-catégories | [📄 Voir](./FOODCTF.md) |

### 🔬 PoCs & Recherche

| 📦 Projet | 🎯 Description | 🔗 Lien |
|-----------|----------------|---------|
| **PHP2Shell PoC** | PoC d'exploitation PHP → shell | [📄 Voir](./php2shell_poc/) |
| **IA — Reconnaissance Système** | Techniques de recon assistées par LLM | [📄 Voir](./ia_reconnaissance_système/) |
| **IA — Roadmap** | Feuille de route cybersécurité IA | [📄 Voir](./ia_roadmap/) |
| **IA — Threat Modeling** | Modélisation de menaces pour systèmes IA | [📄 Voir](./ia_threat_modeling/) |
| **Input Manipulation / Prompt Injection** | Notes sur les injections de prompts | [📄 Voir](./input_manipulation_prompt_injection/) |

> 💡 Certaines rooms ont leur difficulté estimée. N'hésite pas à ouvrir une issue si tu repères une erreur.

---

## 📊 Statistiques du dépôt

| Métrique | Valeur |
|----------|--------|
| 🎯 CTFs documentés (ce repo) | **15+** |
| 🏆 CTFs résolus au total | **300+** |
| 🟢 Easy | 7 |
| 🟡 Medium | 2 |
| 🔴 Hard | 0 |
| 🎯 CTF (custom) | 1 |
| 🐧 Linux | 5 |
| 🪟 Windows | 2 |
| 🔬 PoCs & Recherche IA | 5 |

> 📌 Ces stats ne reflètent que le contenu du dépôt (à partir d'octobre 2026), pas l'ensemble de mon parcours TryHackMe.

---

## 🧭 Structure du repository

```
CTF_TryHackMe/
│
├── README.md                                  # ← Vous êtes ici
│
├── 🏁 ROOMS TRYHACKME
│   ├── silver_platter/                        # Easy · Linux
│   ├── pickle-rick/                           # Easy · Linux
│   ├── nmap101/                               # Easy · Networking
│   ├── nmap102/                               # Easy · Networking
│   ├── vulnerability_101/                     # Easy · Fundamentals
│   ├── soupedecode1/                          # Easy · Linux
│   ├── billing/                               # Easy · Linux
│   ├── grandlarcenyautoii/                    # Medium · Windows
│   ├── malware_analysis/                      # Medium · Malware
│   └── FOODCTF.md                             # CTF custom
│
├── 🔬 PoCs & RECHERCHE
│   ├── php2shell_poc/                         # Exploit PHP → shell
│   ├── ia_reconnaissance_système/             # Notes IA
│   ├── ia_roadmap/                            # Roadmap IA
│   ├── ia_threat_modeling/                    # Threat modeling
│   └── input_manipulation_prompt_injection/   # Prompt injection
│
├── 🛠️ RESSOURCES
│   ├── config/                                # Configs réutilisables
│   └── wordlists/                             # Wordlists perso
│
└── _TEMPLATE/                                 # 📋 Template nouveau CTF
    └── README.md
```

### 📋 Conventions de nommage

- **Dossiers rooms** : `snake_case` ou `nom-room/`
- **Writeups** : `README.md` à la racine du dossier
- **Images** : `images/` dans le dossier du CTF
- **Commits** : `feat(room): ajout writeup <room>` ou `docs(ia): ajout notes <sujet>`

---

## 🚀 Navigation rapide

### Par difficulté
- 🟢 **Easy** — [Silver Platter](./silver_platter/) · [Pickle Rick](./pickle-rick/) · [Nmap 101](./nmap101/) · [Nmap 102](./nmap102/) · [Vulnerability 101](./vulnerability_101/) · [Soup de Code 01](./soupedecode1/) · [Billing](./billing/)
- 🟡 **Medium** — [Grand Larceny Auto II](./grandlarcenyautoii/) · [Malware Analysis](./malware_analysis/)
- 🎯 **CTF** — [FOODCTF](./FOODCTF.md)

### Par OS
- 🐧 **Linux** — Silver Platter · Pickle Rick · Soup de Code 01 · Billing
- 🪟 **Windows** — Grand Larceny Auto II · Malware Analysis
- 🌐 **Networking / Fondamentaux** — Nmap 101 · Nmap 102 · Vulnerability 101

### Par thème
- 🔐 **Auth Bypass** — [Silver Platter](./silver_platter/)
- 🕳️ **IDOR** — [Silver Platter](./silver_platter/)
- 💉 **Command Injection / Web** — [Pickle Rick](./pickle-rick/) · [Soup de Code 01](./soupedecode1/) · [Billing](./billing/)
- ⬆️ **PrivEsc** — [Silver Platter](./silver_platter/) · [Pickle Rick](./pickle-rick/) · [Billing](./billing/)
- 🕵️ **Forensics / AD** — [Grand Larceny Auto II](./grandlarcenyautoii/)
- 🦠 **Malware Analysis** — [Malware Analysis](./malware_analysis/)
- 🤖 **Cybersécurité IA** — [ia_reconnaissance_système](./ia_reconnaissance_système/) · [ia_threat_modeling](./ia_threat_modeling/) · [Input Manipulation](./input_manipulation_prompt_injection/)

---

## 🛠️ Stack & Outils utilisés

| Catégorie | Outils |
|-----------|--------|
| **Reconnaissance** | `nmap` · `ffuf` · `gobuster` · `nuclei` · `whatweb` · `amass` |
| **Exploitation Web** | `burpsuite` · `curl` · `sqlmap` · `wpscan` · `nikto` |
| **Escalade de privilèges** | `linpeas` · `winpeas` · `sudo -l` · `GTFOBins` · `find` |
| **Reverse Shell** | `netcat` · `rlwrap` · `msfvenom` · `python3 -c` |
| **Forensics** | `volatility` · `autopsy` · `wireshark` · `strings` |
| **IA / Prompt** | `langchain` · `ollama` · `garak` · `burp-ai` |

---

## 📖 Format d'un writeup

Chaque writeup suit la même structure pour faciliter la lecture :

```markdown
# 🏁 Nom de la Room

> **Plateforme :** TryHackMe
> **Difficulté :** Easy / Medium / Hard
> **Cible :** <IP>
> **OS :** Linux / Windows

## 📖 Contexte
Description rapide du scénario et des objectifs.

## 1. 🔍 Reconnaissance
Scan de ports, énumération web, découverte d'indices.

## 2. 💥 Exploitation
Vulnérabilités exploitées, payloads, captures.

## 3. 🎯 Accès initial
Obtention du premier shell ou identifiant.

## 4. 🔼 Escalade de privilèges
Pivot et obtention de root.

## 5. 🗺️ Résumé du parcours
Schéma récapitulatif de la chaîne d'attaque.

## 6. 🛡️ Recommandations de remédiation
Tableau des fixes pour chaque vulnérabilité.

## 7. 📚 Références
CVE, documentations, ressources externes.
```

---

## ➕ Ajouter un nouveau CTF

1. **Créer le dossier** :
   ```bash
   mkdir nom_room
   cd nom_room
   mkdir images
   ```

2. **Copier le template** :
   ```bash
   cp ../_TEMPLATE/README.md ./README.md
   ```

3. **Compléter le writeup** (voir structure ci-dessus).

4. **Mettre à jour ce README** :
   - Ajouter une ligne dans le tableau [Index des CTFs](#-index-des-ctfs)
   - Mettre à jour les [statistiques](#-statistiques-du-dépôt)
   - Ajouter le lien dans les sections [Navigation rapide](#-navigation-rapide)

5. **Commit** :
   ```bash
   git add .
   git commit -m "feat(room): ajout writeup <nom_room>"
   git push
   ```

---

## 🏆 Progression

```
Parcours global TryHackMe :  300+ CTFs résolus
Ce dépôt (depuis oct. 2026) : [███████░░░░░░░░░░░░░] 15+ / 50 (objectif 2026)
```

> 🎯 Objectif : documenter **50 rooms** dans ce dépôt d'ici fin 2026, en gardant un niveau de qualité constant (writeups complets + remédiation).

---

## 📬 Contact & Contributions

- 🐙 **GitHub** : [@Lovaxcoding](https://github.com/Lovaxcoding)
- 💬 **Issues** : suggestions, corrections et feedback bienvenus via [les issues](../../issues)
- ⭐ **Star** : mets une ⭐ si ces writeups t'aident !

---

## ⚖️ Licence & Disclaimer

```
Educational Use Only

Les writeups publiés dans ce repository sont fournis à des fins
pédagogiques uniquement. Toutes les techniques décrites ont été
utilisées dans un cadre légal (CTF TryHackMe). L'auteur décline
toute responsabilité quant à une utilisation malveillante des
informations présentées.

Toute reproduction doit mentionner la source.
```

<p align="center">
  <i>Fait avec ❤️ et beaucoup de ☕ par <a href="https://github.com/Lovaxcoding">Lovaxcoding</a></i>
</p>
