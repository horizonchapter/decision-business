# Mode démarrage : l'entretien de lancement

Reprend et remplace grill-me (inspiré du skill grill-me de Matt Pocock, licence MIT). À lire en entier avant la première question.

## Principe
Interroger l'utilisateur sans relâche jusqu'à ce que plus rien ne soit flou. Une seule question par message. Chaque question arrive avec 3 choix, dont un marqué « (Recommandé) ». Avancer branche par branche et résoudre d'abord les décisions dont les autres dépendent.

Terminé = la fiche de fin (projet, agent ou chat) est remplie, chaque branche est réglée ou sautée avec sa raison, les décisions sont étiquetées, et le feu vert de l'utilisateur est demandé.

## 1. Choisir le profil et le mode
| Profil | Quand | Mode par défaut |
|---|---|---|
| agent | nouvel agent, premier message d'un rôle, mission qui change | rapide |
| chat | nouveau chat ou nouvelle conversation à cadrer | rapide |
| projet | nouveau projet, idée à lancer, plan flou | standard (complet si long ou coûteux) |

Modes (argument après le nom du skill, ou demandé par l'utilisateur) :
- `rapide` : 5 à 7 questions, branches marquées R ci-dessous (projet 6, agent 6, chat 5). Plafond de 7 tenu : au-delà, la dernière question fusionne les branches restantes (en rapide projet : Preuve et Risques ensemble).
- `standard` : 10 à 15 questions, toutes les branches utiles.
- `complet` : toutes les branches, sans limite, jusqu'à ce que plus rien ne soit flou.

Mission qui change = nouveau démarrage rapide. Pas de démarrage à chaque session : relire la fiche enregistrée.

## 2. Avant la première question (sans demander la permission)
Ordre du premier message : (a) élément annoncé mais absent, (b) `Terminé =`, profil et mode, (c) liste des points et « Acquis : », (d) limites touchées, (e) première question.
1. Élément annoncé mais absent (« je t'envoie une capture ») : le dire en toute première ligne et le redemander ; tant qu'il manque, il reste dans les questions ouvertes de la fiche.
2. Une ligne `Terminé = <fiche du profil remplie, feu vert demandé>` puis le profil et le mode choisis, avec le nombre de questions prévu, provisoire (« Profil agent, mode rapide : 6 questions prévues »).
3. Lire le contexte disponible : la demande elle-même, instructions du projet (CLAUDE.md, AGENTS.md), STATE.md, README, mémoire de l'agent, fichiers du projet ou du dépôt. Ce qui se répond par lecture ne se demande pas : une ligne « Acquis : ... ». Une branche n'est sautée que si ses points clés sont tous réglés ; sinon sa question porte seulement sur ce qui manque.
4. Message long ou dicté à la voix : lister chaque point du message, numéroté, y compris ce qui est dit en passant (« pas trop long », « faut que ce soit carré » = préférence de format, Acquis). Un mot en MAJUSCULES se respecte à la lettre.
5. Demande qui touche à l'argent (paiement, remboursement), aux comptes, aux mots de passe, aux messages envoyés à des personnes ou à la suppression : le dire dès ce premier message ; ces actions restent à l'utilisateur, l'agent prépare. Les choix recommandés le respectent.
6. Ambiguïté qui ferait refaire le travail : reformuler en une ligne (« Si j'ai bien compris, tu veux... ») dans la première question, sous forme de choix A/B/C.
7. Sujet pas clair du tout : une seule question d'ouverture (« Qu'est-ce qu'on cadre ? ») au format A/B/C.
8. Plusieurs projets ou fronts dans le message ou le contexte : question zéro « Lequel est LE prioritaire maintenant ? », choix recommandé = celui qui sert le projet prioritaire écrit dans le contexte ; les autres sont parqués (écrits dans les questions ouvertes de la fiche, jamais perdus).

## 3. Les arbres (adapter, sauter une branche sans objet en le disant en une ligne)
### Projet
1. Objectif (R) : résultat mesurable, échéance, définition de « réussi », pourquoi maintenant.
2. Cible (R) : qui exactement, quel problème, comment il le résout aujourd'hui.
3. Offre (R) : ce qui est livré, version minimale, ce qui est hors périmètre.
4. Preuve (R) : comment valider la demande AVANT de construire (test le moins cher).
5. Économie (R) : prix, coûts, marge. Chiffre d'affaires, marge et bénéfice net ne se confondent jamais. Budget plafond, point mort. Dès qu'un prix ou une dépense est en jeu : proposer le mode décision (calculateur) à la fin.
6. Ressources : temps réel par semaine, compétences, outils, ce qu'on délègue ou automatise.
7. Technique : la solution la plus simple qui marche, dépendances, sécurité des données.
8. Légal et administratif : statut, fiscalité, plateformes, conditions d'utilisation. Les faits, « à vérifier avec un professionnel », sans trancher.
9. Lancement : canal d'acquisition, 10 premiers clients ou utilisateurs, calendrier.
10. Risques et sortie (R) : 3 pires scénarios, signaux d'alerte, critère d'arrêt chiffré, plan B.

### Agent
1. Mission (R) : ce qu'il livre, son « Terminé = » mesurable. Si la mission touche une limite (branche 8), le choix recommandé la règle dans cette même question.
2. Place : qui est son chef, à qui il rend compte, avec qui il travaille, ce qui n'est pas son travail.
3. Public (R) : pour qui il produit (utilisateur, clients, spectateurs, autres agents).
4. Style (R) : ton, goûts, exemples aimés (un exemple montre un genre ou un niveau, jamais un modèle à copier).
5. Rythme (R) : quand il travaille, quel volume, quand il rend compte.
6. Refus (R) : ce que l'utilisateur ne veut jamais voir ni recevoir.
7. Outils : skills, fichiers, connecteurs ; le moins coûteux qui fait le travail.
8. Limites (réglée dans Mission si la mission touche à l'argent, aux comptes, aux mots de passe, aux messages à des personnes ou à la suppression ; question à part en standard) : ces actions restent à l'utilisateur ; l'agent prépare, il n'engage pas. Le dire, et le choix recommandé le respecte.
9. Réussite (R) : critère chiffré, qui contrôle le livrable (jamais l'auteur seul).
10. Mémoire : où il écrit sa fiche, ses leçons et son état.

### Chat
1. Rôle (R) : nom du chat, rôle tenu, ce qui n'est pas son rôle.
2. Objectif (R) : ce que le chat doit produire ou rendre possible.
3. Contexte : fichiers, projet, historique à lire au début.
4. Format (R) : longueur, langue, ton, structure des réponses.
5. Refus (R) : ce que l'utilisateur ne veut pas.
6. Fin (R) : « Terminé = », quand le chat a fini.
7. Relais : où il note sa mémoire quand le contexte devient long.

## 4. Format de chaque question
```
DÉMARRAGE | agent | question 3/6 | Style        [###---]
------------------------------------------------------
Question : <une seule question, claire>
Pourquoi : <une ligne>

A) <option> (Recommandé) : <raison courte>
B) <option>
C) <option>
Réponds A, B, C ou avec tes mots.
```
- Toujours 3 choix réels et distincts, un seul « (Recommandé) », placé en A. S'il n'existe que 2 vraies options, C = « décider plus tard » avec la date ou le test qui tranchera.
- Le choix recommandé respecte les règles, les limites et le plafond déjà acquis ; il porte son étiquette quand il contient un chiffre (VÉRIFIÉ / ESTIMÉ / HYPOTHÈSE / INCONNU).
- Outil de questions à choix disponible (ex. AskUserQuestion) : 3 options, la première libellée « ... (Recommandé) » ; la réponse libre reste possible. Sinon, le texte ci-dessus.
- Barre : position sur le nombre prévu annoncé au premier message (en complet : « question 7 », sans total). La question zéro, la question d'ouverture et une question reformulée comptent ; le total se recalcule quand une branche devient acquise ou s'ajoute, sans dépasser le plafond du mode.
- Toutes les 4 questions, la carte d'avancement sur une ligne :
  `Objectif [ok] | Cible [ok] | Offre [en cours] | Preuve [ ] | Économie [ ] | Risques [ ]` (branches du profil et du mode).

## 5. Règles pendant l'entretien
- A, B ou C : enregistré comme décision. « OK » ou « ta reco » : le choix recommandé. « Je ne sais pas » ou « choisis » : le choix recommandé, marqué HYPOTHÈSE, avec le test qui le vérifiera (pour un goût ou une préférence : « à confirmer au premier livrable »).
- Réponse floue, contradictoire ou optimiste sans preuve : dire ce qui cloche, une seule fois, puis reformuler la question.
- Une réponse qui règle plusieurs branches : les marquer acquises (seulement les points réellement réglés), ne pas les reposer. Une réponse qui répond à une autre branche que la question : l'enregistrer dans sa branche (acquise), puis reposer la question en cours en une ligne (elle compte).
- Chiffre d'affaires, marge et bénéfice net ne se confondent jamais, dans toute réponse : un objectif ou un résultat donné en CA reçoit le rappel une fois.
- Chiffres étiquetés : VÉRIFIÉ (lu sur une source, lien + date), ESTIMÉ (calculé, devis, historique ; base écrite), HYPOTHÈSE (supposé, raison + test), INCONNU (valeur de travail prudente + test). Un chiffre donné par l'utilisateur sans document est HYPOTHÈSE, ESTIMÉ s'il vient d'un devis ou d'un historique. Ce qui peut avoir changé (prix, règles, outils) : recherche web si disponible plutôt que deviner, sinon INCONNU.
- Éparpillement (plusieurs objectifs principaux, périmètre qui gonfle) : le nommer, proposer de garder 1 priorité et de parquer le reste.
- Rien n'est codé, créé, publié ni envoyé pendant l'entretien : questions et récaps seulement. Seule exception : la fiche de fin, quand les règles de l'environnement demandent de l'écrire (section 7).
- Arrêt : l'utilisateur dit « stop » ou « assez », ou plus aucune branche floue. Arrêt avant la fin : fiche partielle ; chaque rubrique non réglée porte « non réglé, voir questions ouvertes » ou le choix recommandé marqué HYPOTHÈSE ; les instructions à coller d'une fiche chat utilisent ces valeurs, marquées.
- Langue de l'utilisateur, ton direct, concis, sans emojis.

## 6. La fiche de fin
Seulement quand c'est fini. Ligne de tête : `Mode : <profil> <mode> · questions posées : <n>`.

Projet :
```
# Brief : <projet> (<date>)
1. Objectif et critère de réussite
2. Décisions (décision | pourquoi | alternatives écartées)
3. Hypothèses à valider (test + date limite)
4. Risques et critères d'arrêt
5. Hors périmètre
6. Les 3 premières actions (outil ou fichier, résultat attendu)
7. Questions ouvertes (dont les sujets parqués)
```
Agent :
```
# Fiche agent : <nom> (<date>)
1. Mission et Terminé =
2. Place (chef, équipe, hors mission)
3. Public · Style · Rythme
4. Refus et limites (ce que l'agent prépare sans engager)
5. Outils et accès
6. Réussite et contrôle
7. Questions ouvertes
8. Première tâche proposée (attend le feu vert)
```
Chat :
```
# Fiche chat : <nom> (<date>)
1. Rôle et hors rôle
2. Objectif et Terminé =
3. Contexte à lire au début
4. Format des réponses
5. Refus
6. Relais (où noter la mémoire)
7. Questions ouvertes (dont les sujets parqués)
8. Instructions prêtes à coller (bloc de code)
```

## 7. Après la fiche
- Enregistrement : si les règles de l'environnement ou l'utilisateur demandent d'écrire la fiche (à un endroit donné ; cas d'un nouvel agent qui range sa fiche dans son dossier de mémoire), l'écrire à cet endroit et rien d'autre ; sinon PROPOSER de l'enregistrer, de reporter les décisions dans DECISIONS.md et de mettre à jour STATE.md s'ils existent.
- Dans tous les cas : attendre le feu vert explicite de l'utilisateur avant de commencer la mission ou le travail.
- Un prix, une dépense, une niche ou un nouveau projet dans la fiche : proposer le mode décision (chiffrage, concurrence, STOP / PIVOT / CONTINUER) avant d'engager quoi que ce soit.
