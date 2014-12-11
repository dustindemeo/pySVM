from Tkinter import *
import tkFileDialog 
import numpy as np
import itertools
from sklearn.svm import SVC
from sklearn import preprocessing
from SplitWindow import SplitWindow
from SVMWindow import SVMWindow
import SVM
from Variable import Variable

class Gui(Frame):
  
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.initUI()
        
    def initUI(self):
      
        self.indexDV = None
        self.variables = []

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
        self.dvFrame = SplitWindow(self.topRightFrame, background='green')
        self.dvFrame.pack(fill=BOTH, expand=1, side=LEFT)

        self.bottomFrame = LabelFrame(self.master, text='3. Manage SVM')
        self.bottomFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        self.svmFrame = Frame(self.bottomFrame, background='red')
        self.svmFrame.pack(fill=BOTH, expand=1, side=LEFT)
        Label(self.svmFrame, text='Kernel').grid(column=0, row=0, sticky=W)
        Checkbutton(self.svmFrame, text='rbf').grid(column=0, row=1, sticky=W)
        Checkbutton(self.svmFrame, text='linear').grid(column=0, row=2, sticky=W)
        Checkbutton(self.svmFrame, text='poly').grid(column=0, row=3, sticky=W)
        Checkbutton(self.svmFrame, text='sigmoid').grid(column=0, row=4, sticky=W)
        Checkbutton(self.svmFrame, text='precomputed').grid(column=0, row=5, sticky=W)
        Label(self.svmFrame, text='C', anchor=E).grid(column=1, row=0, sticky=E)
        Entry(self.svmFrame, justify=RIGHT).grid(column=1, row=1, sticky=E)
        Entry(self.svmFrame, justify=RIGHT).grid(column=1, row=2, sticky=E)
        Entry(self.svmFrame, justify=RIGHT).grid(column=1, row=3, sticky=E)
        Entry(self.svmFrame, justify=RIGHT).grid(column=1, row=4, sticky=E)
        Entry(self.svmFrame, justify=RIGHT).grid(column=1, row=5, sticky=E)
        Button(self.svmFrame, text='Process', command=self.process).grid(column=0, row=6, sticky=EW)

    def getMaskRow(self):
        maskRow = set()
        for variable in self.variables:
            if not variable.selectedType.get() == 'Skip':
                for i, value in enumerate(variable.values):
                    if value == '':
                        maskRow.add(i)
        return list(maskRow)

    def process(self):
        maskRow = self.getMaskRow()
        # - 1 because of header row in csv
        # could also do numRow = len(self.variables[0].values)a- len(maskRow)
        numRow = len(self.csv) - len(maskRow) - 1
        numSIV = 0
        numCIV = 0
        for variable in self.variables:
            if variable.selectedType.get() == 'Scalar IV':
                numSIV += 1
            elif variable.selectedType.get() == 'Categorical IV':
                numCIV += 1
        SIV = np.empty(shape=(numRow,numSIV))
        i = 0
        for variable in self.variables:
            if variable.selectedType.get() == 'Scalar IV':
                SIV[:,i] = np.delete(np.asarray(variable.values).T, maskRow, axis=0)
                i += 1
        
        CIV = np.empty(shape=(numRow,numCIV))
        i = 0
        for variable in self.variables:
            if variable.selectedType.get() == 'Categorical IV':
                variable.catDict = variable.makeCatDict()
                temp = []
                for v in variable.values:
                    temp.append(variable.catDict[v])
                CIV[:,i] = np.delete(np.asarray(temp).T, maskRow, axis=0)
                i += 1

        self.stdScaler = preprocessing.StandardScaler().fit(SIV)
        sSIV = self.stdScaler.transform(SIV)

        self.encScaler = preprocessing.OneHotEncoder().fit(CIV)
        eCIV = self.encScaler.transform(CIV).toarray()

        #Use eSIV and eCIV if you want scaled and encoded data
        #X = np.concatenate((SIV, CIV), axis=1)
        X = np.concatenate((sSIV, eCIV), axis=1)

        self.variables[self.indexDV].catDict = self.dvFrame.makeCatDict()
        print self.variables[self.indexDV].catDict
        temp = []
        for v in self.variables[self.indexDV].values:
            temp.append(self.variables[self.indexDV].catDict[v])
        y = np.delete(np.asarray(temp).T, maskRow, axis=0)

        SVM.skSVM(X, y)

    def setSelectedType(self, variable):
        if variable.selectedType.get() == 'Binary DV' and not self.indexDV == variable.index:
            if not self.indexDV == None:
                self.variables[self.indexDV].selectedType.set(self.variables[self.indexDV].defaultType)
            self.indexDV = variable.index
            variable.catDict = variable.makeCatDict()
            self.dvFrame.clear()
            self.dvFrame.insertListRight(variable.catDict.keys())
        elif variable.selectedType.get() == 'Scalar IV':
            if not variable.defaultType == 'Scalar IV':
                variable.selectedType.set(variable.defaultType)

    def AuxscrollFunction(self, event):
        self.varCanvas.configure(scrollregion=self.varCanvas.bbox("all"))

    def onOpen(self):

        ftypes = [('CSV files', '*.csv'), ('All files', '*')]
        dlalog = tkFileDialog.Open(self, filetypes=ftypes)
        filename = dlalog.show()
 
        if filename != '':

            self.csv = openCSV(filename)
            for i, col in enumerate(self.csv.T):
                self.variables.append(Variable(i, col))

            for v in self.variables:
                label = Label(self.varFrame, text=v.name, fg="blue")
                label.grid(row=v.index+1, column=0, sticky=W)
                label.bind("<Button-1>", lambda event, v = v: self.clickHeader(v))
                Radiobutton(self.varFrame, variable=v.selectedType, value='Scalar IV', command=lambda v = v: self.clickRadio(v)).grid(row=v.index+1, column=1, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Categorical IV', command=lambda v = v: self.clickRadio(v)).grid(row=v.index+1, column=2, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Binary DV', command=lambda v = v: self.clickRadio(v)).grid(row=v.index+1, column=3, sticky=W)
                Radiobutton(self.varFrame, variable=v.selectedType, value='Skip', command=lambda v = v: self.clickRadio(v)).grid(row=v.index+1, column=4, sticky=W)

    def clickHeader(self, variable):
       
       top = Toplevel()
       top.title(variable.name)

       values = '\n'.join(variable.values)
       msg = Message(top, text=values)
       msg.pack()

       button = Button(top, text="Dismiss", command=top.destroy)
       button.pack()
       return None

    def clickRadio(self, variable):
        self.setSelectedType(variable)
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
    root.geometry("1000x650+10+10")
    root.mainloop()  

if __name__ == '__main__':
    main()  
