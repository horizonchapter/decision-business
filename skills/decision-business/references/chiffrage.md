# Chiffrage (reprise complète de chiffrage-projet 1.0, 20/11/2026)

Source : skill chiffrage-projet (02-skills/chiffrage-projet et compte Claude). Le calculateur est scripts/chiffrer.py de decision-business (copie identique).


Transforme une idée en fiche chiffrée honnête, avec une décision. Sert avant de lancer, de continuer ou d'arrêter un projet (produit, boutique, SaaS, jeu, service).

## Règles de fond
- Ne confonds jamais chiffre d'affaires (CA), marge et bénéfice net.
- Micro-entreprise en France : les cotisations portent sur le CA encaissé et les dépenses ne se déduisent pas, donc une dépense coûte son prix plein. Taux, plafonds, seuil de TVA et aides (ex. ACRE) : cherche-les sur une source officielle (URSSAF, impots.gouv) à la date du jour, cite la source et la date. Jamais de taux de mémoire : sinon INCONNU.
- Étiquette chaque chiffre important : VÉRIFIÉ (source + date) / ESTIMÉ / HYPOTHÈSE / INCONNU. Jamais d'hypothèse présentée comme un fait.
- N'invente aucun chiffre de marché (volume, coût d'acquisition, conversion) : mets une HYPOTHÈSE avec sa raison, ou INCONNU, et propose le test qui la transforme en chiffre.
- Fiscalité, juridique, installation à l'étranger : donne les faits et dis « à vérifier avec un professionnel ». Pas de conseil définitif.

## Étapes
1. **Cadrer** : projet, période, budget maximum acceptable (plafond), et ce qui compte comme réussi. Écris les seuils de décision AVANT de calculer.
2. **Entrées** : tableau `paramètre | valeur | étiquette | source`. Paramètres : prix, coût d'achat ou de production, livraison, frais de paiement et de plateforme, taux de retours, coût d'acquisition par vente (pub), taux de cotisations, charges fixes mensuelles, investissement initial, ventes mensuelles, horizon en mois. Pour un manque : une seule question groupée, sinon HYPOTHÈSE explicite.
3. **Calcul** : par le code (script `scripts/chiffrer.py` s'il est disponible, sinon quelques lignes de Python), jamais de calcul de tête pour les résultats.
4. **Trois scénarios** : prudent (volume x0,5, coût d'acquisition x1,3), réaliste, optimiste (volume x1,5, coût d'acquisition x0,9). Ces multiplicateurs sont des HYPOTHÈSES de départ, modifiables.
5. **Sensibilité** : prix ±10 %, coût d'acquisition ±30 %, retours. Dis lequel fait basculer le résultat.
6. **Décision** : STOP / PIVOT / CONTINUER (seuils ci-dessous) avec une date de décision à fixer.
7. **Test de validation de 72 h**, sans construire, qui transforme la plus grosse HYPOTHÈSE en chiffre.

## Formules (par vente, prix encaissé)
- CA net = prix x (1 - retours)
- Frais = prix x frais en % + frais fixes par vente
- Cotisations = CA net x taux de cotisations
- Marge avant pub = CA net - achat - livraison - frais
- **Marge nette unitaire = marge avant pub - coût d'acquisition - cotisations**
- Résultat mensuel = ventes x marge nette unitaire - charges fixes
- Point mort (ventes par mois) = charges fixes / marge nette unitaire (si > 0)
- Récupération (mois) = investissement / résultat mensuel (si > 0)
- Perte maximale = le plus grand de : investissement + (charges fixes + pub engagée) x horizon à 0 vente (pub engagée = coût d'acquisition x ventes visées), et la perte du pire scénario
- Seuils de bascule : ventes par mois pour l'objectif = (objectif + fixes) / marge nette ; prix minimum pour que la marge nette dépasse le seuil
- Une vente = une commande : `articles_par_commande` x prix + `port_facture` ; livraison, frais fixes et coût d'acquisition comptés par commande (port offert : `port_facture` 0 et `livraison` = ce que paie le vendeur)
Par prudence, un retour fait perdre le prix de vente mais pas les coûts.

## Format d'entrée de chiffrer.py (decision-business 2.0)
Chaque champ : un nombre, ou `{"valeur": 4.0, "etiquette": "VÉRIFIÉ|ESTIMÉ|HYPOTHÈSE|INCONNU", "source": "..."}` (forme à préférer : le calculateur liste les entrées non étiquetées).
- Requis : `prix`, `cout_achat`, `taux_cotisations_pct`, `ventes_mensuelles`.
- Facultatifs (0 par défaut) : `livraison`, `frais_pct`, `frais_fixe`, `taux_retours_pct`, `cac`, `couts_fixes_mensuels`, `investissement`, `heures_par_mois` ; `horizon_mois` (6 par défaut, un choix, pas un fait) ; `minutes_par_vente` (les heures suivent alors les ventes de chaque scénario), `articles_par_commande` (1), `port_facture` (0), `mois_sans_revenu` (revenu à seuil : monétisation, éligibilité, construction ; ces mois-là seules les charges courent), `heures_construction` (une fois, comptées dans le « par heure sur l'horizon »).
- `seuils` : `budget_plafond` (plafond de perte), `marge_nette_min` (0), `objectif_mensuel` (0), `horaire_min` (0 = pas de minimum). `budget_plafond` au premier niveau reste accepté (format 1.0).
- `scenarios` : remplace les multiplicateurs `[volume, coût d'acquisition]`, ex. `{"prudent": [0.4, 1.5]}`.
Sortie en plus des chiffres : verdict FRAGILE si une entrée décisive (prix, achat, coût d'acquisition, cotisations, ventes) n'est ni VÉRIFIÉ ni ESTIMÉ, et l'hypothèse qui pèse le plus (écart du résultat mensuel réaliste sur sa plage réaliste : ventes ±50 %, coût d'acquisition ±30 %, retours ±50 %, autres ±20 % ; `"plage_pct"` dans l'entrée la remplace), cible du test de 72 h. Marge nette négative : le calculateur prévient que l'« optimiste » est le pire scénario.

## Seuils par défaut (HYPOTHÈSES, à confirmer avant le calcul) et ordre des règles
La première règle vraie donne le verdict :
1. STOP : marge nette unitaire <= `marge_nette_min`.
2. STOP : perte maximale > plafond.
3. PIVOT : le point mort dépasse les ventes du scénario réaliste.
4. PIVOT : résultat mensuel réaliste < `objectif_mensuel`.
5. PIVOT : le scénario prudent perd plus que le plafond sur l'horizon.
6. PIVOT : résultat par heure réaliste < `horaire_min`.
Sinon CONTINUER (avec alerte si le scénario prudent perd de l'argent chaque mois).

## Sortie : la fiche de chiffrage
```
# Chiffrage : <projet> (<date>)
Décision recommandée : STOP / PIVOT / CONTINUER, en une phrase, avec le seuil qui ferait changer d'avis
1. Entrées (valeur | étiquette | source)
2. Par vente : prix, coûts, marge nette unitaire
3. Scénarios : ventes, résultat mensuel, résultat sur l'horizon
4. Point mort et récupération
5. Sensibilité : ce qui fait basculer
6. INCONNU et HYPOTHÈSES à valider (avec le test de 72 h)
7. Risques et date de décision
```
Reste court : une page. Si l'utilisateur veut un tableur, propose-le sans l'imposer.

## Garde-fous
- Ne déclare jamais un projet rentable avec une marge nette unitaire <= 0.
- Aucune dépense au-delà du plafond. Jamais de publication, paiement ou envoi sans accord explicite.
- Langue : celle de l'utilisateur, ton direct, sans emojis.
