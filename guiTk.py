#NAME: Variable.py
#DATE CREATED: 12/10/2014
#AUTHORS: Abhinandan Halemane, Dustin DeMeo, Mahshid Aimaq, Vinitha Raja

'''
DESCRIPTION:
This module holds  functions necessary to design & load the required data to Tk gui.
It uses several functions like iniUI, Process , Onopen & several functions to load the data in the perfect format 

'''
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
        self.svmFrame = SVMWindow(self.bottomFrame)
        self.svmFrame.pack(fill=BOTH, expand=1, side=LEFT)
        Button(self.bottomFrame, text='Run', command=self.process).pack()
'''
Maskrow function is designed to mask the list of row that this function outputs.
That list are to be eliminated & not to be shown  in the interactive gui.
If the variable type is skip then then the value or row is pushed to a list.
With this function we get a list of row to be masked.
'''



    def getMaskRow(self):
        maskRow = set()
        for variable in self.variables:
            if not variable.selectedType.get() == 'Skip':
                for i, value in enumerate(variable.values):
                    if value == '':
                        maskRow.add(i)
        return list(maskRow)

'''
Description : Process function is designed to pull all the function , load the data & process in the gui.Initially all the scores, tuned parameter ,categorical variable parameters & data parameters from svm frame are assigned to respective values.
The mask row list generated from mask row function  is loaded to mask row value.
The imputer parameters are given to Scalar IV, Categorical IV & binary DV then these values are assigned to the respective imputer parameters.
'''

    def process(self):
        scoring = self.svmFrame.getScores()
        tuned_parameters = self.svmFrame.getTunedParameters()
        cv_parameters = self.svmFrame.getCVParameters()
        data_parameters = self.svmFrame.getDataParameters()

        maskRow = self.getMaskRow()
        imputerSIV = preprocessing.Imputer(missing_values='NaN', strategy=data_parameters['impute'], axis=0, copy=True)
        imputerCIV = preprocessing.Imputer(missing_values='NaN', strategy='most_frequent', axis=0, copy=True)
        imputerBDV = preprocessing.Imputer(missing_values='NaN', strategy='most_frequent', axis=1, copy=True)
            
        numRow = len(self.csv) - 1 #-1 because of header row in csv)
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
                SIV[:,i] = np.asarray(variable.values).T
                i += 1

        CIV = np.empty(shape=(numRow,numCIV))
        i = 0
        for variable in self.variables:
            if variable.selectedType.get() == 'Categorical IV':
                variable.catDict = variable.makeCatDict()
                temp = []
                for v in variable.values:
                    temp.append(variable.catDict.get(v, None))
                CIV[:,i] = np.asarray(temp).T
                i += 1

        self.variables[self.indexDV].catDict = self.dvFrame.makeCatDict()
        temp = []
        for v in self.variables[self.indexDV].values:
            temp.append(self.variables[self.indexDV].catDict[v])
        y = np.asarray(temp).T
        
        if data_parameters['cleanup'] == 'delete':
            SIV = np.delete(SIV, maskRow, axis=0)
            CIV = np.delete(CIV, maskRow, axis=0)
            y = np.delete(y, maskRow, axis=0)
        else:
            imputerSIV.fit(SIV)
            SIV = imputerSIV.transform(SIV)
            imputerCIV.fit(CIV)
            CIV = imputerCIV.transform(CIV)
            imputerBDV.fit(y)
            y = imputerBDV.transform(y)[0]

        if data_parameters['scale']:
            self.stdScaler = preprocessing.StandardScaler().fit(SIV)
            SIV = self.stdScaler.transform(SIV)

        if data_parameters['oneHot']:
            self.encScaler = preprocessing.OneHotEncoder().fit(CIV)
            CIV = self.encScaler.transform(CIV).toarray()

        X = np.concatenate((SIV, CIV), axis=1)

        SVM.skSVM(X, y, scoring, tuned_parameters, data_parameters, cv_parameters)

    def setSelectedType(self, variable):
        if variable.selectedType.get() == 'Binary DV' and not self.indexDV == variable.index:
            if not self.indexDV == None:
                self.variables[self.indexDV].selectedType.set(self.variables[self.indexDV].defaultType)
            self.indexDV = variable.index
            self.dvFrame.clear()
            self.dvFrame.insertListLeft(list(set(variable.values)))
        elif variable.selectedType.get() == 'Scalar IV':
            if not variable.defaultType == 'Scalar IV':
                variable.selectedType.set(variable.defaultType)

    def AuxscrollFunction(self, event):
        self.varCanvas.configure(scrollregion=self.varCanvas.bbox("all"))
'''
On open function is implemented to display contents in the gui.All the contents of csv file are loaded & customized to display here.
The headers are labelled & once the value is clicked , the list pops up in a separate dialog box.
The main configuration here is the implementation of radio buttons for all the categories mentioned where the user can categorize these variables.
'''
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
       Label(top, text=variable.name).pack()
       values = '\n'.join(variable.values)
       Message(top, text=values).pack()
       Button(top, text="Dismiss", command=top.destroy).pack()
       return None

    def clickRadio(self, variable):
        self.setSelectedType(variable)

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
    root.geometry("1000x700+10+10")
    root.mainloop()  

if __name__ == '__main__':
    main()  
