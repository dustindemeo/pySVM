from Tkinter import *
import tkFileDialog 
import numpy as np
import itertools
from sklearn.svm import SVC

def isNumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

class Variable():

    def __init__(self, index, column):
        self.index = index
        self.name = column[0]
        self.values = column[1:,]
        self.defaultType = self.getDefaultType(self.values)
        self.selectedType = StringVar()                         #this should be the radiobutton value
        self.selectedType.set(self.defaultType)
        #self.catDict = makeCatDict(self.values)
        #self.numEmpty = countEmpty(self.values)

    def makeCatDict(self, values):
        catDict = {}
        i = 0
        for v in values:
            if v not in catDict:
                catDict[v] = i
                i += 1
        return catDict

    def getDefaultType(self, values):
        for v in values:
            if v == '':
                pass
            elif not isNumber(v):
                return 'Categorical IV'
        return 'Scalar IV'

    def countEmpty(self, values):
        numEmpty = 0
        for v in values:
            if v == '':
                numEmpty += 1
        return numEmpty

class Variables():

    def __init__(self, csv):
        self.indexDV = None
        self.variables = []
        for i, col in enumerate(csv.T):
            self.variables.append(Variable(i, col))

    def setSelectedType(self, index, newType):
        if newType == self.variables[i].selectedType:
            return None
        elif newType == 'Binary DV':
            if not self.indexDV == None:
                self.variables[indexDV].selectedType.set(self.variables[indexDV].defaultType)
            self.variables[index].selectedType.set(newType)
        elif self.newType == 'Scalar IV':
            if not self.variables[index].defaultType == 'Scalar IV':
                return None
            else:
                self.variables[index].selectedType.set(newType)
        else:
            self.selectedType = newType

class Gui(Frame):
  
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.initUI()
        
    def initUI(self):
      
        self.rowMask = []
        self.colMask = []
        self.colDV = None

        self.master.title("pySVM")
        
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
	self.topLeftFrame = LabelFrame(self.master, text='1. Manage Variables')
        self.topLeftFrame.grid(row=0, column=0, sticky=NSEW)
        self.varCanvas = Canvas(self.topLeftFrame)
        self.varFrame = Frame(self.varCanvas)
        self.varScroll = Scrollbar(self.master, orient="vertical", command = self.varCanvas.yview)        
        self.varScroll.grid(row=0, column=1, sticky=NSEW)
        self.varCanvas['yscrollcommand'] = self.varScroll.set
        self.varCanvas.create_window((0,0), window=self.varFrame, anchor=NW)
        self.varFrame.bind("<Configure>", self.AuxscrollFunction)
        self.varCanvas.pack(fill=BOTH, expand=1, side=LEFT)

        Label(self.varFrame, text="Column Header").grid(row=0, column=0, sticky=W)
        Label(self.varFrame, text="  Scalar\n    IV").grid(row=0, column=1, sticky=W)
        Label(self.varFrame, text="Categorical\n    IV").grid(row=0, column=2, sticky=W)
        Label(self.varFrame, text="  Binary\n    DV").grid(row=0, column=3, sticky=W)
        Label(self.varFrame, text="\n     Skip").grid(row=0, column=4, sticky=W)

	self.topRightFrame = LabelFrame(self.master, text='2. Manage Dependent Variable')
        self.topRightFrame.grid(row=0, column=2, sticky=NSEW)
        self.dvFrame = Frame(self.topRightFrame, background='green')
        self.dvFrame.pack(fill=BOTH, expand=1, side=LEFT)
        Label(self.dvFrame, text='dv').pack()

        self.bottomFrame = LabelFrame(self.master, text='3. Manage SVM')
        self.bottomFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        self.svmFrame = Frame(self.bottomFrame, background='red')
        self.svmFrame.pack(fill=BOTH, expand=1, side=LEFT)
        Label(self.svmFrame, text='svm').pack()

    def AuxscrollFunction(self, event):
        self.varCanvas.configure(scrollregion=self.varCanvas.bbox("all"))

    def onOpen(self):

        ftypes = [('CSV files', '*.csv'), ('All files', '*')]
        dlalog = tkFileDialog.Open(self, filetypes=ftypes)
        filename = dlalog.show()
 
        if filename != '':

            self.csv = openCSV(filename)
            self.variables = Variables(self.csv)

            for v in self.variables.variables:
                label = Label(self.varFrame, text=v.name, fg="blue")
                label.grid(row=v.index+1, column=0, sticky=W)
                label.bind("<Button-1>", lambda event, v = v: self.clickHeader(v))
                Radiobutton(self.varFrame, variable=v.selectedType, value='Scalar IV', command=lambda v = v: self.selectVarType(v)).grid(row=v.index+1, column=1, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Categorical IV', command=lambda v = v: self.selectVarType(v)).grid(row=v.index+1, column=2, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Binary DV', command=lambda v = v: self.selectVarType(v)).grid(row=v.index+1, column=3, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Skip', command=lambda v = v: self.selectVarType(v)).grid(row=v.index+1, column=4, sticky=W)

    def clickHeader(self, variable):
       
       top = Toplevel()
       top.title(variable.name)

       values = '\n'.join(variable.values)
       msg = Message(top, text=values)
       msg.pack()

       button = Button(top, text="Dismiss", command=top.destroy)
       button.pack()
       return None

    def selectVarType(self, variable):
        print "{} to {}".format(variable.name, variable.selectedType.get())

    def onExit(self):

        self.quit()

def openCSV(filename):

    return np.loadtxt(open(filename, "rb"), dtype='string', delimiter=",", skiprows=0)

def headers(csv):

    return csv[0]

def main():

    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    gui = Gui(root)
    root.geometry("800x640+10+10")
    root.mainloop()  

if __name__ == '__main__':
    main()  
