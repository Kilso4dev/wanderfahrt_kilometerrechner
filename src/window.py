import tkinter as tk
from .rowing_data import RowingData
from .locale import l

#from kivy.properties import 

class TopSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, rowingData: RowingData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowingData = rowingData

        new_person = tk.Button(self, text=l('new_person'), command=self.new_person_pressed)
        new_section = tk.Button(self, text=l('new_section'), command=self.new_section_pressed)
        sections = SectionsSection(rowingData, self)

        new_person.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)
        new_section.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)
        sections.pack(side=tk.RIGHT, padx=self.PADDING, pady=self.PADDING)

    def new_person_pressed(self):
        print('new person pressed')
    def new_section_pressed(self):
        print('new section pressed')

class MatrixSection(tk.Frame):
    PADDING: int = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        test_label = tk.Label(self, text=l('test')+' 2')

        test_label.grid(row=0, column=0, sticky=tk.NSEW)
        #for (i, cperson) in enumerate(self.persons):
        #    clabel = tk.Label(self, text=cperson)
        #    clabel.grid(row=0, column=2+i)

class SectionsSection(tk.Frame):
    def __init__(self, rowing_data: RowingData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowing_data = rowing_data

        test_label = tk.Label(self, text=l('text')+' 1')

        test_label.grid(row=0, column=0, sticky=tk.NSEW)

    

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

        self.top_sect = TopSection(self.rowingData, self)
        self.win_frame = MatrixSection(self)
        self.bottom_section = BottomSection(self)

        self.top_sect.pack(side=tk.TOP, fill=tk.BOTH)
        self.win_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_section.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == '__main__':
    app = WindowApp()
    app.mainloop()
