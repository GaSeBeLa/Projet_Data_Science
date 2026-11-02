# Exploration des données — notes et journal
## Résultat
Un notebook de diagnostic qui suit les 7 points de la Partie 1 du PDF, chaque observation appuyée sur un compte calculé par le module smart_immo testé.
## Notes
- EXP1 : pytest 11 passed ; mutant tué (1 failed) ; vraies données : CSV 2556x36, JSON 2556x37, recherches 5x11 ; seules CSV 0, seules JSON 0 ; 124 valeurs différentes, toutes photos (CSV vide, JSON liste vide)
- EXP2 : Le profil de chaque colonne : nature, taux de vides, formats mélangés. Dépend de EXP1.
- EXP3 : Les doublons, les valeurs aberrantes et les incohérences métier, une règle nommée par contrôle. Dépend de EXP1.
- EXP4 : Le notebook de diagnostic, qui appelle le module et ne recopie aucun calcul. Dépend de EXP2 et EXP3.
## Journal
## Bilan
