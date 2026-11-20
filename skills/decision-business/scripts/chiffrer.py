#!/usr/bin/env python3
"""Calculateur de decision-business. Usage : python chiffrer.py entree.json [--json] | python chiffrer.py --test
Aucune dépendance. Pourcentages en pourcents (12.3). Chaque valeur s'écrit soit en nombre, soit
{"valeur": 4.0, "etiquette": "VÉRIFIÉ|ESTIMÉ|HYPOTHÈSE|INCONNU", "source": "..."}.
Le taux de cotisations est REQUIS : source officielle datée, jamais une valeur devinée."""
import json
import math
import sys

ETIQUETTES = ("VÉRIFIÉ", "ESTIMÉ", "HYPOTHÈSE", "INCONNU")
# clé JSON -> (clé interne, défaut ; None = requis)
CHAMPS = {"prix": ("prix", None), "cout_achat": ("achat", None), "livraison": ("livraison", 0.0),
          "frais_pct": ("frais_pct", 0.0), "frais_fixe": ("frais_fixe", 0.0), "taux_retours_pct": ("retours", 0.0),
          "cac": ("cac", 0.0), "taux_cotisations_pct": ("taux", None), "couts_fixes_mensuels": ("fixes", 0.0),
          "investissement": ("invest", 0.0), "ventes_mensuelles": ("ventes", None), "horizon_mois": ("horizon", 6.0),
          "heures_par_mois": ("heures", 0.0), "minutes_par_vente": ("min_vente", 0.0),
          "articles_par_commande": ("articles", 1.0), "port_facture": ("port_facture", 0.0),
          "mois_sans_revenu": ("sans_revenu", 0.0), "heures_construction": ("h_constr", 0.0)}
# entrées dont l'incertitude rend le verdict fragile
DECISIVES = ("prix", "ventes_mensuelles", "cac", "taux_cotisations_pct", "cout_achat")
SCENARIOS = {"prudent": [0.5, 1.3], "réaliste": [1.0, 1.0], "optimiste": [1.5, 0.9]}  # [volume, coût d'acquisition], HYPOTHÈSES
# incertitude réaliste par défaut (± %) pour désigner l'hypothèse qui pèse le plus ; « plage_pct » dans l'entrée la remplace
PLAGES = {"ventes_mensuelles": 50, "cac": 30, "taux_retours_pct": 50, "minutes_par_vente": 50}


def nombre(k, v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        sys.exit("Champ " + k + " : nombre attendu")
    return float(v)


def lire(d):
    p, entrees = {"nom": str(d.get("nom", "projet"))}, []
    for k, (cle, defaut) in CHAMPS.items():
        v = d.get(k)
        if v is None:
            if defaut is None:
                sys.exit("Champ requis manquant : " + k)
            p[cle] = defaut
            continue
        etiq, src, plage = "", "", PLAGES.get(k, 20)
        if isinstance(v, dict):
            etiq, src, plage = str(v.get("etiquette", "")).upper(), str(v.get("source", "")), float(v.get("plage_pct", plage))
            if etiq and etiq not in ETIQUETTES:
                sys.exit("Champ " + k + " : étiquette " + etiq + " inconnue (" + " / ".join(ETIQUETTES) + ")")
            if "valeur" not in v or v["valeur"] is None:
                sys.exit("Champ " + k + " : valeur de travail requise même si INCONNU (le test de 72 h la remplacera)")
            v = v["valeur"]
        p[cle] = nombre(k, v)
        entrees.append({"champ": k, "valeur": p[cle], "etiquette": etiq or "non étiqueté", "source": src, "plage": plage})
    s = d.get("seuils", {})
    p["seuils"] = {"plafond": s.get("budget_plafond", d.get("budget_plafond")),
                   "marge_min": float(s.get("marge_nette_min", 0)), "objectif": float(s.get("objectif_mensuel", 0)),
                   "horaire_min": float(s.get("horaire_min", 0))}
    p["scenarios"] = {**SCENARIOS, **d.get("scenarios", {})}
    p["entrees"] = entrees
    return p


def par_vente(p, prix=None, cac=None):
    """Une vente = une commande : articles_par_commande x prix + port facturé ; livraison, frais fixes et cac par commande."""
    prix = (p["prix"] if prix is None else prix) * p["articles"] + p["port_facture"]
    cac = p["cac"] if cac is None else cac
    ca_net = prix * (1 - p["retours"] / 100)  # un retour fait perdre le prix, pas les coûts (prudence)
    frais = prix * p["frais_pct"] / 100 + p["frais_fixe"]
    cotis = ca_net * p["taux"] / 100
    avant_pub = ca_net - p["achat"] * p["articles"] - p["livraison"] - frais
    return {"prix": prix, "ca_net": ca_net, "frais": frais, "cotisations": cotis,
            "marge_avant_pub": avant_pub, "cac": cac, "marge_nette": avant_pub - cac - cotis}


def scenario(p, nom, mult_volume, mult_cac):
    u = par_vente(p, cac=p["cac"] * mult_cac)
    ventes = p["ventes"] * mult_volume
    mensuel = ventes * u["marge_nette"] - p["fixes"]
    heures = p["heures"] + ventes * p["min_vente"] / 60  # les heures suivent les ventes si minutes_par_vente est donné
    actifs = max(p["horizon"] - p["sans_revenu"], 0)  # mois sans revenu (éligibilité, construction) : charges seules
    horizon = mensuel * actifs - p["fixes"] * (p["horizon"] - actifs) - p["invest"]
    h_total = heures * p["horizon"] + p["h_constr"]
    return {"nom": nom, "ventes": ventes, "cac": u["cac"], "marge_nette": u["marge_nette"], "heures": heures,
            "resultat_mensuel": mensuel, "par_heure": mensuel / heures if heures else None, "resultat_horizon": horizon,
            "par_heure_horizon": horizon / h_total if h_total else None}


def mensuel_realiste(p):
    return p["ventes"] * par_vente(p)["marge_nette"] - p["fixes"]


def bascule(p, s):
    """Seuils qui font changer le verdict : ventes pour l'objectif, prix minimum pour une marge nette > minimum."""
    mn = par_vente(p)["marge_nette"]
    pente = par_vente(p, prix=p["prix"] + 1)["marge_nette"] - mn  # la marge nette est linéaire en prix
    return {"ventes_objectif": (s["objectif"] + p["fixes"]) / mn if mn > 0 else None,
            "prix_minimum": p["prix"] + (s["marge_min"] - mn) / pente if pente > 0 else None}


def poids_hypotheses(p):
    """Pour chaque entrée HYPOTHÈSE, INCONNU ou non étiquetée : écart du résultat mensuel réaliste à ±20 %."""
    inv = {k: cle for k, (cle, _) in CHAMPS.items()}
    out = []
    for e in p["entrees"]:
        if e["etiquette"] in ("VÉRIFIÉ", "ESTIMÉ") or not e["valeur"]:
            continue
        cle, k = inv[e["champ"]], e["plage"] / 100
        bas, haut = (mensuel_realiste({**p, cle: e["valeur"] * m}) for m in (1 - k, 1 + k))
        out.append({"champ": e["champ"], "etiquette": e["etiquette"], "bas": min(bas, haut), "haut": max(bas, haut),
                    "ecart": abs(haut - bas), "plage": e["plage"]})
    return sorted(out, key=lambda x: -x["ecart"])


def calculer(p):
    base, s = par_vente(p), p["seuils"]
    scs = [scenario(p, nom, *m) for nom, m in p["scenarios"].items()]
    prudent, realiste = scs[0], scs[1]
    mn = base["marge_nette"]
    point_mort = p["fixes"] / mn if mn > 0 else None
    recup = p["invest"] / realiste["resultat_mensuel"] if realiste["resultat_mensuel"] > 0 else None
    # 0 vente : la pub engagée (coût d'acquisition x ventes visées) est dépensée quand même ; et jamais moins que le pire scénario
    pub = p["cac"] * p["ventes"]
    perte_max = max(p["invest"] + (p["fixes"] + pub) * p["horizon"], *(-c["resultat_horizon"] for c in scs))
    sens = []
    for lib, prix, cac in (("prix -10%", p["prix"] * 0.9, None), ("prix +10%", p["prix"] * 1.1, None),
                           ("cac +30%", None, p["cac"] * 1.3), ("cac -30%", None, p["cac"] * 0.7)):
        u = par_vente(p, prix=prix, cac=cac)
        sens.append({"cas": lib, "marge_nette": u["marge_nette"],
                     "resultat_mensuel": p["ventes"] * u["marge_nette"] - p["fixes"]})
    plafond = None if s["plafond"] is None else float(s["plafond"])
    # arbre de décision : la première règle vraie donne le verdict (même ordre que SKILL.md)
    regles = [
        ("STOP", mn <= s["marge_min"], "marge nette unitaire %.2f <= %.2f : chaque vente perd ou ne rapporte rien" % (mn, s["marge_min"])),
        ("STOP", plafond is not None and perte_max > plafond, "perte maximale %.2f > plafond %s" % (perte_max, plafond)),
        ("PIVOT", point_mort is not None and point_mort > realiste["ventes"],
         "point mort %d ventes/mois > ventes du scénario réaliste %.0f" % (math.ceil(point_mort or 0), realiste["ventes"])),
        ("PIVOT", realiste["resultat_mensuel"] < s["objectif"],
         "résultat mensuel réaliste %.2f < objectif %.2f" % (realiste["resultat_mensuel"], s["objectif"])),
        ("PIVOT", plafond is not None and -prudent["resultat_horizon"] > plafond,
         "le scénario prudent perd %.2f sur l'horizon, plus que le plafond %s" % (-prudent["resultat_horizon"], plafond)),
        ("PIVOT", s["horaire_min"] > 0 and p["heures"] > 0 and realiste["par_heure"] < s["horaire_min"],
         "%.2f par heure en réaliste < minimum %.2f" % (realiste["par_heure"] or 0, s["horaire_min"])),
    ]
    verdict, raisons = next(((v, [r]) for v, ok, r in regles if ok),
                            ("CONTINUER", ["le scénario réaliste dépasse le point mort et tient les seuils"]))
    if verdict == "CONTINUER" and prudent["resultat_mensuel"] < 0:
        raisons.append("attention : le scénario prudent perd de l'argent chaque mois")
    if mn < 0:
        raisons.append("marge nette négative : plus on vend, plus on perd, le scénario « optimiste » est le pire")
    if p["min_vente"] == 0 and p["heures"]:
        raisons.append("heures fixes dans les 3 scénarios (minutes_par_vente pour qu'elles suivent les ventes)")
    fragiles = [e["champ"] for e in p["entrees"] if e["champ"] in DECISIVES and e["etiquette"] not in ("VÉRIFIÉ", "ESTIMÉ")]
    return {"par_vente": base, "scenarios": scs, "point_mort": point_mort, "recuperation_mois": recup,
            "perte_max": perte_max, "pub_mensuelle": pub, "bascule": bascule(p, s), "sensibilite": sens, "verdict": verdict, "raisons": raisons,
            "fragile": fragiles, "poids_hypotheses": poids_hypotheses(p),
            "non_etiquetes": [e["champ"] for e in p["entrees"] if e["etiquette"] == "non étiqueté" and e["champ"] != "horizon_mois"]}  # l'horizon est un choix, pas un fait


def md(p, r):
    f = lambda x: "-" if x is None else "%.2f" % x
    u = r["par_vente"]
    out = ["# Chiffrage : " + p["nom"], "",
           "Verdict du calculateur : **" + r["verdict"] + "** : " + " ; ".join(r["raisons"])]
    if r["fragile"]:
        out.append("Verdict FRAGILE : entrées décisives non vérifiées (" + ", ".join(r["fragile"]) + ").")
    if r["poids_hypotheses"]:
        h = r["poids_hypotheses"][0]
        out.append("Hypothèse qui pèse le plus (à tester en 72 h) : %s (%s), à ±%.0f %% le résultat mensuel va de %s à %s."
                   % (h["champ"], h["etiquette"], h["plage"], f(h["bas"]), f(h["haut"])))
    if r["non_etiquetes"]:
        out.append("A étiqueter : " + ", ".join(r["non_etiquetes"]) + ".")
    out += ["", "## Entrées", "| Champ | Valeur | Étiquette | Source |", "|---|---:|---|---|"]
    out += ["| %s | %s | %s | %s |" % (e["champ"], f(e["valeur"]), e["etiquette"], e["source"] or "-") for e in p["entrees"]]
    s = p["seuils"]
    out += ["", "Seuils : marge nette > %s ; plafond de perte %s ; objectif mensuel %s ; minimum par heure %s"
            % (f(s["marge_min"]), "-" if s["plafond"] is None else f(float(s["plafond"])), f(s["objectif"]), f(s["horaire_min"] or None)),
            "", "## Par vente", "| Poste | Montant |", "|---|---:|",
            "| Prix | " + f(u["prix"]) + " |", "| CA net (après retours) | " + f(u["ca_net"]) + " |",
            "| Achat + livraison | " + f(p["achat"] + p["livraison"]) + " |", "| Frais paiement/plateforme | " + f(u["frais"]) + " |",
            "| Marge avant pub | " + f(u["marge_avant_pub"]) + " |", "| Coût d'acquisition | " + f(u["cac"]) + " |",
            "| Cotisations (sur CA net) | " + f(u["cotisations"]) + " |", "| **Marge nette unitaire** | **" + f(u["marge_nette"]) + "** |", "",
            "## Scénarios (multiplicateurs HYPOTHÈSE)",
            "| Scénario | Ventes/mois | Coût acq. | Marge nette | Résultat mensuel | Heures/mois | Par heure | Sur %.0f mois (invest. inclus) | Par heure sur l'horizon |" % p["horizon"],
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for c in r["scenarios"]:
        out.append("| %s | %.0f | %s | %s | %s | %s | %s | %s | %s |" % (c["nom"], c["ventes"], f(c["cac"]), f(c["marge_nette"]), f(c["resultat_mensuel"]),
                                                                    f(c["heures"]), f(c["par_heure"]), f(c["resultat_horizon"]), f(c["par_heure_horizon"])))
    b = r["bascule"]
    out += ["", "Point mort (ventes/mois) : " + ("jamais (marge nette <= 0)" if r["point_mort"] is None else "%d" % math.ceil(r["point_mort"])),
            "Récupération de l'investissement (scénario réaliste, mois) : " + ("jamais" if r["recuperation_mois"] is None else "%.1f" % r["recuperation_mois"]),
            "Perte maximale : " + f(r["perte_max"]) + " (le plus grand de : invest. + (fixes + pub engagée %s/mois) x horizon à 0 vente, et la perte du pire scénario)" % f(r["pub_mensuelle"]),
            "Seuils de bascule : ventes/mois pour l'objectif " + ("jamais" if b["ventes_objectif"] is None else "%d" % math.ceil(b["ventes_objectif"]))
            + " ; prix minimum pour une marge nette > seuil " + ("-" if b["prix_minimum"] is None else f(b["prix_minimum"])), "",
            "## Sensibilité (volume réaliste)", "| Cas | Marge nette | Résultat mensuel |", "|---|---:|---:|"]
    out += ["| %s | %s | %s |" % (c["cas"], f(c["marge_nette"]), f(c["resultat_mensuel"])) for c in r["sensibilite"]]
    return "\n".join(out)


def test():
    """Auto-contrôle : cas de l'exemple (chiffres de la 1.0 inchangés) et une branche par verdict."""
    base = {"prix": 4.0, "cout_achat": 1.2, "livraison": 1.3, "frais_pct": 2.0, "frais_fixe": 0.25, "taux_retours_pct": 3,
            "cac": 0.5, "taux_cotisations_pct": 10, "couts_fixes_mensuels": 30, "investissement": 100,
            "ventes_mensuelles": 40, "horizon_mois": 3, "budget_plafond": 300}
    r = calculer(lire(base))
    assert r["verdict"] == "PIVOT" and round(r["point_mort"]) == 185 and abs(r["par_vente"]["marge_nette"] - 0.1624) < 1e-3, r
    # banc 20/11 : la pub engagée compte dans la perte à 0 vente (avant : 100 + 30 x 3 = 190 ; après : 100 + (30 + 0,5 x 40) x 3 = 250)
    assert round(r["scenarios"][1]["resultat_horizon"], 2) == -170.56 and r["perte_max"] == 250, r["perte_max"]
    assert calculer(lire({**base, "prix": 2.5}))["verdict"] == "STOP"  # marge nette négative
    assert calculer(lire({**base, "budget_plafond": 200}))["verdict"] == "STOP"  # perte max 250 > 200
    ok = {**base, "prix": 8.0, "budget_plafond": 1000}
    assert calculer(lire(ok))["verdict"] == "CONTINUER"
    assert calculer(lire({**ok, "seuils": {"objectif_mensuel": 500}}))["verdict"] == "PIVOT"
    assert calculer(lire({**ok, "heures_par_mois": 20, "seuils": {"horaire_min": 12}}))["verdict"] == "PIVOT"
    lab = {k: {"valeur": v, "etiquette": "VÉRIFIÉ", "source": "test"} for k, v in base.items() if k in CHAMPS}
    r = calculer(lire({**lab, "budget_plafond": 200, "ventes_mensuelles": {"valeur": 40, "etiquette": "HYPOTHÈSE"}}))
    assert r["fragile"] == ["ventes_mensuelles"] and r["poids_hypotheses"][0]["champ"] == "ventes_mensuelles"
    # banc 20/11 : prix et ventes en HYPOTHÈSE, c'est le volume (±50 %) qui pèse le plus, pas le prix à ±20 %
    hyp = lambda v: {"valeur": v, "etiquette": "HYPOTHÈSE"}
    r = calculer(lire({**ok, "prix": hyp(8.0), "ventes_mensuelles": hyp(40)}))
    assert r["poids_hypotheses"][0]["champ"] == "ventes_mensuelles", r["poids_hypotheses"]
    # heures qui suivent les ventes ; mois sans revenu ; panier de 2 articles ; marge négative signalée ; seuils de bascule
    r = calculer(lire({**ok, "heures_par_mois": 5, "minutes_par_vente": 15}))
    assert [c["heures"] for c in r["scenarios"]] == [10, 15, 20], r["scenarios"]
    r0, r2 = calculer(lire(ok)), calculer(lire({**ok, "mois_sans_revenu": 2}))
    assert round(r2["scenarios"][1]["resultat_horizon"] - r0["scenarios"][1]["resultat_horizon"], 6) == round(-2 * r0["scenarios"][1]["resultat_mensuel"] - 2 * 30, 6)
    u1, u2 = calculer(lire(ok))["par_vente"], calculer(lire({**ok, "articles_par_commande": 2}))["par_vente"]
    assert u2["prix"] == 16 and round(u2["marge_avant_pub"] - u1["marge_avant_pub"], 6) == round(8 * 0.97 - 1.2 - 8 * 0.02, 6)
    assert any("le pire" in x for x in calculer(lire({**base, "prix": 2.5}))["raisons"])
    b = calculer(lire({**ok, "seuils": {"objectif_mensuel": 100}}))["bascule"]
    assert abs(par_vente(lire({**ok, "prix": b["prix_minimum"]}))["marge_nette"]) < 1e-9 and b["ventes_objectif"] > 0
    # banc 20/11 cas 06 : 1,44 vente affichée « 1 » ; une vente ne se coupe pas, on arrondit au-dessus
    p = lire({**ok, "seuils": {"objectif_mensuel": 1}})
    r = calculer(p)
    assert r["bascule"]["ventes_objectif"] % 1 > 0  # cas fractionnaire, sinon le test ne prouve rien
    assert ("l'objectif %d " % math.ceil(r["bascule"]["ventes_objectif"])) in md(p, r)
    print("test OK : 14 cas (exemple 1.0 aux chiffres identiques sauf perte max avec pub, STOP x2, PIVOT x3, CONTINUER, poids des hypothèses, heures, mois sans revenu, panier, marge négative, bascule, arrondi au-dessus)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        test()
        sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("Usage : python chiffrer.py entree.json [--json] | python chiffrer.py --test")
    with open(args[0], encoding="utf-8-sig") as fh:  # Windows (Notepad, PowerShell) ajoute souvent un BOM
        p = lire(json.load(fh))
    r = calculer(p)
    print(json.dumps(r, indent=2, ensure_ascii=False) if "--json" in sys.argv else md(p, r))
