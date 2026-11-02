"""Profil des colonnes d'un DataFrame de texte (fiche EXP2).

On compte, on ne corrige rien : les valeurs restent telles que lues.
Le module rend des DataFrame ; il n'affiche rien.
"""

import math
import re
from collections.abc import Mapping

import pandas as pd

# Part minimale des cases remplies qui doivent coller à une nature
# (booléenne, temporelle, numérique) pour que la colonne la reçoive.
NATURE_THRESHOLD = 0.9

# Au plus ce nombre de valeurs distinctes : la colonne est catégorielle.
CATEGORY_MAX_DISTINCT = 50

BOOLEAN_WORDS = frozenset({"true", "false", "vrai", "faux", "oui", "non"})

# Un nombre (virgule ou point décimal), éventuellement suivi d'une unité.
NUMBER_PATTERN = re.compile(r"-?\d+(?:[.,]\d+)?\s*(?:€|m²|m2)?")

MONTHS_FR = (
    "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"
)

PRICE_FORMATS: dict[str, str] = {
    "nombre nu": r"\d+",
    "nombre + €": r"\d+\s*€",
}

# Le timestamp commence par 1 : secondes depuis 1970, entre 2001 et 2033.
# Cela évite de prendre un numéro de téléphone (0…) pour une date.
DATE_FORMATS: dict[str, str] = {
    "ISO date": r"\d{4}-\d{2}-\d{2}",
    "ISO date + heure": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
    "JJ/MM/AAAA": r"\d{2}/\d{2}/\d{4}",
    # Mesuré le 2026-11-02 sur les 402 dates à tirets du CSV : le 1er nombre
    # ne dépasse jamais 12, le 2e le dépasse 227 fois → mois avant jour.
    "MM-JJ-AAAA": r"\d{2}-\d{2}-\d{4}",
    "timestamp": r"1\d{9}",
    "JJ mois AAAA": rf"\d{{1,2}} (?:{MONTHS_FR}) \d{{4}}",
}

GENERIC_FORMATS: dict[str, str] = {
    "entier": r"-?\d+",
    "décimal": r"-?\d+[.,]\d+",
}

FORMATS_BY_COLUMN: dict[str, dict[str, str]] = {
    "prix": PRICE_FORMATS,
    "date_publication": DATE_FORMATS,
}

MAX_EXAMPLES = 3


def is_empty(value: object) -> bool:
    """Rend `True` si `value` est manquante (None, NaN, NA) ou un texte blanc.

    Un texte fait seulement d'espaces compte comme vide ; tout autre objet
    non manquant compte comme rempli.
    """
    if value is None or value is pd.NA:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return isinstance(value, str) and value.strip() == ""


def _filled(series: pd.Series) -> list[str]:
    """Rend les valeurs remplies de `series`, en texte, sans les retoucher."""
    return [str(v) for v in series.tolist() if not is_empty(v)]


def _share(values: list[str], test) -> float:
    """Rend la part de `values` qui passe `test` ; 0.0 pour une liste vide."""
    if not values:
        return 0.0
    return sum(1 for v in values if test(v)) / len(values)


def _is_boolean(value: str) -> bool:
    """Rend `True` si `value` est un mot booléen (`True`, `oui`…), casse ignorée."""
    return value.strip().lower() in BOOLEAN_WORDS


def _is_number(value: str) -> bool:
    """Rend `True` si `value` est un nombre, éventuellement suivi de `€` ou `m²`."""
    return NUMBER_PATTERN.fullmatch(value.strip()) is not None


def _is_date(value: str) -> bool:
    """Rend `True` si `value` colle à l'un des formats de `DATE_FORMATS`."""
    text = value.strip()
    return any(re.fullmatch(p, text) for p in DATE_FORMATS.values())


def guess_nature(values: list[str]) -> tuple[str, float]:
    """Devine la nature d'une colonne d'après ses valeurs remplies.

    Rend `(nature, part)`, la part étant celle des valeurs qui collent à la
    nature retenue. La règle, appliquée dans cet ordre :

    1. aucune valeur remplie → « vide » (part NaN) ;
    2. plus de 90 % de mots booléens (`True`, `False`, `oui`, `non`, `vrai`,
       `faux`, casse ignorée) → « booléenne » ;
    3. plus de 90 % de dates à l'un des formats de `DATE_FORMATS` →
       « temporelle » ;
    4. plus de 90 % de nombres, éventuellement suivis de `€` ou `m²` →
       « numérique » ;
    5. au plus 50 valeurs distinctes → « catégorielle » (part NaN) ;
    6. sinon → « texte libre » (part NaN).

    Les dates passent avant les nombres : un timestamp est aussi un nombre.
    """
    if not values:
        return "vide", math.nan
    for nature, test in (
        ("booléenne", _is_boolean),
        ("temporelle", _is_date),
        ("numérique", _is_number),
    ):
        share = _share(values, test)
        if share > NATURE_THRESHOLD:
            return nature, share
    if len(set(values)) <= CATEGORY_MAX_DISTINCT:
        return "catégorielle", math.nan
    return "texte libre", math.nan


def profile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rend une ligne par colonne de `df` : comptes, vides, distinctes, nature.

    Colonnes rendues : `column`, `n_rows`, `n_filled`, `n_empty`,
    `empty_rate`, `n_distinct` (sur les seules cases remplies, valeurs brutes),
    `nature` et `nature_share` (voir `guess_nature`).

    Un vide est une valeur manquante ou un texte blanc (`is_empty`).
    Un DataFrame sans ligne donne un `empty_rate` NaN et la nature « vide ».
    """
    rows = []
    for column, series in df.items():
        values = _filled(series)
        n_rows = len(series)
        n_empty = n_rows - len(values)
        nature, share = guess_nature(values)
        rows.append(
            {
                "column": column,
                "n_rows": n_rows,
                "n_filled": len(values),
                "n_empty": n_empty,
                "empty_rate": n_empty / n_rows if n_rows else math.nan,
                "n_distinct": len(set(values)),
                "nature": nature,
                "nature_share": share,
            }
        )
    return pd.DataFrame(rows)


def format_variants(
    series: pd.Series, patterns: Mapping[str, str] | None = None
) -> pd.DataFrame:
    """Compte les formats d'écriture des valeurs de `series`.

    Rend un DataFrame à trois colonnes : `format`, `count` et `examples`
    (jusqu'à trois valeurs distinctes, brutes). Une ligne par motif, dans
    l'ordre donné, même à zéro ; puis « autre » (rien ne colle) et « vide ».
    Chaque valeur tombe dans le premier motif qui la couvre en entier
    (espaces de bord ignorés) : la somme des comptes vaut `len(series)`.

    Sans `patterns`, les motifs viennent du nom de la série
    (`FORMATS_BY_COLUMN`), sinon de `GENERIC_FORMATS`.
    """
    if patterns is None:
        patterns = FORMATS_BY_COLUMN.get(str(series.name), GENERIC_FORMATS)
    compiled = {name: re.compile(p) for name, p in patterns.items()}
    counts: dict[str, int] = {name: 0 for name in [*compiled, "autre", "vide"]}
    examples: dict[str, list[str]] = {name: [] for name in counts}
    for value in series.tolist():
        if is_empty(value):
            counts["vide"] += 1
            continue
        text = str(value)
        found = next(
            (n for n, rx in compiled.items() if rx.fullmatch(text.strip())), "autre"
        )
        counts[found] += 1
        if len(examples[found]) < MAX_EXAMPLES and text not in examples[found]:
            examples[found].append(text)
    return pd.DataFrame(
        {
            "format": list(counts),
            "count": list(counts.values()),
            "examples": [examples[n] for n in counts],
        }
    )
