import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, vert=False, horiz=False, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg='#B044FF')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#30C049')
        scrollbar_vert = tk.Scrollbar(self, orient="horizontal", command=canvas.xview, bg='#90C3FF')
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox('all')
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar_vert.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_vert.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.TOP, fill="both", expand=True)
