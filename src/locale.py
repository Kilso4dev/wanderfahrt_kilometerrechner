LOC_TEXT: dict[str, dict[str, str]] = {
    'de': {
        'title': 'KmCalc - Kilometer-Rechner für Wanderfahrten',
        'new_person': 'Neue Person',
        'new_section': 'Neuer Abschnitt',
        'section': 'Abschnitt',
        'calc_km': 'Kilometer auswerten',
        'test': 'Test',

        'sect_id': 'Abschnitt ID',
        'sect_nrow': 'nicht rudernd',
    },
    'en': {
        'title': 'KmCalc - kilometer calculator for tours',
        'new_person': 'New person',
        'new_section': 'New section',
        'section': 'Section',
        'calc_km': 'analyze kilometers',
        'test': 'Test',

        'sect_id': 'Section',
        'sect_nrow': 'not rowing',
    }
}

DEFAULT_LOC: str = 'en'

locale = DEFAULT_LOC

def l(k: str) -> str:
    try:
        return LOC_TEXT[locale][k]
    except KeyError:
        return k

def set_locale(new_loc: str):
    global locale
    for ck in LOC_TEXT.keys():
        if new_loc == ck:
            locale = new_loc

def get_available_locales() -> list[str]:
    return list(LOC_TEXT.keys())
