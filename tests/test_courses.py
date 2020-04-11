import pathlib
import shutil

from hsklcourses.courses import (
    get_courses,
    as_sorted_dataframe,
    create_folder_structure,
)
from hsklcourses.shortcuts import (
    get_angewandte_informatik_courses,
    get_master_informatik_courses,
    get_nachrichtentechnik_courses,
)


def test_angewandte_informatik():
    courses = get_courses("Bachelor Angewandte Informatik")
    assert courses[0]["modul"] == "Grundlagen der Informatik (GDI)"
    assert courses[0]["semester"] == "1"


def test_nachrichtentechnik():
    courses = get_courses("Bachelor Elektrotechnik", "Nachrichtentechnik")
    assert courses[0]["modul"] == "Analysis 1"
    assert courses[0]["semester"] == "1"


def test_master_informatik():
    courses = get_courses("Master Informatik", "Software Entwicklung")
    assert courses[0]["modul"] == "Automaten, Berechenbarkeit und Komplexität (ABK)"
    assert courses[0]["semester"] == "1"


def test_shorcuts():
    ai = get_angewandte_informatik_courses()
    i = get_master_informatik_courses()
    nt = get_nachrichtentechnik_courses()

    ai_df = as_sorted_dataframe(ai)
    i_df = as_sorted_dataframe(i)
    nt_df = as_sorted_dataframe(nt)

    assert ai_df.semester.min() == "1"
    assert i_df.semester.min() == "1"
    assert nt_df.semester.min() == "1"

    assert ai_df.semester.max() == "6"
    assert i_df.semester.max() == "3"
    assert nt_df.semester.max() == "7"


def test_create_folder_structure():
    ai = get_angewandte_informatik_courses()
    i = get_master_informatik_courses()
    nt = get_nachrichtentechnik_courses()

    assert not pathlib.Path("test_data", "Bachelor Angewandte Informatik").exists()
    assert not pathlib.Path("test_data", "Master Informatik").exists()
    assert not pathlib.Path("test_data", "Bachelor Elektrotechnik").exists()

    create_folder_structure(
        ai, pathlib.Path("test_data", "Bachelor Angewandte Informatik")
    )
    create_folder_structure(i, pathlib.Path("test_data", "Master Informatik"))
    create_folder_structure(nt, pathlib.Path("test_data", "Bachelor Elektrotechnik"))

    assert pathlib.Path("test_data", "Bachelor Angewandte Informatik").exists()
    assert pathlib.Path("test_data", "Master Informatik").exists()
    assert pathlib.Path("test_data", "Bachelor Elektrotechnik").exists()

    assert pathlib.Path(
        "test_data",
        "Bachelor Angewandte Informatik",
        "Grundlagen der Informatik (GDI)",
        "Skript",
    ).exists()

    assert pathlib.Path(
        "test_data",
        "Bachelor Angewandte Informatik",
        "Projektmanagement (PM)",
        "Uebungen",
    ).exists()

    assert pathlib.Path(
        "test_data",
        "Bachelor Angewandte Informatik",
        "Anwendung und Programmierung von Mikrocontrollern (APM)",
        "Code",
    ).exists()

    shutil.rmtree("test_data/")

    assert not pathlib.Path("test_data").exists()
