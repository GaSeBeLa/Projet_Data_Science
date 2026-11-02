# Projet_Data_Science — Smart Immo

Projet de groupe du cours ENGI IA : explorer, nettoyer et modéliser les
annonces immobilières de l'énoncé.

## Installer

Avec Python 3.14 (sous Windows : `py -3`) :

```bash
py -3 -m pip install -r requirements.txt
```

## Poser le dossier des données

Les données sont celles du Starter Pack du Fil Rouge, lues en place et jamais
copiées dans ce dépôt.

- Par défaut, le module cherche
  `../ProjetFileRouge/Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/fixtures/annonces/`,
  à côté de ce dépôt.
- Sinon, posez la variable d'environnement `SMART_IMMO_DATA` vers ce dossier
  `fixtures/annonces` :

```powershell
$env:SMART_IMMO_DATA = "<chemin vers>/fixtures/annonces"
```

```bash
export SMART_IMMO_DATA="<chemin vers>/fixtures/annonces"
```

## Lancer les tests

Depuis la racine du dépôt :

```bash
py -3 -m pytest -q
```

Les tests n'ont pas besoin des données : ils construisent leurs propres petits
exemples.
