import tkinter as tk
from typing import Callable, Union
from functools import partial
from .rowing_data import RowingData
from .locale import l
from .scrollframe import ScrollableFrame

WIDGET_HEADER_PROPS: dict = {
    'relief': 'solid',
}
WIDGET_BODY_PROPS: dict = {
    'relief': 'solid',
}
WIDGET_PROPS: dict = {
    'borderwidth': .5,
}

WIDGET_PAD: dict = {
    'padx': 4,
    'pady': 2,
}

#from kivy.properties import 
class EditWidget(tk.Frame):
    rowing_data: RowingData

    edit_btn: tk.Button
    edit_img: tk.PhotoImage
    edit_fn: Union[Callable[[RowingData, int], int], None]

    del_btn: tk.Button
    del_img: tk.PhotoImage
    del_fn: Union[Callable[[RowingData, int], int], None]


    def __init__(self, master, \
                 rowing_data: RowingData, \
                 ind: int, \
                 *args, \
                 edit_fn: Callable[[RowingData, int], int] = None, \
                 del_fn: Callable[[RowingData, int], int] = None, \
                 **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowing_data = rowing_data
        self.index = ind

        self.edit_img = tk.PhotoImage(file='assets/2x/outline_edit_black_24dp.png').subsample(3, 3)
        self.edit_btn = tk.Button(self, image=self.edit_img, command=self.edit_sect_pressed, **WIDGET_PAD)
        self.edit_fn = edit_fn

        self.del_img = tk.PhotoImage(file='assets/2x/outline_remove_black_24dp.png').subsample(3, 3)
        self.del_btn = tk.Button(self, image=self.del_img, command=self.del_sect_pressed, **WIDGET_PAD)
        self.del_fn = del_fn

        self.edit_btn.grid(row=0, column=0)
        self.del_btn.grid(row=0, column=1)

    def edit_sect_pressed(self):
        if self.edit_fn is not None:
            self.edit_fn(self.rowing_data, self.index)
        print(f'{self.index}: edit_img pressed')

    def del_sect_pressed(self):
        if self.del_fn is not None:
            self.del_fn(self.rowing_data, self.index)
        print(f'{self.index}: delete section up pressed')

class SectionsSection(tk.Frame):
    rowing_data: RowingData
    sect_headers: tuple[tk.Label, tk.Label]
    sect_rows: list[tuple[tk.Label, tk.Label, EditWidget]] = []

    def __init__(self, master, rowing_data: RowingData, *args, **kwargs):
        super().__init__(master, *args, **WIDGET_PROPS, **WIDGET_BODY_PROPS, **kwargs)
        self.rowing_data: RowingData = rowing_data

        header_sect_name = tk.Label(self, text=l('sect_id'), **WIDGET_PROPS, **WIDGET_HEADER_PROPS, **WIDGET_PAD)
        header_sect_name.grid(row=0, column=0, sticky=tk.NSEW)

        sect_nrow = tk.Label(self, text=l('sect_nrow'), **WIDGET_PROPS, **WIDGET_HEADER_PROPS, **WIDGET_PAD)
        sect_nrow.grid(row=0, column=1, sticky=tk.NSEW)

        empty_frame = tk.Frame(self, **WIDGET_PROPS, **WIDGET_BODY_PROPS)
        empty_frame.grid(row=0, column=2, sticky=tk.NSEW)
        
        self.sect_headers = (header_sect_name, sect_nrow)

        self.update_data()

    def update_data(self):
        for (id_label, sect_nrow_label, edit_wgt) in self.sect_rows:
            id_label.destroy()
            sect_nrow_label.destroy()
            edit_wgt.destroy()
            self.sect_rows = []

        for (i, c) in enumerate(self.rowing_data.sections):
            sect_id_label = tk.Label(self, text=f'{i}', **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            sect_id_label.grid(row=i+1, column=0, sticky=tk.NSEW)
            sect_nrow_label = tk.Label(self, text=f'{c}', **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            sect_nrow_label.grid(row=i+1, column=1, sticky=tk.NSEW)
            edit_wgt = EditWidget(self, self.rowing_data, i, **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            edit_wgt.grid(row=i+1, column=2, sticky=tk.E)

            self.sect_rows.append((sect_id_label, sect_nrow_label, edit_wgt))

class TopSection(tk.Frame):
    rowing_data: RowingData
    person_btn: tk.Button
    section_btn: tk.Button
    sections: SectionsSection

    def __init__(self, master, rowingData: RowingData, *args, new_sect_fn: Callable[[], None], new_person_fn: Callable[[], None], **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowing_data = rowingData

        self.person_btn = tk.Button(self, text=l('new_person'), command=new_person_fn)
        self.person_btn.pack(side=tk.LEFT, anchor=tk.NW, **WIDGET_PAD)

        self.section_btn = tk.Button(self, text=l('new_section'), command=new_sect_fn)
        self.section_btn.pack(side=tk.LEFT, anchor=tk.NW, **WIDGET_PAD)

        self.sections = SectionsSection(self, rowingData)
        self.sections.pack(side=tk.RIGHT, anchor=tk.NW, **WIDGET_PAD)

    def update_data(self):
        self.sections.update_data()

class MatrixSection(tk.Frame):
    PADDING: int = 5
    rowing_data: RowingData

    days: list[tuple[tk.Label, tk.Label, tk.Label, EditWidget]] = []

    player_names_header: list[tk.Label] = []
    checkbox_rows: list[list[tuple[tk.BooleanVar, tk.Checkbutton]]] = []

    def __init__(self, master, rowing_data: RowingData, *args, **kwargs):
        super().__init__(master, *args, **WIDGET_PROPS, **WIDGET_BODY_PROPS, **kwargs) # , background='#222222'
        self.rowing_data = rowing_data

        tk.Label(self, text=l('day'), **WIDGET_PAD).grid(row=0, column=0)
        tk.Label(self, text=l('km_of_day'), **WIDGET_PAD).grid(row=0, column=1)
        tk.Label(self, text=l('section_id'), **WIDGET_PAD).grid(row=0, column=2)


        #test_label = tk.Label(self, text=l('test')+' 2')
        #test_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.update_data()

    def update_data(self):
        # Delete day rows
        for (day_name, day_km, sect_ind, edit_widget) in self.days:
            day_name.destroy()
            day_km.destroy()
            sect_ind.destroy()
            edit_widget.destroy()
        self.days = []

        # Delete header
        for c_header in self.player_names_header:
            c_header.destroy()
        self.player_names_header = []

        # Delete checkboxes
        for crow in self.checkbox_rows:
            for citems in crow:
                (_, cchkbx) = citems
                cchkbx.destroy()
        self.checkbox_rows = []


        inv_map_names: dict[str, int] = {}
        # Generate header
        for (i, c_name) in enumerate(self.rowing_data.persons):
            inv_map_names[c_name] = i # populate inverted map
            self.player_names_header.append(tk.Label(self, text=c_name))

        # Generate days, km and checkboxes
        for (i, cday) in enumerate(self.rowing_data.person_days):
            day_label = tk.Label(self, text=f'{l("day")} {i+1}')
            km_label = tk.Label(self, text=f'{cday.km}km')
            sect_ind = tk.Label(self, text=f'{"None" if cday.section_ind == -1 else cday.section_ind}')
            edit_wgt = EditWidget(self, self.rowing_data, i, \
#                                  edit_fn= lambda rd, i: print(f'[{i}] editing on {rd}'), \
#                                  del_fn=lambda rd, i: print(f'[{i}] deleting on {rd}'), \
                                  **WIDGET_BODY_PROPS, **WIDGET_PROPS, **WIDGET_PAD)
            self.days.append((day_label, km_label, sect_ind, edit_wgt))

            new_checkbox_row: list[tuple[tk.BooleanVar, tk.Checkbutton]] = []
            for (cpers, cval) in cday.persons_incl.items():
                cb = tk.BooleanVar()
                cb.set(cval)
                def get_val_from_ind(indices: tuple[int, int]) -> bool:
                    (day_i, pers_i) = indices
                    (l, _) = self.checkbox_rows[day_i][pers_i]
                    return l.get()

                def cmd_handler(rd: RowingData, indices: tuple[int, int]) -> None:
                    (day_i, pers_i) = indices
                    rd.set_person_rowing(rd.persons[pers_i], day_i, get_val_from_ind(indices))
                    #print(f'c_checkbutton {indices}: {get_val_from_ind(indices)}')
                    #print(f'Datamodel: {rd.persons[pers_i]}, Day {day_i} -> {rd.person_days[day_i].persons_incl[rd.persons[pers_i]]}')

                fn_partial_app = partial(cmd_handler, self.rowing_data)
                fn_partial_app = partial(fn_partial_app, (i, inv_map_names[cpers]))
                new_checkbox = tk.Checkbutton(self, \
                                               variable=cb, command=fn_partial_app)

                new_checkbox_row.append((cb, new_checkbox))
            self.checkbox_rows.append(new_checkbox_row)


        for (i, (day_label, km_label, sect_ind, edit_wgt)) in enumerate(self.days):
            day_label.grid(row=i+1, column=0, sticky=tk.NSEW)
            km_label.grid(row=i+1, column=1, sticky=tk.NSEW)
            sect_ind.grid(row=i+1, column=2, sticky=tk.NSEW)
            edit_wgt.grid(row=i+1, column=len(self.rowing_data.persons)+3, sticky=tk.NSEW)

        for (i, c_name_label) in enumerate(self.player_names_header):
            c_name_label.grid(row=0, column=3+i, sticky=tk.NSEW)

        for (cdayi, cd_check_row) in enumerate(self.checkbox_rows):
            for (c_pers_i, (_, c_checkbox)) in enumerate(cd_check_row):
                c_checkbox.grid(row=cdayi+1, column=c_pers_i+3)

        # Configure resizing
        checkbox_rows = len(self.checkbox_rows)
        #for i in range(checkbox_rows+3):
        #    self.rowconfigure(i, weight=1)
        if checkbox_rows > 0:
            checkbox_columns = len(self.checkbox_rows[0])
            for i in range(2, checkbox_columns+2):
                self.columnconfigure(i, weight=1)



class BottomSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        calculate = tk.Button(self, text=l('calc_km'), command=self.calculate_pressed)

        calculate.pack(side=tk.RIGHT, padx=self.PADDING, pady=self.PADDING)

    def calculate_pressed(self):
        print('calculate pressed')


class WindowApp(tk.Tk):
    rowing_data: RowingData = RowingData()
    top_sect: TopSection
    win_frame: MatrixSection
    bottom_section: BottomSection
    W = 500
    H = 300

    def new_section_pressed(self):
        from .create_section_dialog import new_section
        sect: Union[int,None] = new_section(self)
        if sect is not None:
            print(f'New section: {sect}km')
            self.rowing_data.append_section(sect)
            self.top_sect.update_data()
            print(list(map(lambda c: c.__str__(), self.rowing_data.person_days)))
        else:
            print('No new section')
        print('new section pressed')

    def new_person_pressed(self):
        from .create_person_dialog import new_pers
        pers: str = new_pers(self)
        if pers is not None:
            print(f'New person: {pers}')
            self.rowing_data.add_person(pers)
            self.win_frame.update_data()
            print(list(map(lambda c: c.__str__(), self.rowing_data.person_days)))
        else:
            print('No new section')
        print('new section pressed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minsize(self.W, self.H)
        self.geometry(f'{self.W}x{self.H}')
        self.title(l('title'))
        scrollframe = ScrollableFrame(self)

        self.top_sect = TopSection(self, self.rowing_data, \
                                   new_sect_fn=self.new_section_pressed, \
                                   new_person_fn=self.new_person_pressed)
        self.win_frame = MatrixSection(scrollframe.scrollable_frame, self.rowing_data)
        self.bottom_section = BottomSection(self)

        self.top_sect.pack(side=tk.TOP, fill=tk.BOTH)
        self.win_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_section.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == '__main__':
    app = WindowApp()
    app.mainloop()
