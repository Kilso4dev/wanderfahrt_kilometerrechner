import tkinter as tk
from .rowing_data import RowingData
from .locale import l

#from kivy.properties import 

class TopSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_person = tk.Button(self, text=l('new_person'), command=self.new_person_pressed)
        new_section = tk.Button(self, text=l('new_section'), command=self.new_section_pressed)

        new_person.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)
        new_section.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)


    def new_person_pressed(self):
        print('new person pressed')
    def new_section_pressed(self):
        print('new section pressed')

class MatrixSection(tk.Frame):
    PADDING: int = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #for (i, cperson) in enumerate(self.persons):
        #    clabel = tk.Label(self, text=cperson)
        #    clabel.grid(row=0, column=2+i)

class SectionsSection(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class BottomSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        calculate = tk.Button(self, text=l('calc_km'), command=self.calculate_pressed)

        calculate.pack(side=tk.RIGHT, padx=self.PADDING, pady=self.PADDING)

    def calculate_pressed(self):
        print('calculate pressed')

class WindowApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(l('title'))

        self.top_sect = TopSection(self)
        self.win_frame = MatrixSection(self)
        self.bottom_section = BottomSection(self)

        self.top_sect.pack(side=tk.TOP, fill=tk.BOTH)
        self.win_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bottom_section.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == '__main__':
    app = WindowApp()
    app.mainloop() 
