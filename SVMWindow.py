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
        self.gamma = LabelFrame(self, text='gamma')
        self.gamma.grid(column=3, row=0, sticky=EW)
        self.gammaFrame = EntryFrame(self.gamma, 1)
        self.gammaFrame.grid(column=0, row=0)
        self.coef = LabelFrame(self, text='coef')
        self.coef.grid(column=4, row=0, sticky=EW)
        self.coefFrame = EntryFrame(self.coef, 1)
        self.coefFrame.grid(column=0, row=0)
        self.degree = LabelFrame(self, text='degree')
        self.degree.grid(column=5, row=0, sticky=EW)
        self.degreeFrame = EntryFrame(self.degree, 1)
        self.degreeFrame.grid(column=0, row=0)


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = SVMWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

