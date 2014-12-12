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
        self.default = default
        self.lastRow = 0
        self.entryVariables = []
        self.entryWidgets = []
        self.addButton = Button(self, text='Add', command=self.addEntry)
        self.addButton.grid(column=0, row=self.lastRow)
        self.removeButton = Button(self, text='Remove', command=self.removeEntry)
        self.removeButton.grid(column=1, row=self.lastRow)
        self.lastRow += 1
        self.entryVariables.append(StringVar())
        self.entryVariables[-1].set(default)
        self.entryWidgets.append(Entry(self, justify=RIGHT, textvariable=self.entryVariables[-1], validate='key', validatecommand=(validateNumber, '%P')))
        self.entryWidgets[-1].grid(column=0, columnspan=2, row=self.lastRow)
        self.lastRow += 1

    def addEntry(self):
        validateNumber = self.register(isValid)
        self.entryVariables.append(StringVar())
        self.entryVariables[-1].set(self.default)
        self.entryWidgets.append(Entry(self, justify=RIGHT, textvariable=self.entryVariables[-1], validate='key', validatecommand=(validateNumber, '%P')))
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
