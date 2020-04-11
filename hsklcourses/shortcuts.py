from .courses import get_courses


def get_angewandte_informatik_courses():
    return get_courses("Bachelor Angewandte Informatik")


def get_master_informatik_courses():
    return get_courses("Master Informatik", "Software Entwicklung")


def get_nachrichtentechnik_courses():
    return get_courses("Bachelor Elektrotechnik", "Nachrichtentechnik")
