import pathlib

from hsklcourses.courses import create_folder_structure
from hsklcourses.shortcuts import (
    get_master_informatik_courses,
    get_angewandte_informatik_courses,
    get_nachrichtentechnik_courses,
)


def main():
    ai = get_angewandte_informatik_courses()
    i = get_master_informatik_courses()
    nt = get_nachrichtentechnik_courses()

    create_folder_structure(ai, pathlib.Path("Bachelor Angewandte Informatik"))
    create_folder_structure(i, pathlib.Path("Master Informatik"))
    create_folder_structure(nt, pathlib.Path("Bachelor Elektrotechnik"))


if __name__ == "__main__":
    main()
