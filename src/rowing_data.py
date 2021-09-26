from typing import Optional
import functools as ft
import re

HEADER_RE = re.compile(r'^--([0-9]+),([0-9]+)$')
LINE_RE = re.compile(r'^([0-9]+\.[0-9]*|[0-9]*\.[0-9]+|[0-9]+)$')

class Day:
    km: float = 0
    descr: str = ''
    section_ind: int = -1
    persons_incl: dict[str, bool] = {}

    def __init__(self, person_init_state: dict[str, bool], km: float, section_ind: int, descr: str = None):
        self.km = km
        self.section_ind = section_ind
        if descr is None:
            self.descr = f'Day: {round(km)}km'
        else:
            self.descr = descr

        self.persons_incl = person_init_state.copy()

    def set_person_rowing(self, name: str, rowing: bool):
        self.persons_incl[name] = rowing

    def remove_person(self, name: str):
        try:
            del self.persons_incl[name]
        except KeyError:
            pass

    # ----------------------------------- Serialization ----------------------------------- 
    def to_dict(self) -> dict:
        return {
            'descr': self.descr,
            'km': self.km,
            'section_ind': self.section_ind,
            'persons_incl': self.persons_incl,
        }

    # ----------------------------------- Deserialization ----------------------------------- 
def day_from_dict(d: dict) -> Day:
    return Day(
        d['persons_incl'],
        d['km'],
        d['section_ind'],
        descr=d['descr'],
    )

class RowingData:
    person_days: list[Day] = []
    sections: list[int] = [] # index: identifier, int: persons not rowing
    persons: list[str] = []
    def __init__(self, person_days: list[Day] = None, sections: list[int] = None, persons: list[str] = None):
        if person_days is not None:
            self.person_days = person_days
        if sections is not None:
            self.sections = sections
        if persons is not None:
            self.persons = persons



    # ----------------------------------- Persons ----------------------------------- 
    def add_person(self, name: str):
        self.persons.append(name)
        for cday in self.person_days:
            cday.set_person_rowing(name, False)

    def set_person(self, name: str, day_ind: int, rowing: bool):
        self.person_days[day_ind].set_person_rowing(name, rowing)

    def set_person_rowing(self, name: str, day_ind: int, rowing: bool):
        self.person_days[day_ind].persons_incl[name] = rowing

    def delete_person(self, name: str):
        for cday in self.person_days:
            cday.remove_person(name)

    # ----------------------------------- Sections ----------------------------------- 
    def insert_section(self, insert_at: int, persons_not_rowing: int) -> int:
        self.sections.insert(insert_at, persons_not_rowing)
        abs_index: int = insert_at if insert_at >= 0 else len(self.sections) + insert_at
        print(f'Sections {self.sections} abs_index: {abs_index}')
        for cday in self.person_days:
            if cday.section_ind > abs_index:
                cday.section_ind += 1
            if cday.section_ind == -1:
                cday.section_ind = abs_index

        return abs_index

    def append_section(self, persons_not_rowing: int) -> int:
        return self.insert_section(-1, persons_not_rowing)
        #return len(self.sections)-1
    
    def delete_section(self, section_ind: int) -> tuple[int, list[Day]]:
        to_del = self.sections[section_ind]
        del self.sections[section_ind] # Delete section from list
        days_with_section: list[Day] = []
        for c_day in self.person_days:
            if c_day.section_ind > section_ind:
                c_day.section_ind -= 1
            elif c_day.section_ind == section_ind:
                days_with_section.append(c_day)

        return (to_del, days_with_section)

    # ----------------------------------- Days ----------------------------------- 
    # last_person_state: list[persons that are rowing]?
    def insert_day(self, km: float, persons_init_state: dict[str, bool] = None, section_index: int = -1, day_index: int = -1) -> int:
        if persons_init_state is None:
            persons_init_state = {}
            for cperson in self.persons:
                persons_init_state[cperson] = True
        day_index = len(self.persons)-1 if day_index == -1 else day_index

        self.person_days.insert(day_index, Day(persons_init_state, km, section_index))
        return day_index

    def delete_day(self, day_index: int) -> Optional[Day]:
        try:
            to_del = self.person_days[day_index]
            del self.person_days[day_index]
            return to_del
        except IndexError:
            pass

        return None

    def get_all_sections(self) -> list[int]:
        return self.sections

    
    # ----------------------------------- Serialization ----------------------------------- 
    def to_dict(self) -> dict:
        return {
            'person_days': list(map(lambda c: c.to_dict(), self.person_days)),
            'sections': self.sections,
            'persons': self.persons,
        }
    # ----------------------------------- Deserialization ----------------------------------- 
def rowing_data_from_dict(d: dict) -> RowingData:
    return RowingData(
        person_days=list(map(lambda c: day_from_dict(c), d['person_days'])),
        sections=d['sections'],
        persons=d['persons'],
    )


