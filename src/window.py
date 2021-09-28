import tkinter as tk
from .rowing_data import RowingData
from .locale import l

WIDGET_HEADER_PROPS: dict = {
    'relief': 'solid',
}
WIDGET_BODY_PROPS: dict = {
    'relief': 'solid',
}
WIDGET_PROPS: dict = {
    'borderwidth': 1,
}

WIDGET_PAD: dict = {
    'padx': 4,
    'pady': 2,
}

#from kivy.properties import 

class TopSection(tk.Frame):
    def __init__(self, master, rowingData: RowingData, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowingData = rowingData

        new_person = tk.Button(self, text=l('new_person'), command=self.new_person_pressed)
        new_person.pack(side=tk.LEFT, anchor=tk.NW, **WIDGET_PAD)

        new_section = tk.Button(self, text=l('new_section'), command=self.new_section_pressed)
        new_section.pack(side=tk.LEFT, anchor=tk.NW, **WIDGET_PAD)

        sections = SectionsSection(self, rowingData)
        sections.pack(side=tk.RIGHT, anchor=tk.NW, **WIDGET_PAD)

    def new_person_pressed(self):
        print('new person pressed')
    def new_section_pressed(self):
        print('new section pressed')


class MatrixSection(tk.Frame):
    PADDING: int = 5
    rowing_data: RowingData
    def __init__(self, master, rowing_data: RowingData, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowing_data = rowing_data

        test_label = tk.Label(self, text=l('test')+' 2')
        test_label.grid(row=0, column=0, sticky=tk.NSEW)
        #for (i, cperson) in enumerate(self.persons):
        #    clabel = tk.Label(self, text=cperson)
        #    clabel.grid(row=0, column=2+i)


class EditWidget(tk.Frame):
    def __init__(self, master, rowing_data: RowingData, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowing_data = rowing_data
        l = tk.Label(self, text='EditWidget')
        l.grid(row=0, column=0)


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

        self.update_rows()

    def update_rows(self):
        for (id_label, sect_nrow_label, edit_wgt) in self.sect_rows:
            id_label.destroy()
            del id_label
            sect_nrow_label.destroy()
            del sect_nrow_label
            edit_wgt.destroy()
            del edit_wgt


        for (i, c) in enumerate(self.rowing_data.sections):
            sect_id_label = tk.Label(self, text=f'{i}', **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            sect_id_label.grid(row=i+1, column=0, sticky=tk.NSEW)
            sect_nrow_label = tk.Label(self, text=f'{c}', **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            sect_nrow_label.grid(row=i+1, column=1, sticky=tk.NSEW)
            edit_wgt = EditWidget(self, self.rowing_data, **WIDGET_PROPS, **WIDGET_BODY_PROPS)
            edit_wgt.grid(row=i+1, column=2, sticky=tk.E)

            self.sect_rows.append((sect_id_label, sect_nrow_label, edit_wgt))
    

class BottomSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        calculate = tk.Button(self, text=l('calc_km'), command=self.calculate_pressed)

        calculate.pack(side=tk.RIGHT, padx=self.PADDING, pady=self.PADDING)

    def calculate_pressed(self):
        print('calculate pressed')


class WindowApp(tk.Tk):
    rowingData: RowingData = RowingData()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(l('title'))

        self.top_sect = TopSection(self, self.rowingData)
        self.win_frame = MatrixSection(self, self.rowingData)
        self.bottom_section = BottomSection(self)

        self.top_sect.pack(side=tk.TOP, fill=tk.BOTH)
        self.win_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_section.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == '__main__':
    app = WindowApp()
    app.mainloop()
