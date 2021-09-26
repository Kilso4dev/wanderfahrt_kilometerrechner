import tkinter as tk


#from kivy.properties import 

class KmCalc(tk.Frame):
    PADDING: int = 5

    persons: list[str] = ['P1', 'P2', 'P3', 'P4']
    sections: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (i, cperson) in enumerate(self.persons):
            clabel = tk.Label(self, text=cperson)
            clabel.grid(row=0, column=2+i)


class TopSection(tk.Frame):
    PADDING: int = 2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_person = tk.Button(self, text='New person', command=self.new_person_pressed)
        new_section = tk.Button(self, text='New section', command=self.new_section_pressed)

        new_person.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)
        new_section.pack(side=tk.LEFT, padx=self.PADDING, pady=self.PADDING)


    def new_person_pressed(self):
        print('new person pressed')
    def new_section_pressed(self):
        print('new section pressed')


def create_window():
    app = tk.Tk()
    app.title('KmCalc')
    top_sect = TopSection(app)
    win_frame = KmCalc(app)

    top_sect.pack(fill=tk.X, expand=False)
    win_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
    return app

if __name__ == '__main__':
    app = create_window()
    app.mainloop() 
