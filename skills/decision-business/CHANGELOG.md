# Changelog decision-business

## 1.0.0 (2026-11-20)
- Création (super-skills, demande de l'utilisateur, 20/11) : chiffrage-projet 1.0 repris en entier (references/chiffrage.md, scripts/chiffrer.py identique), grill-me, deep-research et competitive-brief appelés, avis contraire et test de 72 h obligatoires, fiche de décision en 9 rubriques.
- Essai : exemples/entree-exemple.json -> sortie identique à chiffrage-projet (diff vide), PIVOT, point mort 185 ventes/mois.


## 2.0.0 (2026-11-20, demande de l'utilisateur)
- grill-me sort du parcours : il reste l'entretien de démarrage d'un agent ou d'un chat ; un plan flou se cadre ici en 3 questions au plus.
- Arbre de décision A à H dans SKILL.md, 6 règles de verdict dans un ordre écrit, verdict final seulement plus prudent que le calculateur, avec raison.
- chiffrer.py : entrées étiquetées (`valeur`, `etiquette`, `source`, format 1.0 toujours lu), bloc `seuils` (plafond, marge minimum, objectif mensuel, minimum par heure), `heures_par_mois` et résultat par heure, multiplicateurs de scénarios réglables, verdict FRAGILE, hypothèse qui pèse le plus (±20 %), table des entrées dans la sortie, `--test` (7 cas).
- Changement de comportement : la règle « le scénario prudent perd plus que le plafond » (écrite en 1.0 mais absente du code) rend maintenant PIVOT au lieu de CONTINUER.
- Nouveau : references/modele-dossier.md ; section étiquettes ; liens deep-research, competitive-brief, avocat-du-diable.
- Essais : `--test` OK ; exemple -> mêmes chiffres qu'en 1.0 (JSON comparé clé par clé, seul ajout : par heure), PIVOT, point mort 185, FRAGILE, hypothèse qui pèse le plus = prix (-50,82 à +3,78 par mois) ; étiquette inconnue et INCONNU sans valeur -> message clair, code 1 ; multiplicateurs remplacés -> pris en compte.

## 2.1.0 (2026-11-20)
- Nouveau mode démarrage (references/demarrage.md) : reprend 100 % de grill-me 1.0.0 (principe, 3 modes, lecture du contexte, question d'ouverture, question zéro de priorité, arbre projet en 10 branches, barre et carte d'avancement, règles, fiche de fin, propositions d'enregistrement) et l'étend : profils agent et chat, 3 choix A/B/C avec un seul « (Recommandé) » en A, messages dictés (liste de chaque point, MAJUSCULES, élément annoncé absent, reformulation), Économie ajoutée au mode rapide projet, limites (argent, comptes, mots de passe, messages, suppression) dans le profil agent, fiche agent et fiche chat, enregistrement selon les règles de l'environnement, feu vert obligatoire, passage au mode décision quand un prix ou une dépense apparaît.
- SKILL.md : table « Choisir le mode », résumé du mode démarrage, mode décision inchangé sauf l'étape A (plan flou -> mode démarrage rapide au lieu de 3 questions groupées).
- Description : déclenchée aussi par /grill-me, « grille-moi », nouvel agent, nouveau chat (grill-me avait disable-model-invocation, retiré ici exprès : le démarrage d'un agent doit se déclencher seul).
- Nouveau : exemples/demarrage-exemple.md (repris de l'exemple de grill-me, au nouveau format).
- Essais : 3 cas de démarrage (nouvel agent, chat dicté en vrac, projet rapide) joués avec grill-me puis avec cette version, relus par un contrôleur indépendant ; 14 défauts du texte corrigés (ordre du premier message, compte des questions, limites dès le départ, réponse hors question, étiquettes, fiche partielle) ; chiffrer.py inchangé (`--test` OK).

## 2.2.0 (2026-11-20, corrections après le banc : 5 cas joués, moyenne 7,9)
- chiffrer.py : pub engagée (coût d'acquisition x ventes visées) comptée dans la perte à 0 vente, et perte maximale jamais inférieure à la perte du pire scénario (banc 01 : 204,60 au lieu de 384,60 ; banc 03 : 470 alors que le réaliste perdait 1 672) ; hypothèse qui pèse le plus mesurée sur une plage réaliste par entrée (ventes ±50 %, coût d'acquisition ±30 %, `plage_pct` pour la changer) : le volume n'est plus battu d'office par le prix à ±20 % (bancs 02, 04, 05) ; `minutes_par_vente` (heures qui suivent les ventes de chaque scénario) ; `articles_par_commande` et `port_facture` (panier moyen, port offert) ; `mois_sans_revenu` (monétisation à seuil, période de construction) et `heures_construction` (par heure sur l'horizon) ; seuils de bascule (ventes pour l'objectif, prix minimum) ; alerte « marge négative : l'optimiste est le pire ». `--test` : 7 -> 13 cas, chacun écrit sur un défaut du banc.
- Exemple : perte maximale 190 -> 250 (pub comptée) ; plafond de l'exemple passé de 200 à 300 pour garder un cas PIVOT (avec 200, le calculateur dit maintenant STOP, ce qui est juste).
- SKILL.md : VÉRIFIÉ seulement sur la page source ouverte ; lecture d'un concurrent = HYPOTHÈSE ; « une page » définie (450 mots, pré-mortem dans le dossier, annexes à part) ; relecteur indépendant défini (contrôleur dans l'AIOS, sinon « contrôle non fait » écrit) ; jamais d'accord simulé pour DECISIONS.md ; FRAGILE ne remonte pas un STOP ; comparer deux options ; proportion deep-research ; chiffres de vendeurs de formation exclus ; TVA, OSS, IOSS, récurrent : à écrire à part avec source.

## 2.2.1 (2026-11-20, seconde vague du banc, cas 06 noté 3,0/10)
- SKILL.md, case A de l'arbre : personne pour répondre = 3 questions groupées écrites, jamais de réponse simulée ni de feu vert supposé, pas de calcul sur des valeurs inventées, verdict « pas décidable » + 2 ou 3 pistes. Attendus du juge couverts par une ligne écrite : 1/5 avant, 5/5 après (ESTIMÉ : contrôle statique, cas non rejoué).
- chiffrer.py : entrée JSON avec BOM (Notepad, PowerShell) lue (avant : JSONDecodeError) ; point mort et ventes pour l'objectif arrondis au-dessus (avant : 1,44 affiché « 1 » ; exemple 185 -> 186). `--test` : 13 -> 14 cas.
