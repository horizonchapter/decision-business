# Décision : Boutique de stickers (cas fictif, 20/11/2026)
Terminé = dossier d'une page, chiffres étiquetés, verdict + seuil qui ferait changer d'avis + test de 72 h + date de décision.

**Verdict : PIVOT (provisoire, FRAGILE).** Avec 0,16 € de marge nette par vente, il faut 186 ventes par mois pour couvrir 30 € de charges fixes, contre 40 attendues (HYPOTHÈSE).
Je change d'avis si le test de 72 h montre au moins 120 ventes par mois possibles à 4,40 € ou plus. Date de décision : 27/11/2026.
Verdict du calculateur : PIVOT (règle 3, point mort > ventes réalistes). Écart avec le verdict final : aucun.

## 1. Question et seuils (écrits avant le calcul)
- Décision : lancer ou non une boutique de stickers à 4 €, avant le 27/11/2026.
- Plafond de perte : 300 € · objectif mensuel : 0 € (au moins l'équilibre) · minimum par heure : aucun (HYPOTHÈSES par défaut).
- Projet prioritaire en cours : aucun dans ce cas fictif.

## 2. Entrées
| Champ | Valeur | Étiquette | Source (date) |
|---|---:|---|---|
| Prix | 4,00 € | HYPOTHÈSE | prix visé, non testé |
| Achat + livraison | 2,50 € | ESTIMÉ | devis imprimeur et tarif lettre suivie fictifs |
| Frais de paiement | 2 % + 0,25 € | HYPOTHÈSE | frais courants |
| Retours | 3 % | HYPOTHÈSE | aucune |
| Coût d'acquisition | 0,50 € | HYPOTHÈSE | aucune, à mesurer |
| Cotisations | 10 % | INCONNU | taux d'exemple, à remplacer par le taux officiel du jour |
| Charges fixes / investissement | 30 €/mois / 100 € | ESTIMÉ | abonnement et stock fictifs |
| Ventes | 40/mois | HYPOTHÈSE | aucune, à mesurer |
| Temps | 10 h/mois | ESTIMÉ | préparation des commandes |

## 3. Chiffres (chiffrer.py, exemples/entree-exemple.json)
- Par vente : CA net 3,88 € ; marge avant pub 1,05 € ; marge nette unitaire 0,16 €.
- Sur 3 mois : prudent -189,28 € ; réaliste -170,56 € (-2,35 € par heure) ; optimiste -151,84 €.
- Point mort 186 ventes/mois ; récupération : jamais ; perte maximale 250 € avec la pub engagée (sous le plafond de 300 €).
- Sensibilité : le prix fait basculer (+10 % -> marge 0,50 €). Hypothèse qui pèse le plus : le prix, à ±20 % le résultat mensuel va de -50,82 € à +3,78 €.

## 4. Demande et concurrence
Non mesurées dans ce cas fictif (INCONNU). En vrai : competitive-brief sur 3 à 5 boutiques, prix relevés avec source et date ; deep-research pour la taille du marché.

## 5. Avocat du diable
Même en optimiste la boutique perd de l'argent ; à -2,35 € de l'heure, le temps passé coûte ; un sticker à 4 € se vend partout, rien ne protège la marge. Verdict : NE PAS LANCER au prix actuel, LANCER AVEC CONDITIONS seulement si le prix tient à 4,40 € ou plus.

## 6. Test de 72 h
Action : page de précommande à 4,40 € le lot de 3, montrée à 200 personnes de la cible · seuil : 6 précommandes (3 %), écrit avant · date : 23/11/2026 · résultat : à remplir.

## 7. INCONNU, HYPOTHÈSES et risques
- Taux de cotisations officiel du jour (INCONNU) ; coût d'acquisition réel ; retours plus forts que 3 %.

## 8. Suivi
27/11/2026 : résultat du test -> nouveau verdict -> ligne dans DECISIONS.md après accord.

