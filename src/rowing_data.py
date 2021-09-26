class Day:
    km: float = 0
    descr: str = ''
    section_ind: int = -1
    players_rowing: dict[str, bool] = {}

    def __init__(self, person_init_state: dict[str, bool], km: float, section_ind: int, descr: str = None):
        self.km = km
        self.section_ind = section_ind
        if descr is None:
            self.descr = f'Day: {round(km)}km'
        else:
            self.descr = descr

        self.players_rowing = person_init_state.copy()

    def set_person_rowing(self, name: str, rowing: bool):
        self.players_rowing[name] = rowing

    def remove_person(self, name: str):
        try:
            del self.players_rowing[name]
        except KeyError:
            pass


class RowingData:
    person_days: list[Day]
    sections: list[int] = [] # index: identifier, int: persons not rowing
    persons: list[str] = []

    # ----------------------------------- Persons ----------------------------------- 
    def add_person(self, name: str):
        self.persons.append(name)
        for cday in self.person_days:
            cday.set_person_rowing(name, False)

    def set_person(self, name: str, day_ind: int, rowing: bool):
        self.person_days[day_ind].set_person_rowing(name, rowing)

    def set_person_rowing(self, name: str, day_ind: int, rowing: bool):
        self.person_days[day_ind].players_rowing[name] = rowing

    def delete_person(self, name: str):
        for cday in self.person_days:
            cday.remove_person(name)

    # ----------------------------------- Sections ----------------------------------- 
    def insert_section(self, insert_at: int, persons_not_rowing: int) -> int:
        self.sections.insert(insert_at, persons_not_rowing)
        return insert_at

    def append_section(self, persons_not_rowing: int) -> int:
        self.insert_section(-1, persons_not_rowing)
        return len(self.sections)-1
    
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

    def delete_day(self, day_index: int) -> Day:
        to_del = self.person_days[day_index]
        del self.person_days[day_index]
        return to_del

    def get_all_sections(self) -> list[int]:
        return self.sections


