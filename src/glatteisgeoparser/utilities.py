import re

GEO_STOPWORD_PRESETS = [
    "CANTONE ",
    "CANTON ",
    "CANTONS ",
    "CANTONES ",
    "CANTONI ",
    "CANTONS ",
    "KANTON ",
    "DES ",
    "DI ",
    "DELLA ",
    "DELLI ",
    "DELL'",
    "DEL ",
    "DEI ",
    "DEGLI ",
    "DE ",
    "ST. ",
    "D'",
]


def standardize_name(name: str) -> str:
    name = name.casefold()
    name = name.upper()
    for n in GEO_STOPWORD_PRESETS:
        name = name.removeprefix(n)
        name = name.strip()
    name = re.sub(r"(\(.*\))", "", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    return name
