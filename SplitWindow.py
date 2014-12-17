from Tkinter import *
import re

'''From http://stackoverflow.com/questions/5254021/python-human-sort-of-numbers-with-alpha-numeric-but-in-pyqt-and-a-lt-oper'''
def humanKey(key):
    parts = re.split('(\d*\.\d+|\d+)', key)
    return tuple((e.swapcase() if i % 2 == 0 else float(e))
        for i, e in enumerate(parts))

class SplitWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        self.leftLabel = Label (self, text='Fail', borderwidth=1, relief=RAISED)
        self.leftLabel.grid(row=0, column=0, sticky=EW)
        self.leftListbox = Listbox(self, width=20, borderwidth=0, selectborderwidth=0, relief=FLAT, exportselection=FALSE)
        self.leftListbox.grid(row=1, column=0)
        self.leftListbox.bind('<B1-Motion>', lambda event, self=self: self.selectLeft(event.y))
        self.leftListbox.bind('<Button-1>', lambda event, self=self: self.selectLeft(event.y))
        self.leftListbox.bind('<Double-Button-1>', lambda event, self=self: self.doubleLeft(event.y))
        self.leftListbox.bind('<Leave>', lambda event: 'break')
        self.leftListbox.bind('<B2-Motion>', lambda event, self=self: self.b2motionLeft(event.x, event.y))
        self.leftListbox.bind('<Button-2>', lambda evenet, self=self: self.button2Left(evenet.x, event.y))
        self.leftScrollbar = Scrollbar(self, orient=VERTICAL, command=self.scrollLeft)
        self.leftScrollbar.grid(row=0, column=1, rowspan=2, sticky=NS)
        self.leftListbox['yscrollcommand']=self.leftScrollbar.set

        self.rightLabel = Label (self, text='Pass', borderwidth=1, relief=RAISED)
        self.rightLabel.grid(row=0, column=3, sticky=EW)
        self.rightListbox = Listbox(self, width=20, borderwidth=0, selectborderwidth=0, relief=FLAT, exportselection=FALSE)
        self.rightListbox.grid(row=1, column=3)
        self.rightListbox.bind('<B1-Motion>', lambda event, self=self: self.selectRight(event.y))
        self.rightListbox.bind('<Button-1>', lambda event, self=self: self.selectRight(event.y))
        self.rightListbox.bind('<Double-Button-1>', lambda event, self=self: self.doubleRight(event.y))
        self.rightListbox.bind('<Leave>', lambda event: 'break')
        self.rightListbox.bind('<B2-Motion>', lambda event, self=self: self.b2motionRight(event.x, event.y))
        self.rightListbox.bind('<Button-2>', lambda event, self=self: self.button2Right(event.x, event.y))
        self.rightScrollbar = Scrollbar(self, orient=VERTICAL, command=self.scrollRight)
        self.rightScrollbar.grid(row=0, column=4, rowspan=2, sticky=NS)
        self.rightListbox['yscrollcommand']=self.rightScrollbar.set


    def selectLeft(self, y):
        row = self.leftListbox.nearest(y)
        self.leftListbox.selection_clear(0, END)
        self.rightListbox.selection_clear(0, END)
        self.leftListbox.selection_set(row, None)
        return 'break'

    def selectRight(self, y):
        row = self.rightListbox.nearest(y)
        self.leftListbox.selection_clear(0, END)
        self.rightListbox.selection_clear(0, END)
        self.rightListbox.selection_set(row, None)
        return 'break'

    def doubleLeft(self, y):
        row = self.leftListbox.nearest(y)
        value = self.leftListbox.get(row, last=None)
        if not value == '':
            self.rightListbox.insert(END, value)
            self.leftListbox.delete(row, None)
            self.leftListbox.selection_clear(0, END)
            self.rightListbox.selection_clear(0, END)
            self.sortRight()
        return 'break'

    def doubleRight(self, y):
        row = self.rightListbox.nearest(y)
        value = self.rightListbox.get(row, last=None)
        if not value == '':
            self.leftListbox.insert(END, value)
            self.rightListbox.delete(row, None)
            self.rightListbox.selection_clear(0, END)
            self.leftListbox.selection_clear(0, END)
            self.sortLeft()
        return 'break'

    def makeCatDict(self):
        catDict = {}
        for v in self.leftListbox.get(0, END):
            catDict[v] = 0
        for v in self.rightListbox.get(0, END):
            catDict[v] = 1
        return catDict

    def scrollLeft(self, *args):
        apply(self.leftListbox.yview, args)

    def scrollRight(self, *args):
        apply(self.rightListbox.yview, args)

    def insertListLeft(self, l):
        for value in l:
            self.leftListbox.insert(0, value)
        self.sortLeft()

    def insertListRight(self, l):
        for value in l:
            self.rightListbox.insert(0, value)
        self.sortRight()

    def insertLeft(self, value):
        self.leftListbox.insert(0, value)
        self.sortLeft()

    def insertRight(self, value):
        self.rightListbox.insert(0, value)
        self.sortRight()

    def sortLeft(self):
        temp = list(self.leftListbox.get(0, END))
        temp.sort(key=humanKey)
        self.leftListbox.delete(0, END)
        for i in temp:
            self.leftListbox.insert(END, i)

    def sortRight(self):
        temp = list(self.rightListbox.get(0, END))
        temp.sort(key=humanKey)
        self.rightListbox.delete(0, END)
        for i in temp:
            self.rightListbox.insert(END, i)

    def clear(self):
        self.leftListbox.delete(0, END)
        self.rightListbox.delete(0, END)

if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='Binary Dependent Variable').pack()
    sw = SplitWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    for i in range(15):
        sw.insertLeft('Left {}'.format(i))
        sw.insertRight('Right {}'.format(i))
    tk.mainloop()

