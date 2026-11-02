# Exploration des données — notes et journal
## Résultat
Un notebook de diagnostic qui suit les 7 points de la Partie 1 du PDF, chaque observation appuyée sur un compte calculé par le module smart_immo testé.
## Notes
- EXP1 : Le module charge le CSV, les JSON et les recherches, et compare CSV et JSON. Ne dépend de rien.
- EXP2 : Le profil de chaque colonne : nature, taux de vides, formats mélangés. Dépend de EXP1.
- EXP3 : Les doublons, les valeurs aberrantes et les incohérences métier, une règle nommée par contrôle. Dépend de EXP1.
- EXP4 : Le notebook de diagnostic, qui appelle le module et ne recopie aucun calcul. Dépend de EXP2 et EXP3.
## Journal
## Bilan
