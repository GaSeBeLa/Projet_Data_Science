# Projet Data Science « Smart Immo » — à lire en premier, en entier, et seul

Projet de groupe du cours ENGI IA (Seb, Gabriel, amethyste) : transformer les annonces
immobilières brutes de l'énoncé en données propres, puis comparer des modèles de
Machine Learning sur deux problématiques métier. Ce n'est **pas** une appli en
production. Dépôt : [GaSeBeLa/Projet_Data_Science](https://github.com/GaSeBeLa/Projet_Data_Science).
Énoncé : `ProjetDataScience.pdf` (Python, Pandas, Scikit-learn ; extensions FastAPI,
Pydantic, TensorFlow). Données : le Starter Pack du Fil Rouge, voisin, en lecture seule.

## Où on en est — en cinq lignes

- Dépôt créé le 2026-11-02 par Gabriel, équipé de la méthode le même jour.
- Aucun code encore. Premier chantier : **EXP**, l'exploration (Partie 1 du PDF).
- Mesures déjà faites le 2026-11-02 sur `annonces.csv` (pandas, hors dépôt) : 2 556
  lignes, 36 colonnes, corrélation prix ↔ surface 0,04, 43,4 % de cases vides en moyenne.
  À refaire dans le module, elles ne valent pas résultat.
- Détail daté : `context AI/01-etat.md`.

## Quatre règles non négociables

1. **Annoncer le plan en une ou deux phrases avant d'agir**, et poser un
   questionnaire au moindre choix ouvert.
2. **Mesurer avant de corriger**, et afficher les comptes bruts à côté du
   verdict — un instrument muet rend son propre échec indiagnosticable.
3. **Aucun chiffre ni cible inventés** : une problématique irréalisable avec les
   données se dit et se justifie (PDF, Partie 3) ; le Starter Pack ne se modifie jamais.
4. **Aucun secret, aucun chemin absolu, aucune donnée du Starter Pack dans git.**

Prose et commentaires en français, noms de code en anglais.

## Routage — ouvrir ceci, et rien d'autre

Cette table remplace la lecture de `00-INDEX.md`. Si la tâche n'y figure pas,
et seulement dans ce cas, ouvrir l'index.

| La tâche | Ouvrir |
|---|---|
| ouvrir un chantier, ou le découper en fiches | **lancer `/vlp:chantier`** — la méthode vit dans le kit, pas ici |
| jouer une fiche du chantier EXP (exploration des données) | `context AI/02-exploration.md` — chantier **ouvert**, par `/vlp:tache EXP<n>` |
| relire un chantier clos | `context AI/00-INDEX-archive.md` — sa ligne y nomme le fichier de fiches |
| reprendre après une longue interruption | `context AI/01-etat.md` |

## Économie de contexte

La fenêtre sature par **densité de contexte**, pas par volume horaire. Donc,
dans cet ordre :

- **Un fichier de contexte ne s'ouvre que si la table ci-dessus le nomme.** Le
  voisin d'un fichier utile n'est pas utile ; il n'est que du volume.
- **Ne jamais lire le dossier de contexte en entier**, ni le README.
- **Une tâche, une session.** `/clear` entre deux tâches : une session laissée
  ouverte relit tout son passé à chaque tour.
- **Le coût est dans les tours, pas dans les lignes** : grouper les lectures
  en un appel, ne pas retaper ce qu'un script régénère.
- **Explorer et lire avec un modèle léger**, garder le lourd pour ce qui décide.
- Grep ciblé plutôt que lecture de fichier entier, dans le code comme ici.
