# Décision : <projet> (<date>)
Terminé = dossier d'une page, chiffres étiquetés, verdict + seuil qui ferait changer d'avis + test de 72 h + date de décision.

**Verdict : STOP / PIVOT / CONTINUER** (provisoire si FRAGILE), en une phrase.
Je change d'avis si : <seuil mesurable>. Date de décision : <date>.
Verdict du calculateur : <verdict + règle>. Écart avec le verdict final : <aucun / raison, seulement vers plus de prudence>.

## 1. Question et seuils (écrits avant le calcul)
- Décision : <quoi, pour qui, avant quand>
- Plafond de perte : <montant> · objectif mensuel : <montant> · minimum par heure : <montant>
- Projet prioritaire en cours : <nom> ; cette décision ouvre-t-elle un nouveau front ? <oui / non>

## 2. Entrées
| Champ | Valeur | Étiquette | Source (date) |
|---|---:|---|---|
| <champ> | <valeur> | VÉRIFIÉ / ESTIMÉ / HYPOTHÈSE / INCONNU | <source> |

## 3. Chiffres (sortie de chiffrer.py)
- Par vente : prix, marge avant pub, marge nette unitaire.
- Scénarios prudent / réaliste / optimiste : ventes, résultat mensuel, par heure, sur l'horizon.
- Point mort, récupération, perte maximale.
- Sensibilité : ce qui fait basculer. Hypothèse qui pèse le plus : <champ, fourchette>.

## 4. Demande et concurrence
| Concurrent | Prix | Promesse | Faiblesse | Source (date) |
|---|---:|---|---|---|
Demande : <signal mesuré, avec source datée, ou INCONNU>.

## 5. Avocat du diable
<avis cité tel quel, ou pré-mortem écrit : 3 risques, ce qui les prouverait, coût d'un échec, verdict LANCER / AVEC CONDITIONS / NE PAS LANCER>

## 6. Test de 72 h
Action : <sans construire> · seuil de réussite : <écrit avant> · date : <date> · résultat : <à remplir après>

## 7. INCONNU, HYPOTHÈSES et risques
- <ce qui manque, et comment le mesurer>

## 8. Suivi
<date> : résultat du test -> nouveau verdict -> ligne dans DECISIONS.md après accord.
