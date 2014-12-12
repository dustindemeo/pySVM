from Tkinter import *
from EntryFrame import EntryFrame

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        
        self.rbf = EntryFrame(self, 3)
        self.rbf.grid(column=0, row=0)


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = svmWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

