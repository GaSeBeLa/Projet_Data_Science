> **QUAND LIRE** : on joue une fiche `EXP*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache EXP<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier EXP — Exploration des données (Partie 1)

**Ouvert.** le 2026-11-02.

**À quoi il sert.** Le PDF demande un diagnostic de la qualité et de la structure des
données, dans un notebook. Ce chantier le produit, sur un module testé que la Partie 2 réutilisera.

**Fait.** Rien. Ouvert le 2026-11-02, cadré en 4 fiches, `EXP1` à jouer.

**Session** : 1abb9954-636f-4727-aa4a-97bd9123c07f

## Le socle commun

**Choix de Seb** (Discord, 2026-11-02) : Data Science seul (l'audit SQL du Fil Rouge est
un autre chantier) ; module Python testé + notebook ; données de l'énoncé en lecture seule.

**Les données** — dossier `fixtures/annonces/` du Starter Pack du Fil Rouge, **lu en place**,
jamais copié ni modifié. Chemin par défaut, relatif à la racine du dépôt :
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/fixtures/annonces/` ;
réglable par la variable d'environnement `SMART_IMMO_DATA` (un coéquipier n'a pas la même arborescence).

| Fichier | Contenu mesuré le 2026-11-02 |
|---|---|
| `annonces.csv` | 2 556 lignes, 36 colonnes, UTF-8 **avec BOM** ; colonnes `contact.nom`, `contact.telephone`… aplaties |
| `json/annonce_NNNN.json` | 2 556 fichiers, un par annonce ; `contact` est un objet imbriqué ; clés absentes plutôt que vides |
| `recherches.csv` | 5 recherches : `reference`, `ville`, `type_bien`, `budget_max`, `surface_min`, `nb_pieces_min`, `criteres_souhaites`, `dpe_max` |

Lien entre sources : `annonces.recherche_ref` → `recherches.reference`.

**Le code** : paquet `smart_immo/` à la racine, tests dans `tests/`, notebooks dans `notebooks/`.
Le module **rend des DataFrame et des comptes** ; il n'affiche rien et ne trace rien : le
notebook appelle et trace. Lire tout en texte (`dtype=str`) : la conversion est un constat
de l'exploration, pas un préalable. Les tests tournent sur de **petits DataFrame construits
dans le test**, jamais sur le Starter Pack (un coéquipier sans les données doit pouvoir les lancer).

**Environnement** : `py -3` = Python 3.14.6, pandas 3.0.5, pytest 9.1.1, matplotlib 3.11.2,
scikit-learn 1.9.1, nbconvert 7.17.2 (mesuré le 2026-11-02). ⚠️ `python` seul lance un
3.12 **sans pandas**. Seaborn absent : ne pas l'utiliser.

**Hors chantier** : corriger quoi que ce soit (c'est la Partie 2), choisir une
problématique (Partie 3), l'audit de la base SQL du Fil Rouge.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `EXP1` | Charger les trois sources | rien |
| `EXP2` | Décrire chaque colonne | `EXP1` |
| `EXP3` | Chercher doublons, valeurs aberrantes et incohérences | `EXP1` |
| `EXP4` | Écrire le notebook de diagnostic | `EXP2`, `EXP3` |

`EXP2` et `EXP3` ne se touchent pas : jouables dans n'importe quel ordre.

---

<!-- FICHE:EXP1 -->
## EXP1 [x] — Charger les trois sources

**Session** : 29c1d8d8-d279-426a-a4f3-e3ac6c27d2d1
**Dépend de** : rien.
**Fichiers** : `smart_immo/__init__.py`, `smart_immo/load.py`, `tests/test_load.py`,
`requirements.txt`, `README.md`, `.gitignore` (neufs, sauf `README.md`) — et rien d'autre.

**Prompt**
Écris `smart_immo/load.py`. `data_dir()` rend le dossier des données (`SMART_IMMO_DATA`,
sinon le chemin relatif du socle) et lève une erreur claire s'il n'existe pas.
`load_annonces_csv`, `load_annonces_json` (aplatit `contact` en `contact.nom`… comme le
CSV, garde le nom du fichier source) et `load_recherches` rendent des DataFrame en texte.
`compare_sources(csv, json)` rend les écarts entre les deux, par `id` : annonces présentes
d'un seul côté, et valeurs différentes, colonne par colonne (vide CSV = clé absente JSON).
`requirements.txt` épingle les versions mesurées du socle. `README.md` : installer, poser
`SMART_IMMO_DATA`, lancer les tests. `.gitignore` : caches Python, `.ipynb_checkpoints`, `.venv`.

**Critère de fin**
`py -3 -m pytest -q` vert, compte affiché, avec des tests sur DataFrame construits : BOM
retiré, contact JSON aplati, clé absente = vide, écart détecté. Mutant : faire ignorer à
`compare_sources` une colonne → un test tombe. Puis, sur les vraies données, afficher les
comptes de `compare_sources` (annonces seules d'un côté, valeurs différentes), sans les juger.
<!-- /FICHE -->

---

<!-- FICHE:EXP2 -->
## EXP2 [ ] — Décrire chaque colonne

**Dépend de** : `EXP1`.
**Fichiers** : `smart_immo/profile.py`, `tests/test_profile.py` (neufs) — et rien d'autre.

**Prompt**
Écris `profile_columns(df)` : une ligne par colonne avec son nombre de valeurs, son **taux
de vides** (vide ou blanc = vide), son nombre de valeurs distinctes, et sa **nature
devinée** — numérique, catégorielle, temporelle, texte libre ou booléenne — par une règle
écrite dans la docstring (ex. : > 90 % des non-vides convertibles en nombre). Ajoute
`format_variants(series)` qui compte les **formats** d'une colonne : pour `prix`, nombre
nu contre nombre suivi de `€` ; pour `date_publication`, timestamp, ISO, `JJ/MM/AAAA`,
« 25 octobre 2024 »… Chaque motif reconnu et un « autre » qui garde des exemples.
Rien n'est corrigé : on compte.

**Critère de fin**
`py -3 -m pytest -q` vert, compte affiché ; tests sur un DataFrame construit avec un vide,
un blanc, un prix en `€` et trois formats de date. Mutant : compter un blanc comme rempli
→ un test tombe. Sur les vraies données : le tableau de `profile_columns` affiché, brut.
<!-- /FICHE -->

---

<!-- FICHE:EXP3 -->
## EXP3 [ ] — Chercher doublons, valeurs aberrantes et incohérences

**Dépend de** : `EXP1`.
**Fichiers** : `smart_immo/quality.py`, `tests/test_quality.py` (neufs) — et rien d'autre.

**Prompt**
Écris trois familles de contrôles, chacun rend les lignes fautives et leur compte.
`find_duplicates` : doublons exacts, et **même annonce sous deux `id`** (mêmes ville,
type, surface, prix, adresse — la clé est écrite dans la docstring). `find_outliers` :
par la règle de l'écart interquartile (1,5 × IQR) sur `prix` et `surface`, par type de
bien. `find_inconsistencies` : règles métier listées une à une — `surface` ≠ `surface_m2`
quand les deux sont remplies, `nb_chambres` > `nb_pieces`, prix ou surface ≤ 0, code
postal qui ne va pas avec la ville, `recherche_ref` absente de `recherches.csv`.
Chaque règle a un nom court ; aucune n'est appliquée sans être nommée.

**Critère de fin**
`py -3 -m pytest -q` vert, compte affiché ; un test par règle, sur DataFrame construit.
Mutant : retirer la règle `nb_chambres > nb_pieces` → son test tombe. Sur les vraies
données : le compte de chaque règle affiché, brut.
<!-- /FICHE -->

---

<!-- FICHE:EXP4 -->
## EXP4 [ ] — Écrire le notebook de diagnostic

**Dépend de** : `EXP2`, `EXP3`.
**Fichiers** : `notebooks/01_exploration.ipynb` (neuf), `README.md` — et rien d'autre.

**Prompt**
Le notebook suit les 7 points de la Partie 1 du PDF, une section chacun : fichiers et rôle,
colonnes et volumes, natures des variables, taux de vides (graphique en barres), doublons
et valeurs aberrantes et incohérences, liens entre sources (annonces par recherche), puis
**les principales observations**. Chaque cellule de code appelle `smart_immo` ; aucun
calcul n'est recopié dans le notebook. Chaque observation écrite cite le compte affiché
juste au-dessus, jamais un chiffre tapé à la main. Graphiques matplotlib, fond clair.
Le dépôt est **public** : aucune sortie n'affiche de colonne `contact.*` ou `adresse`
ligne par ligne — seulement des comptes.
`README.md` : comment rouvrir et réexécuter le notebook.

**Critère de fin**
`py -3 -m jupyter nbconvert --to notebook --execute notebooks/01_exploration.ipynb` sans
erreur ; `py -3 -m pytest -q` toujours vert. Seb ouvre le notebook et lit les observations.
<!-- /FICHE -->
