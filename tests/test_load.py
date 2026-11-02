"""Tests du chargement des sources (fiche EXP1).

Tous les tests construisent leurs propres petites données dans un dossier
temporaire : ils ne lisent jamais le Starter Pack.
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from smart_immo import load


def write_json(folder: Path, name: str, record: dict) -> None:
    """Écrit une annonce JSON dans `folder`, sous le nom `name`."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(json.dumps(record), encoding="utf-8")


# --- data_dir ---------------------------------------------------------------


def test_data_dir_reads_environment_variable(tmp_path, monkeypatch):
    monkeypatch.setenv("SMART_IMMO_DATA", str(tmp_path))
    assert load.data_dir() == tmp_path


def test_data_dir_missing_folder_raises_clear_error(tmp_path, monkeypatch):
    missing = tmp_path / "absent"
    monkeypatch.setenv("SMART_IMMO_DATA", str(missing))
    with pytest.raises(FileNotFoundError, match="SMART_IMMO_DATA"):
        load.data_dir()


# --- load_annonces_csv ------------------------------------------------------


def test_csv_bom_removed_and_all_text(tmp_path):
    path = tmp_path / "annonces.csv"
    path.write_text("id,prix,ville\n1,100,Lyon\n2,,NA\n", encoding="utf-8-sig")
    df = load.load_annonces_csv(path)
    assert list(df.columns) == ["id", "prix", "ville"]
    assert df.loc[0, "prix"] == "100"
    # Seule une case vide est manquante : « NA » reste un texte.
    assert pd.isna(df.loc[1, "prix"])
    assert df.loc[1, "ville"] == "NA"


# --- load_annonces_json -----------------------------------------------------


def test_json_contact_flattened_like_csv(tmp_path):
    write_json(
        tmp_path,
        "annonce_0001.json",
        {
            "id": "a",
            "prix": 100,
            "meuble": True,
            "latitude": 43.5,
            "photos": ["u1", "u2"],
            "contact": {"nom": "Claire", "telephone": "04"},
        },
    )
    df = load.load_annonces_json(tmp_path)
    row = df.iloc[0]
    assert row["contact.nom"] == "Claire"
    assert row["contact.telephone"] == "04"
    assert "contact" not in df.columns
    assert row["prix"] == "100"
    assert row["meuble"] == "True"
    assert row["latitude"] == "43.5"
    assert row["photos"] == "u1; u2"
    assert row["source_file"] == "annonce_0001.json"


def test_json_missing_key_is_missing_value(tmp_path):
    write_json(tmp_path, "annonce_0001.json", {"id": "a", "prix": 1})
    write_json(tmp_path, "annonce_0002.json", {"id": "b"})
    df = load.load_annonces_json(tmp_path).set_index("id")
    assert pd.isna(df.loc["b", "prix"])


# --- load_recherches --------------------------------------------------------


def test_recherches_loaded_as_text(tmp_path):
    path = tmp_path / "recherches.csv"
    path.write_text("reference,budget_max\nREC-1,406100\n", encoding="utf-8")
    df = load.load_recherches(path)
    assert df.loc[0, "budget_max"] == "406100"


# --- compare_sources --------------------------------------------------------


def make_sources():
    """Rend un couple (csv, json) construit à la main, avec des écarts connus."""
    csv = pd.DataFrame(
        {
            "id": ["a", "b", "c"],
            "prix": ["100", "200", "300"],
            "ville": ["Lyon", pd.NA, "Nice"],
        }
    )
    json_df = pd.DataFrame(
        {
            "id": ["a", "b", "d"],
            "prix": ["100", "250", "400"],
            "ville": ["Lyon", pd.NA, "Pau"],
            "source_file": ["f1", "f2", "f4"],
        }
    )
    return csv, json_df


def test_compare_finds_ids_on_one_side_only():
    csv, json_df = make_sources()
    result = load.compare_sources(csv, json_df)
    assert result.only_csv == ["c"]
    assert result.only_json == ["d"]


def test_compare_finds_differing_values():
    csv, json_df = make_sources()
    diffs = load.compare_sources(csv, json_df).diffs
    assert diffs.to_dict("records") == [
        {"id": "b", "column": "prix", "csv_value": "200", "json_value": "250"}
    ]


def test_compare_empty_csv_equals_absent_json_key():
    csv = pd.DataFrame({"id": ["a"], "prix": ["1"], "cave": [pd.NA]})
    json_df = pd.DataFrame({"id": ["a"], "prix": ["1"]})
    assert load.compare_sources(csv, json_df).diffs.empty


def test_compare_checks_every_column():
    csv = pd.DataFrame({"id": ["a"], "prix": ["1"], "ville": ["Lyon"]})
    json_df = pd.DataFrame({"id": ["a"], "prix": ["1"], "ville": ["Nice"]})
    diffs = load.compare_sources(csv, json_df).diffs
    assert diffs["column"].tolist() == ["ville"]


def test_compare_rejects_duplicate_ids():
    csv = pd.DataFrame({"id": ["a", "a"], "prix": ["1", "2"]})
    json_df = pd.DataFrame({"id": ["a"], "prix": ["1"]})
    with pytest.raises(ValueError, match="dupliqu"):
        load.compare_sources(csv, json_df)
