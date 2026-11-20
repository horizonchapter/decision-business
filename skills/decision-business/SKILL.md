---
name: decision-business
description: Porte unique pour démarrer et pour décider. Mode démarrage (remplace grill-me) - entretien de lancement d'un nouvel agent, d'un nouveau chat ou d'un projet - lit le contexte, pose une question à la fois avec 3 choix A/B/C dont un « (Recommandé) », modes rapide, standard, complet, repère l'éparpillement et finit par une fiche. Mode décision - un projet, une niche, un produit, un prix ou une dépense vaut-il le coup ? Arbre de décision fixe, calculateur testé (marge nette, point mort, 3 scénarios, résultat par heure), demande et concurrence sourcées, avocat du diable, chiffres VÉRIFIÉ / ESTIMÉ / HYPOTHÈSE / INCONNU, verdict STOP, PIVOT ou CONTINUER avec test de 72 h, en une page. Pour /grill-me, « grille-moi », nouvel agent, nouveau chat, « cadre ce projet », « est-ce rentable ? », « on lance ? », « STOP ou on continue ? », prix, marge, concurrence, choix entre deux idées, avant toute dépense, refonte ou nouveau projet.
---

# Décision business

Deux modes, une seule porte : démarrer (cadrer un agent, un chat ou un projet) et décider (chiffrer, trancher). Fichiers :
- `references/demarrage.md` : l'entretien de démarrage complet (profils, arbres, format des questions, fiches de fin).
- `scripts/chiffrer.py` : le calculateur (aucune dépendance, `--test` pour l'auto-contrôle).
- `references/chiffrage.md` : formules, format d'entrée, seuils.
- `references/modele-dossier.md` : le dossier de décision à remplir.
- `exemples/` : un entretien de démarrage, une entrée étiquetée et le dossier de décision qui en sort.

## Choisir le mode (d'abord)
| Signal | Mode |
|---|---|
| nouvel agent, premier message d'un rôle, mission qui change, nouveau chat, /grill-me, « grille-moi », « cadre ce projet », plan flou | démarrage |
| « rentable ? », « on lance ? », STOP / PIVOT / CONTINUER, prix, marge, dépense, concurrence, choix entre deux idées | décision |
| nouveau projet : plan clair (chiffres, offre, cible) -> décision ; plan flou -> démarrage | selon le plan |
Les deux à la fois : démarrage rapide d'abord, puis décision sur la fiche obtenue. Doute : une question au format A/B/C ci-dessous.

## Mode démarrage
Lire `references/demarrage.md` en entier avant la première question. L'essentiel :
- Profil agent, chat ou projet ; mode rapide (5 à 7 questions), standard (10 à 15) ou complet (sans limite). Défauts : agent et chat en rapide, projet en standard.
- Premier message : élément annoncé absent d'abord, puis `Terminé =`, profil, mode et nombre de questions, « Acquis : ... » (contexte et demande), chaque point d'un message dicté, limites touchées (argent, comptes, mots de passe, messages, suppression), question zéro si plusieurs fronts.
- Une seule question par message, toujours ce format :
```
DÉMARRAGE | agent | question 3/6 | Style        [###---]
------------------------------------------------------
Question : <une seule question>
Pourquoi : <une ligne>
A) <option> (Recommandé) : <raison courte>
B) <option>
C) <option>
Réponds A, B, C ou avec tes mots.
```
- « OK » = le choix recommandé ; « je ne sais pas » = le recommandé en HYPOTHÈSE. Rien n'est codé, créé, publié ni envoyé pendant l'entretien, sauf la fiche de fin quand l'environnement ou l'utilisateur demande de l'écrire.
- Fin : la fiche du profil, puis feu vert explicite de l'utilisateur avant tout travail. Un prix, une dépense ou un nouveau projet dans la fiche : proposer le mode décision.

## Mode décision
### 0. Cadrer (avant tout chiffre)
- Écris `Terminé = dossier de décision d'une page, chiffres étiquetés, verdict + seuil qui ferait changer d'avis + test de 72 h + date de décision`.
- Une phrase : quelle décision, pour qui, avant quand. Plafond de perte acceptable. Ce qui compte comme réussi.
- Seuils écrits AVANT le calcul, dans le bloc `seuils` de l'entrée : plafond de perte, objectif de résultat mensuel, minimum par heure (défauts dans `references/chiffrage.md`).
- Garde-fou dispersion : si la décision ouvre un nouveau front alors qu'un projet prioritaire n'est pas fini, le dire en première ligne avec le projet prioritaire.

### 1. L'arbre de décision (dans cet ordre, sans sauter de case)
```
A. Le plan est-il clair (cible, offre, prix, objectif) ?
   non -> mode démarrage, profil projet, rapide (une question à la fois, format A/B/C), puis reprendre en B ; l'utilisateur refuse ou toujours flou -> verdict « pas décidable » + ce qui manque. Fin.
   personne pour répondre (sous-agent, routine, cas écrit) -> 3 questions au plus, groupées et écrites dans le dossier ; jamais de réponse simulée ni de feu vert supposé ; chiffrer.py ne tourne pas sur des valeurs inventées ; verdict « pas décidable » + ce qui manque + 2 ou 3 pistes à chiffrer ensuite (sans prix ni verdict). Fin.
B. Les chiffres de marché existent-ils (taille, prix pratiqués, tendance) ?
   non -> skill deep-research (sinon recherche web) ; chaque chiffre trouvé = VÉRIFIÉ + source + date.
C. Des concurrents existent ?
   oui -> skill competitive-brief (sinon tableau : 3 à 5 concurrents, prix, promesse, faiblesse, source datée).
   non -> le dire, et chercher pourquoi (marché vide ou marché mort ?).
D. Chiffrer : chiffrer.py sur l'entrée étiquetée (section 2).
E. Verdict du calculateur : première règle vraie, dans l'ordre
   1. marge nette unitaire <= minimum                         -> STOP
   2. perte maximale (0 vente) > plafond                       -> STOP
   3. point mort > ventes du scénario réaliste                 -> PIVOT
   4. résultat mensuel réaliste < objectif                     -> PIVOT
   5. le scénario prudent perd plus que le plafond             -> PIVOT
   6. résultat par heure réaliste < minimum par heure          -> PIVOT
   sinon                                                      -> CONTINUER
F. Le verdict est-il FRAGILE (prix, ventes, coût d'acquisition, cotisations ou achat en HYPOTHÈSE ou INCONNU) ?
   oui -> aucune dépense avant le test de 72 h sur « l'hypothèse qui pèse le plus » ; verdict provisoire.
G. Avocat du diable (section 3). Il peut faire descendre le verdict (CONTINUER -> PIVOT -> STOP), jamais le monter.
H. Décision finale, seuil qui ferait changer d'avis, test de 72 h, date de décision.
```
Le verdict final peut différer de celui du calculateur seulement vers plus de prudence, avec la raison écrite (demande, concurrence, avocat du diable).
Taux de cotisations, plafonds, TVA, aides : source officielle à la date du jour (URSSAF, impots.gouv), jamais de mémoire, sinon INCONNU.
FRAGILE ne remonte jamais un STOP : un STOP reste STOP ; on écrit seulement quelle entrée fragile pourrait le renverser et le test qui le dirait.
Comparer deux options : un `chiffrer.py` par option avec les mêmes seuils, puis un tableau côte à côte (marge nette, point mort, résultat réaliste, par heure sur l'horizon construction comprise, perte maximale, verdict).
Proportion : deep-research et competitive-brief seulement pour les chiffres qui peuvent changer le verdict ; sinon 3 sources ouvertes à la main suffisent, et on le dit.

### 2. Chiffrer (calculateur, jamais de tête)
1. Entrée JSON (format complet : `references/chiffrage.md`) : chaque valeur `{"valeur": 4.0, "etiquette": "HYPOTHÈSE", "source": "..."}`. Un INCONNU garde une valeur de travail ; le test de 72 h la remplacera.
2. `python <skill>/scripts/chiffrer.py entree.json` : entrées étiquetées, marge nette unitaire, point mort, récupération, perte maximale, 3 scénarios avec résultat par heure, seuils de bascule, sensibilité, verdict, mention FRAGILE et hypothèse qui pèse le plus. `--json` pour réutiliser. `--test` : auto-contrôle (13 cas) avant de s'y fier sur une nouvelle machine.
3. CA, marge et bénéfice net ne se confondent jamais. Micro-entreprise : cotisations sur le CA encaissé, dépenses non déductibles.
4. Le temps compte : `heures_par_mois` donne le résultat par heure, à comparer au `horaire_min` ; `minutes_par_vente` fait suivre les heures aux ventes de chaque scénario, `heures_construction` compte le temps de mise en place.
5. Cas que le calculateur couvre (format : `references/chiffrage.md`) : panier de plusieurs articles et port offert (`articles_par_commande`, `port_facture`), revenu qui n'arrive qu'après un seuil ou une période (`mois_sans_revenu` : monétisation de plateforme, éligibilité, construction), pub dépensée même à 0 vente (comptée dans la perte maximale), seuils de bascule. Hors calculateur, à écrire à part avec source : TVA (franchise en base ou non ; ventes numériques à des particuliers de l'UE : régime OSS et seuil de 10 000 € ; import hors UE : IOSS), revenus récurrents, coûts d'hébergement qui montent avec l'usage.
6. Les chiffres d'un vendeur de formation ou d'une capture (« 10 000 €/mois ») ne servent jamais de base : preuve non vérifiable, biais du survivant, CA et non bénéfice. Les écrire comme tels et les exclure du calcul.

### 3. Avocat du diable (obligatoire)
- Si un agent avocat-du-diable existe (décision coûteuse ou difficile à défaire : argent, nouveau projet, refonte, changement d'organisation), le lancer avec le dossier en cours et citer son avis tel quel : 3 risques, ce qui les prouverait, coût d'un échec, verdict LANCER / LANCER AVEC CONDITIONS / NE PAS LANCER. Sans avis, la décision n'est pas prise.
- Sinon, l'écrire soi-même en 3 à 5 lignes, en pré-mortem : « dans 3 mois, ça a échoué : pourquoi ? », ce qui rend le scénario réaliste trop optimiste, ce qu'on abandonne en le faisant.

### 4. Étiquettes (partout, y compris dans le dossier)
| Étiquette | Quand | Exige |
|---|---|---|
| VÉRIFIÉ | lu sur la page source ouverte (pas un extrait de moteur de recherche, pas un site tiers qui la résume) | lien ou document + date |
| ESTIMÉ | calculé ou tiré d'un devis, d'un historique | la base du calcul |
| HYPOTHÈSE | supposé, plausible | la raison + le test qui le mesure |
| INCONNU | pas de donnée fiable | une valeur de travail prudente + le test |
Un chiffre garde la même étiquette dans tout le dossier. Jamais d'HYPOTHÈSE présentée comme un fait. Page officielle injoignable : ESTIMÉ (source secondaire nommée) ou INCONNU, jamais VÉRIFIÉ. La lecture qu'on fait d'un concurrent (sa faiblesse) est une HYPOTHÈSE, sauf avis client ou source citée.

### 5. Décider et prouver
- Test de 72 h, sans construire, sur l'hypothèse qui pèse le plus : action, seuil de réussite écrit avant, date.
- Dossier : copier `references/modele-dossier.md`, le remplir (exemple : `exemples/fiche-decision-exemple.md`). « Une page » = 450 mots au plus, une page A4 : verdict, 5 chiffres clés, pré-mortem de 3 à 5 lignes DANS le dossier, risques (réglementaires compris, chacun « fait » ou « à vérifier » avec source datée), test de 72 h, date. Le détail (chiffrage complet, concurrents, sources) va en annexe dans un fichier à part, cité par son nom.
- Contrôle : un relecteur qui n'a pas écrit le dossier (dans l'AIOS : l'agent contrôleur ; ailleurs : un autre agent ou l'utilisateur). Pas de relecteur disponible : écrire « contrôle indépendant non fait » dans le dossier, jamais le sauter en silence.
- Dans l'AIOS : dossier dans `a_valider/` du projet, ligne dans `DECISIONS.md` seulement après l'accord réel de l'utilisateur ; sans accord, écrire « en attente d'accord » (jamais d'accord simulé).

## Garde-fous
- Jamais « rentable » avec une marge nette unitaire <= 0.
- Aucun chiffre de marché inventé : HYPOTHÈSE avec sa raison, ou INCONNU, et le test qui le mesure.
- Fiscalité, juridique, étranger : les faits et « à vérifier avec un professionnel ».
- Aucune dépense, aucun paiement, aucun compte créé, aucun message envoyé : la décision se prépare, l'utilisateur engage l'argent.
- Langue de l'utilisateur, ton direct, sans emojis.
