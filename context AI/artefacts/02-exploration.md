# Exploration des données — notes et journal
## Résultat
Un notebook de diagnostic qui suit les 7 points de la Partie 1 du PDF, chaque observation appuyée sur un compte calculé par le module smart_immo testé.
## Notes
- EXP1 : pytest 11 passed ; mutant tué (1 failed) ; vraies données : CSV 2556x36, JSON 2556x37, recherches 5x11 ; seules CSV 0, seules JSON 0 ; 124 valeurs différentes, toutes photos (CSV vide, JSON liste vide)
- EXP2 : 24 passed ; mutant blanc→rempli : 4 failed ; pyright 0 errors ; 36 colonnes profilées ; prix : 2174 nombre nu, 382 nombre + € ; date_publication : 6 formats, 0 autre
- EXP3 : Les doublons, les valeurs aberrantes et les incohérences métier, une règle nommée par contrôle. Dépend de EXP1.
- EXP4 : Le notebook de diagnostic, qui appelle le module et ne recopie aucun calcul. Dépend de EXP2 et EXP3.
## Journal
- 2026-11-02 : EXP2 : les 402 dates à tirets sont en mois-jour-année (1er nombre > 12 : 0 fois, 2e : 227 fois) ; format nommé MM-JJ-AAAA, retouche du test autorisée par Seb
## Bilan
