"""Chargement des trois sources de l'énoncé, en texte, sans rien corriger.

Les sources vivent dans le Starter Pack du Fil Rouge, lu en place et jamais
modifié. Tout est lu en texte (`str`) : convertir les types est un constat de
l'exploration, pas un préalable. Ce module rend des DataFrame et des comptes ;
il n'affiche rien.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ENV_VAR = "SMART_IMMO_DATA"

# Chemin par défaut, relatif à la racine du dépôt (voisin du dépôt).
DEFAULT_RELATIVE_DIR = Path(
    "../ProjetFileRouge/Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/fixtures/annonces"
)

REPO_ROOT = Path(__file__).resolve().parents[1]

# Séparateur des listes dans le CSV (ex. la colonne `photos`).
LIST_SEPARATOR = "; "


def data_dir() -> Path:
    """Rend le dossier des données.

    Prend la variable d'environnement `SMART_IMMO_DATA` si elle est posée,
    sinon le chemin par défaut relatif à la racine du dépôt.

    Lève `FileNotFoundError` si le dossier n'existe pas, avec le chemin
    essayé et la variable à poser.
    """
    raw = os.environ.get(ENV_VAR)
    folder = Path(raw) if raw else (REPO_ROOT / DEFAULT_RELATIVE_DIR).resolve()
    if not folder.is_dir():
        raise FileNotFoundError(
            f"Dossier des données introuvable : {folder}. "
            f"Posez la variable d'environnement {ENV_VAR} vers le dossier "
            "fixtures/annonces du Starter Pack."
        )
    return folder


def _read_text_csv(path: Path) -> pd.DataFrame:
    """Lit un CSV en texte et rend un DataFrame.

    Le BOM éventuel est retiré (`utf-8-sig`). Seule une case vide devient
    une valeur manquante : « NA », « null » ou « None » restent du texte.
    """
    return pd.read_csv(
        path,
        dtype=str,
        encoding="utf-8-sig",
        keep_default_na=False,
        na_values=[""],
    )


def load_annonces_csv(path: Path | None = None) -> pd.DataFrame:
    """Rend `annonces.csv` en DataFrame de texte.

    Sans `path`, lit `annonces.csv` dans `data_dir()`. Une case vide est
    une valeur manquante.
    """
    return _read_text_csv(path or data_dir() / "annonces.csv")


def load_recherches(path: Path | None = None) -> pd.DataFrame:
    """Rend `recherches.csv` en DataFrame de texte.

    Sans `path`, lit `recherches.csv` dans `data_dir()`.
    """
    return _read_text_csv(path or data_dir() / "recherches.csv")


def _to_text(value: Any) -> str | None:
    """Rend une valeur JSON en texte, écrite comme dans le CSV.

    `None` reste `None` (manquant). Une liste devient ses éléments joints
    par `"; "`. Un booléen devient `"True"` ou `"False"`. Le reste passe
    par `str`.
    """
    if value is None:
        return None
    if isinstance(value, list):
        return LIST_SEPARATOR.join(str(item) for item in value)
    return str(value)


def _flatten(record: dict[str, Any], prefix: str = "") -> dict[str, str | None]:
    """Aplatit un objet JSON : `{"contact": {"nom": x}}` donne `contact.nom`.

    Rend un dict à un seul niveau, valeurs en texte. Un objet vide ne
    produit aucune colonne.
    """
    flat: dict[str, str | None] = {}
    for key, value in record.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(_flatten(value, prefix=f"{name}."))
        else:
            flat[name] = _to_text(value)
    return flat


def load_annonces_json(folder: Path | None = None) -> pd.DataFrame:
    """Rend les annonces JSON en un DataFrame de texte, une ligne par fichier.

    Sans `folder`, lit `data_dir() / "json"`. Les fichiers `*.json` sont lus
    dans l'ordre de leur nom. `contact` est aplati en `contact.nom`… comme
    dans le CSV ; une clé absente donne une valeur manquante. La colonne
    `source_file` garde le nom du fichier. Dossier sans JSON : DataFrame vide.
    """
    folder = folder or data_dir() / "json"
    rows = []
    for path in sorted(folder.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        row = _flatten(record)
        row["source_file"] = path.name
        rows.append(row)
    return pd.DataFrame(rows, dtype=str)


def _text_or_none(value: object) -> str | None:
    """Rend `value` si c'est un texte, sinon `None` (NaN, NA : valeur manquante)."""
    return value if isinstance(value, str) else None


@dataclass
class SourceComparison:
    """Écarts entre le CSV et les JSON, par `id`.

    - `only_csv` : ids présents dans le seul CSV, triés ;
    - `only_json` : ids présents dans les seuls JSON, triés ;
    - `diffs` : une ligne par valeur différente, colonnes
      `id`, `column`, `csv_value`, `json_value`.
    """

    only_csv: list[str]
    only_json: list[str]
    diffs: pd.DataFrame


def compare_sources(csv: pd.DataFrame, json_df: pd.DataFrame) -> SourceComparison:
    """Compare les annonces du CSV et des JSON, par `id`.

    Rend les ids présents d'un seul côté, et chaque valeur qui diffère,
    colonne par colonne, sur les ids communs. Une colonne absente d'un côté
    compte comme vide : une case vide du CSV égale une clé absente du JSON.
    `source_file` n'est pas comparée.

    Lève `ValueError` si un `id` est dupliqué d'un côté : la comparaison
    par `id` n'a alors pas de sens.
    """
    for name, frame in (("CSV", csv), ("JSON", json_df)):
        if frame["id"].duplicated().any():
            raise ValueError(f"ids dupliqués dans la source {name}")

    csv_ids = set(csv["id"])
    json_ids = set(json_df["id"])
    common = sorted(csv_ids & json_ids)

    columns = sorted((set(csv.columns) | set(json_df.columns)) - {"id", "source_file"})
    left = csv.set_index("id").reindex(index=common, columns=columns)
    right = json_df.set_index("id").reindex(index=common, columns=columns)

    left_rows = left.to_dict("index")
    right_rows = right.to_dict("index")

    records = []
    for id_ in common:
        for column in columns:
            # Manquant (NaN, NA) devient None des deux côtés : vide = absent.
            csv_value = _text_or_none(left_rows[id_][column])
            json_value = _text_or_none(right_rows[id_][column])
            if csv_value != json_value:
                records.append(
                    {
                        "id": id_,
                        "column": column,
                        "csv_value": csv_value,
                        "json_value": json_value,
                    }
                )

    diffs = pd.DataFrame(records, columns=["id", "column", "csv_value", "json_value"])
    return SourceComparison(
        only_csv=sorted(csv_ids - json_ids),
        only_json=sorted(json_ids - csv_ids),
        diffs=diffs,
    )
