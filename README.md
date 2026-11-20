<p align="center">
  <img src="assets/banner.png" alt="Decision Business" width="100%">
</p>

<p align="center">
  <img alt="Licence MIT" src="https://img.shields.io/badge/licence-MIT-2F5BFF?style=flat-square">
  <img alt="Skill Claude" src="https://img.shields.io/badge/Claude-skill-060A14?style=flat-square">
  <img alt="Version 2.2.1" src="https://img.shields.io/badge/version-2.2.1-8E9AB2?style=flat-square">
</p>

# decision-business — Decision Business

**Une seule porte pour démarrer un projet et pour décider : un entretien une question à la fois, puis des chiffres vérifiables et un verdict STOP, PIVOT ou CONTINUER.**
*Start sharp, decide with numbers: STOP, PIVOT or CONTINUE.*

## ✦ Ce que fait le skill

| | |
|---|---|
| **Mode démarrage** | Une question à la fois, 3 choix A/B/C dont un recommandé, modes rapide, standard, complet, fiche finale. |
| **Mode décision** | Marge nette, point mort, 3 scénarios, résultat par heure, avec un calculateur testé (`chiffrer.py`). |
| **Honnêteté des chiffres** | VÉRIFIÉ, ESTIMÉ, HYPOTHÈSE, INCONNU ; demande et concurrence sourcées ; avocat du diable. |
| **Verdict** | STOP, PIVOT ou CONTINUER avec un test de 72 h, en une page. |

## ✦ Installation

**Télécharger** : bouton vert **Code → Download ZIP**, ou :

```bash
git clone https://github.com/horizonchapter/decision-business.git
```

**Claude Code** (pour tous tes projets) :

```bash
cp -r decision-business/skills/decision-business ~/.claude/skills/
```

**Claude (app et web)** : importe le fichier [`decision-business.zip`](decision-business.zip) dans les réglages des skills de Claude.

## ✦ Utilisation

- « Grille-moi sur ce projet. »
- « Est-ce rentable ? On lance ? »
- `python skills/decision-business/scripts/chiffrer.py --test`

## ✦ Remplace

Ce skill reprend [grill-me](https://github.com/horizonchapter/grill-me) (mode démarrage, inspiré de Matt Pocock, MIT) et [chiffrage-projet](https://github.com/horizonchapter/chiffrage-projet) (calculateur). Ces deux dépôts sont archivés.

## ✦ Structure

```
decision-business/
├── skills/decision-business/
│   ├── SKILL.md
│   ├── references/   démarrage, chiffrage, modèle de dossier
│   ├── scripts/      chiffrer.py
│   └── exemples/     entretien, entrée JSON, fiche de décision (fictifs)
├── decision-business.zip
└── assets/             bannière
```

## ✦ Voir aussi

[design-horizon](https://github.com/horizonchapter/design-horizon) · [publication-sure](https://github.com/horizonchapter/publication-sure) · [memoire-relais](https://github.com/horizonchapter/memoire-relais) · [pdf-sobre](https://github.com/horizonchapter/pdf-sobre) · [skill-booster](https://github.com/horizonchapter/skill-booster) · [clearmind](https://github.com/horizonchapter/clearmind)

## ✦ Licence

[MIT](LICENSE). Historique des versions : [CHANGELOG](CHANGELOG.md).
