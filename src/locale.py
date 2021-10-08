LOC_TEXT: dict[str, dict[str, str]] = {
    'de': {
        'title': 'KmCalc - Kilometer-Rechner für Wanderfahrten',
        'new_person': 'Neue Person',
        'new_section': 'Neuer Abschnitt',
        'section': 'Abschnitt',
        'section_id': 'Abschnitts-ID',
        'calc_km': 'Kilometer auswerten',

        'sect_id': 'Abschnitt ID',
        'sect_nrow': 'nicht rudernd',

        'day': 'Tag',
        'km_of_day': 'tägliche km',

        'new_sect': 'Neuer Abschnitt',
        'kms': 'Kilometer',
        'pers_not_rowing': 'nicht-rudernde personen',
        'sect_create_inv_title': 'Eingegebene Zahl ungültig',
        'sect_create_inv_msg': 'Der eingegebene Wert ist ungültig. Erneut eingeben?',

        'new_pers': 'Neue Person',
        'new_pers_name': 'Name',

        'new_day': 'Neuer Tag',
        'new_day_km': 'km',
    },
    'en': {
        'title': 'KmCalc - kilometre calculator for tours',
        'new_person': 'New person',
        'new_section': 'New section',
        'section': 'Section',
        'section_id': 'Section ID',
        'calc_km': 'analyze kilometers',

        'sect_id': 'Section',
        'sect_nrow': 'not rowing',

        'day': 'Day',
        'km_of_day': 'Daily km',

        'new_sect': 'new section',
        'kms': 'kilometers',

        'pers_not_rowing': 'not rowing',
        'sect_create_inv_title': 'Number invalid',
        'sect_create_inv_msg': 'The input number is invalid. Retry?',

        'new_pers': 'New Person',
        'new_pers_name': 'Name',

        'new_day': 'New Day',
        'new_day_km': 'km',
    }
}

DEFAULT_LOC: str = 'de'

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
