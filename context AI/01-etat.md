> **QUAND LIRE** : on reprend après une longue interruption, on choisit le
> prochain chantier, ou on doute d'une décision passée. Les cinq lignes de
> `CLAUDE.md` suffisent dans la plupart des cas — ouvrir ceci seulement quand
> elles ne suffisent pas.

# État du projet — daté

## Où on en est

*(au 2026-11-02)*

- Dépôt `GaSeBeLa/Projet_Data_Science` créé par Gabriel ; un seul commit (`README.md`).
- Aucun code, aucun notebook.
- Données : `annonces.csv` (2 556 lignes, 36 colonnes), 2 556 JSON, `recherches.csv`
  (5 recherches), dans le Starter Pack du Fil Rouge, lu en place.
- Mesures de repérage (hors dépôt, à refaire dans le module) : corrélation prix ↔
  surface 0,04 ; prix médian château 105 000 € contre maison 259 000 € ; 43,4 % de
  cases vides en moyenne ; aucun `id` ni `reference` en double.
- Problématiques pressenties : B (qualification annonce ↔ recherche) la plus adaptée,
  A (prix) faisable mais faible, C (mandat vendu) sans données de ventes — à trancher
  en Partie 3, rien n'est décidé.

## La TODO ordonnée — les chantiers possibles

C'est d'ici que `/chantier` tire ses propositions. Un chantier par entrée,
ordonné par ce qui débloque le reste.

| # | Chantier | Ce qu'il apporte | Coût estimé | Dépend de |
|---|---|---|---|---|
| 1 | Exploration (Partie 1) | diagnostic de qualité et de structure, dans un notebook | 4 fiches | rien |
| 2 | Nettoyage et pipeline (Partie 2) | pipeline Scikit-learn reproductible, qualité avant/après, jeu préparé | 4–5 fiches | 1 |
| 3 | Problématiques métier (Partie 3) | deux problématiques justifiées : cible, variables, métrique, limites | 2 fiches | 1 |
| 4 | Benchmark des modèles (Partie 4) | modèles comparés sur un protocole commun, tableau, modèle retenu | 4–5 fiches | 2, 3 |
| 5 | Synthèse et oral (Partie 5), puis extensions | synthèse écrite, README ; FastAPI, Pydantic, TensorFlow en option | 3–5 fiches | 4 |

## Journal des décisions

Une ligne par décision imprévue tranchée en cours de fiche — jamais un résumé
de ce que le code dit déjà.

- **2026-11-02** — Seb (Discord) : chantier d'exploration limité au Data Science
  (l'audit SQL du Fil Rouge est un chantier à part) ; un dépôt à part ; module Python
  testé + notebook ; données de l'énoncé en lecture seule ; tout est versionné, le
  livrable pour la prof se fera à la fin.

- **2026-11-02** — EXP2 : les 402 dates à tirets de `date_publication` sont en
  **mois-jour-année** (1er nombre > 12 : 0 fois, 2e : 227 fois), celles à `/` en
  jour-mois ; format nommé « MM-JJ-AAAA ». Seb a autorisé la retouche du test (`987d628`).
