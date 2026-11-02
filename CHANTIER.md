# Chantier courant — Projet Data Science « Smart Immo »

> Fichier lu **en entier** par `/vlp:chantier` et `/vlp:tache`, depuis la racine du
> projet. C'est la seule table à tenir : rien à mettre à jour ailleurs quand un
> chantier s'ouvre ou se clôt. Garde-le sous le seuil de `scripts/vlp.py` : `renvois` avertit.
> Les libellés en gras se recopient **à l'identique** : ils sont lus tels quels.

- **alias** : ds
- **kit** : le plugin vlp — sans chemin de machine, ce fichier part dans Git
- **contexte** : context AI/
- **méthode** : methode-chantier.md, à la racine du kit — il voyage avec le plugin
- **chantiers possibles** : context AI/01-etat.md
- **fichier d'état** : context AI/01-etat.md
- **index** : context AI/00-INDEX.md
- **artefact feuille de route** : https://claude.ai/artifact/S19Mosvwg1zeVCgRnKa4aV
- **artefact du chantier** : https://claude.ai/artifact/JUhn7rpPzEFSskNSj5pRxr
- **artefact enchaînement** : aucun
- **livraison** : aucune — des notebooks et un module Python, rien à déployer
- **vérification** : `py -3 -m pytest -q`, depuis la racine du dépôt — la session la
  lance et lit son verdict
- **contexte dans Git** : oui — tranché par Seb sur Discord le 2026-11-02 ; le livrable
  propre pour la prof se fera à la fin du projet
- **commandes longues** : aucune


## Contraintes d'écriture

Les règles que toute fiche respecte, quel que soit son sujet. Trois ou quatre,
pas quinze — celles qu'on regrette de ne pas avoir écrites.

- **Le Starter Pack est en lecture seule** (`../ProjetFileRouge/Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/`) :
  jamais modifié, jamais copié dans ce dépôt ; on le lit par un chemin relatif réglable.
- **Aucun chiffre ni résultat inventé** : tout compte vient d'une mesure rejouable
  (consigne du PDF, § 7 « Ne présentez pas de performances non mesurées »).
- **Aucune fuite entre entraînement et test** : tout ce qui apprend des données
  (imputation, encodage, mise à l'échelle) s'ajuste sur le seul jeu d'entraînement.
- Prose et commentaires en français, noms de code en anglais ; aucun chemin absolu ni
  secret dans le code ; du Python touché passe `pyright` avant son commit.

## Chantiers clos — dans l'index, pas ici

Chacun a sa ligne dans l'**index** ; sa page reste sur la feuille de route.

Lettres de fiche déjà prises : EXP (Exploration des données). Un nouveau chantier en choisit un autre —
trois majuscules, jamais réemployées, même après clôture. `/vlp:chantier` le
propose, l'utilisateur tranche ; c'est cette ligne qui rend le refus possible.
