from Tkinter import *
from EntryFrame import EntryFrame

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        
        self.scoring = LabelFrame(self, text='Scoring')
        self.scoring.grid(column=0, row=0, sticky=EW)
        self.kernel = LabelFrame(self, text='Kernels')
        self.kernel.grid(column=1, row=0, sticky=EW)
        self.c = LabelFrame(self, text='C')
        self.c.grid(column=2, row=0, sticky=EW)
        self.cFrame = EntryFrame(self.c, 3)
        self.cFrame.grid(column=0, row=0)


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = svmWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

