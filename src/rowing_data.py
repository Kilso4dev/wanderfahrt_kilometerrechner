from typing import Optional
import functools as ft
import re

HEADER_RE = re.compile(r'^--([0-9]+),([0-9]+)$')
LINE_RE = re.compile(r'^([0-9]+\.[0-9]*|[0-9]*\.[0-9]+|[0-9]+)$')


def calc_km_reduced(km_days: list[float], persons_all: int, persons_rowing: int):
    #def a(acc, c):
    #    print(f'c: {c} rounded c: {round(c)}')
    #    return acc+round(c)

    km_all = ft.reduce(lambda acc, c: acc+round(c), km_days, 0)
    #km_all = ft.reduce(a, km_days, 0)
    #print(f'km_all: {km_all}')
    km_reduced = round((persons_rowing/persons_all) * km_all)
    return km_reduced

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
    def __str__(self):
        return f'{{ km: {self.km}\tdescription: {self.descr}\tsection: {self.section_ind}\tpersons rowing: {self.persons_incl}}}'

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
                cday.section_ind = abs_index+1

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
        day_index = 0 if day_index == -1 else day_index

        print(f'day_index: {day_index}')

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

    def __str__(self):
        res = '\ndays:'
        for cday in self.person_days:
            res += f'\t{cday}\n'
        res += 'Sections: '
        for csection in self.sections:
            res += f'\t{csection}, '
        res += '\npersons: '
        for cpers in self.persons:
            res += f'{cpers}, '
        res += '\n'
        return res
    
    def calculate(self) -> dict[str, float]:
        def sort_days(acc: dict[int, list[Day]], cday: Day) -> dict[int, list[Day]]:
            if acc.get(cday.section_ind) is None:
                acc[cday.section_ind] = []

            acc[cday.section_ind].append(cday)
            return acc

        section_days: dict[int, list[Day]] = ft.reduce(sort_days, self.person_days, {})
        res: dict[str, list[Day]] = {}
        for cind in section_days:
            days: list[Day] = section_days[cind]
            if len(days) > 0:
                persons = days[0].persons_incl
                sect_res_reduced: float = calc_km_reduced(list(map(lambda c: c.km, days)), )



        return res

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


