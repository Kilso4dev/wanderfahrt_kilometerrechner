import tkinter as tk
from tkinter.messagebox import askretrycancel
import typing as tp
from .locale import l

PAD: dict = {
    'padx': 4,
    'pady': 2,
}

ret: tp.Union[int, None] = None

def new_section(master) -> tp.Union[int, None]:
    global ret
    ret = None

    km_input_str: tk.StringVar = tk.StringVar()

    win = tk.Toplevel(master, padx=30, pady=10) # make a new window
    subframe: tk.Frame = tk.Frame(win, **PAD)
    tk.Label(subframe, text=f"{l('pers_not_rowing')}:").pack(side=tk.LEFT)
    tk.Entry(subframe, textvariable=km_input_str, width=4).pack(side=tk.RIGHT)

    subframe.pack()

    def quit():
        global ret
        try:
            ret = int(km_input_str.get())
        except ValueError:
            retry = askretrycancel(master=win, title=l('sect_create_inv_title'), message=l('sect_create_inv_msg'))
            if retry:
                win.lift()
                return
        win.quit()

    ok_btn = tk.Button(win, text='OK', command=quit, **PAD)  # set quit callback
    ok_btn.bind('')
    ok_btn.pack()

    win.protocol('WM_DELETE_WINDOW', win.quit)  # quit on wm close too!

    win.title(l('new_sect'))
    win.resizable(False, False)
    win.focus_set() # take over input focus,
    win.grab_set() # disable other windows while I'm open,
    #win.lift()

    win.mainloop()  # and start a nested event loop to wait 
    win.destroy()
    return ret
