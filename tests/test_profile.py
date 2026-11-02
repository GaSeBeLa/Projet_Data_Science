"""Tests du profil des colonnes (fiche EXP2).

Tous les tests construisent leurs propres petits DataFrame : ils ne lisent
jamais le Starter Pack.
"""

import math

import pandas as pd

from smart_immo import profile


def row_of(table: pd.DataFrame, column: str) -> dict:
    """Rend la ligne de `table` qui décrit `column`, en dictionnaire."""
    return table.set_index("column").loc[column].to_dict()


def sample_frame() -> pd.DataFrame:
    """Un petit jeu d'annonces : un vide, un blanc, un prix en €, trois formats de date."""
    return pd.DataFrame(
        {
            "prix": ["100000", "250000 €", "", "  ", "180000", None],
            "date_publication": [
                "2024-10-25",
                "25/10/2024",
                "1729850000",
                "25 octobre 2024",
                "2024-10-25T10:35:10",
                "09-02-2025",
            ],
            "meuble": ["True", "False", None, "True", "", "False"],
            "dpe": ["A", "B", "A", "C", "B", "A"],
        },
        dtype="object",
    )


def test_blank_counts_as_empty():
    """Un texte fait seulement d'espaces compte comme un vide."""
    table = profile.profile_columns(sample_frame())
    prix = row_of(table, "prix")
    assert prix["n_rows"] == 6
    assert prix["n_empty"] == 3
    assert prix["n_filled"] == 3
    assert prix["empty_rate"] == 0.5


def test_distinct_counts_filled_values_only():
    """Les valeurs distinctes se comptent sur les seules cases remplies."""
    table = profile.profile_columns(sample_frame())
    assert row_of(table, "dpe")["n_distinct"] == 3
    assert row_of(table, "meuble")["n_distinct"] == 2


def test_nature_guesses():
    """Chaque colonne de l'exemple reçoit la nature attendue."""
    table = profile.profile_columns(sample_frame())
    assert row_of(table, "prix")["nature"] == "numérique"
    assert row_of(table, "date_publication")["nature"] == "temporelle"
    assert row_of(table, "meuble")["nature"] == "booléenne"
    assert row_of(table, "dpe")["nature"] == "catégorielle"


def test_free_text_when_many_distinct_values():
    """Plus de valeurs distinctes que le seuil des catégories : texte libre."""
    df = pd.DataFrame({"titre": [f"Bel appartement n°{i}" for i in range(60)]})
    table = profile.profile_columns(df)
    assert row_of(table, "titre")["nature"] == "texte libre"


def test_numeric_needs_more_than_ninety_percent():
    """Une colonne à 50 % de nombres n'est pas numérique."""
    df = pd.DataFrame({"etage": ["1", "2", "RDC", "dernier étage"]})
    table = profile.profile_columns(df)
    etage = row_of(table, "etage")
    assert etage["nature"] == "catégorielle"


def test_nature_share_shown_beside_verdict():
    """La part des valeurs qui collent à la nature s'affiche à côté du verdict."""
    table = profile.profile_columns(sample_frame())
    assert row_of(table, "prix")["nature_share"] == 1.0
    assert math.isnan(row_of(table, "dpe")["nature_share"])


def test_all_empty_column():
    """Une colonne sans aucune valeur remplie a la nature « vide »."""
    df = pd.DataFrame({"cave": [None, "", " "]}, dtype="object")
    cave = row_of(profile.profile_columns(df), "cave")
    assert cave["nature"] == "vide"
    assert cave["empty_rate"] == 1.0
    assert cave["n_distinct"] == 0


def test_zero_rows():
    """Un DataFrame sans ligne : taux de vides indéfini (NaN), nature « vide »."""
    df = pd.DataFrame({"prix": pd.Series([], dtype="object")})
    prix = row_of(profile.profile_columns(df), "prix")
    assert prix["n_rows"] == 0
    assert math.isnan(prix["empty_rate"])
    assert prix["nature"] == "vide"


def counts_of(variants: pd.DataFrame) -> dict[str, int]:
    """Rend `{format: nombre}` depuis le tableau de `format_variants`."""
    return dict(zip(variants["format"], variants["count"]))


def test_price_formats():
    """Pour `prix` : nombre nu, nombre suivi de €, vide, et « autre »."""
    series = pd.Series(["100", "200 €", "300€", "abc", "", None], name="prix")
    variants = profile.format_variants(series)
    counts = counts_of(variants)
    assert counts["nombre nu"] == 1
    assert counts["nombre + €"] == 2
    assert counts["vide"] == 2
    assert counts["autre"] == 1
    other = variants.set_index("format").loc["autre", "examples"]
    assert other == ["abc"]


def test_date_formats():
    """Pour `date_publication` : chaque format reconnu, et l'inconnu dans « autre »."""
    dates = sample_frame()["date_publication"].tolist() + ["hier"]
    series = pd.Series(dates, name="date_publication")
    counts = counts_of(profile.format_variants(series))
    assert counts["ISO date"] == 1
    assert counts["ISO date + heure"] == 1
    assert counts["JJ/MM/AAAA"] == 1
    assert counts["MM-JJ-AAAA"] == 1
    assert counts["timestamp"] == 1
    assert counts["JJ mois AAAA"] == 1
    assert counts["autre"] == 1


def test_formats_sum_to_length():
    """Chaque valeur tombe dans un seul format : la somme vaut la longueur."""
    series = pd.Series(["1", "2 €", "x", None, " "], name="prix")
    variants = profile.format_variants(series)
    assert variants["count"].sum() == len(series)


def test_explicit_patterns_override_column_name():
    """Des motifs passés en argument priment sur ceux du nom de colonne."""
    series = pd.Series(["RDC", "3", "RDC"], name="etage")
    variants = profile.format_variants(series, {"rez-de-chaussée": r"RDC"})
    assert counts_of(variants) == {"rez-de-chaussée": 2, "autre": 1, "vide": 0}
