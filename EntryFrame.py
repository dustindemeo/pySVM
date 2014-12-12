from Tkinter import *

def isValid(str):
    '''DESCRIPTION: This function determines if a string can be cast to a number or is empty
       PRECONDITIONS: None. Any value can be given to isNumber
       POSTCONDITIONS: True/False will be returned to the calling function.
       SIDE EFFECTS: None.
       RETURN: True if n is a number or empty. False if n is not a number.
       '''
    if str == '':
        return True
    try:
        float(str)
        return True
    except ValueError:
        return False

class EntryFrame(Frame):

    def __init__(self, master, default, **args):
        Frame.__init__(self, master, args)
        validateNumber = self.register(isValid)
        self.canvas = Canvas(self, height='4c', width='2c')
        self.frame = Frame(self.canvas, args)
        self.sb = Scrollbar(self, orient='vertical', command = self.canvas.yview)
        self.sb.grid(row=0, column=1, sticky=NSEW)
        self.canvas['yscrollcommand'] = self.sb.set
        self.canvas.create_window((0,0), window=self.frame, anchor=NW)
        self.frame.bind("<Configure>", self.auxScroll)
        self.canvas.grid(column=0, row=0)

        self.default = default
        self.lastRow = 0
        self.entryVariables = []
        self.entryWidgets = []
        self.addButton = Button(self.frame, text='+', command=self.addEntry)
        self.addButton.grid(column=0, row=self.lastRow)
        self.removeButton = Button(self.frame, text='-', command=self.removeEntry)
        self.removeButton.grid(column=1, row=self.lastRow)
        self.lastRow += 1
        self.entryVariables.append(StringVar())
        self.entryVariables[-1].set(default)
        self.entryWidgets.append(Entry(self.frame, justify=RIGHT, width=8, textvariable=self.entryVariables[-1], validate='key', validatecommand=(validateNumber, '%P')))
        self.entryWidgets[-1].grid(column=0, columnspan=2, row=self.lastRow)
        self.lastRow += 1

    def addEntry(self):
        validateNumber = self.register(isValid)
        self.entryVariables.append(StringVar())
        self.entryVariables[-1].set(self.default)
        self.entryWidgets.append(Entry(self.frame, justify=RIGHT, width=8, textvariable=self.entryVariables[-1], validate='key', validatecommand=(validateNumber, '%P')))
        self.entryWidgets[-1].grid(column=0, columnspan=2, row=self.lastRow)
        self.lastRow += 1

    def removeEntry(self):
        if len(self.entryVariables) > 1:
            del self.entryVariables[-1]
            self.entryWidgets[-1].grid_forget()
            del self.entryWidgets[-1]
            self.lastRow -= 1

    def getValues(self):
       values = []
       for v in self.entryVariables:
           values.append(v.get())
       values.sort()
       return values 

    def auxScroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
