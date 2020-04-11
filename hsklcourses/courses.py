import json
import pathlib
import re

import pandas
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://campusboard.hs-kl.de/portalapps/sv/ModulAnsicht.do"

studiengaenge_ids = {
    "Bachelor Angewandte Informatik": 213,
    "Master Informatik": 482,
    "Bachelor Elektrotechnik": 312,
}

schwerpunkte_ids = {
    "Nachrichtentechnik": 324,
    "Software Entwicklung": 308,
}


def construct_data_source_url(studiengang, schwerpunkt=None):
    url = f"{BASE_URL}?stgid={studiengaenge_ids.get(studiengang)}"

    if schwerpunkt:
        url = f"{url}&cspkt_id={schwerpunkte_ids.get(schwerpunkt)}"

    return url


def get_courses(studiengang, schwerpunkt=None):
    if studiengang not in studiengaenge_ids:
        raise ValueError(f"Error: Unknown Studiengang {studiengang}")

    if schwerpunkt and schwerpunkt not in schwerpunkte_ids:
        raise ValueError(f"Error: Unknown Schwerpunkt {schwerpunkt}")

    data_source_url = construct_data_source_url(studiengang, schwerpunkt)

    response = requests.get(data_source_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "border_collapse"})

    rows = table.findAll("tr")

    courses = []

    for row in rows:
        columns = row.findAll("td")

        if len(columns) == 6 or len(columns) == 7:
            course = [column.text.strip() for column in columns]
            courses.append(course)

    if len(courses[0]) == 6:
        headers = ["semester", "modulnr", "modul", "sws", "cp", "pdf"]
    else:
        headers = ["semester", "modulnr", "sp", "modul", "sws", "cp", "pdf"]

    courses_dict_list = [dict(zip(headers, course)) for course in courses]

    df = as_sorted_dataframe(courses_dict_list)
    courses_list = as_list(df)

    return courses_list


def pretty_print_coures(courses):
    print(json.dumps(courses, indent=2))


def as_sorted_dataframe(courses):
    return pandas.DataFrame(courses).sort_values(["semester", "modul"])[
        ["semester", "modul", "sws", "cp"]
    ]


def as_list(dataframe):
    return json.loads(dataframe.to_json(orient="records"))


def get_valid_filename(text):
    return re.sub("[^\w_.)( -]", "", text)


def create_folder_structure(courses, base_path=None):
    for course in courses:
        course_name = course.get("modul")
        folder_name = get_valid_filename(course_name)
        path = pathlib.Path(base_path if base_path else pathlib.Path(), folder_name)

        print(f"Creating {path}...")
        path.mkdir(parents=True, exist_ok=True)
        create_basic_subfolders(path)


def create_basic_subfolders(path, subfolders=None):
    if not subfolders:
        subfolders = ["Skript", "Uebungen", "Literatur", "Notizen", "Projekt", "Code"]

    for subfolder in subfolders:
        sub_path = pathlib.Path(path, subfolder)
        print(f"Creating subpath {sub_path}...")
        sub_path.mkdir(parents=True, exist_ok=True)
