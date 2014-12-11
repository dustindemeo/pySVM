from Tkinter import *

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        
        Label(self, text='Kernel').grid(column=0, row=0, sticky=W)
        Checkbutton(self, text='rbf').grid(column=0, row=1, sticky=W)
        Checkbutton(self, text='linear').grid(column=0, row=2, sticky=W)
        Checkbutton(self, text='poly').grid(column=0, row=3, sticky=W)
        Checkbutton(self, text='sigmoid').grid(column=0, row=4, sticky=W)
        Checkbutton(self, text='precomputed').grid(column=0, row=5, sticky=W)
        Label(self, text='C', anchor=E).grid(column=1, row=0, sticky=E)
        Entry(self, justify=RIGHT).grid(column=1, row=1, sticky=E)
        Entry(self, justify=RIGHT).grid(column=1, row=2, sticky=E)
        Entry(self, justify=RIGHT).grid(column=1, row=3, sticky=E)
        Entry(self, justify=RIGHT).grid(column=1, row=4, sticky=E)
        Entry(self, justify=RIGHT).grid(column=1, row=5, sticky=E)
        Button(self, text='Process').grid(column=0, row=6, sticky=EW)


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = svmWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

