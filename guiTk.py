from Tkinter import *
import tkFileDialog 
import numpy as np
import itertools
from sklearn.svm import SVC

class Gui(Frame):
  
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.initUI()
        
    def initUI(self):
      
	self.varTypes = []
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
        Label(self.varFrame, text="S IV").grid(row=0, column=1, sticky=W)
        Label(self.varFrame, text="C IV").grid(row=0, column=2, sticky=W)
        Label(self.varFrame, text=" DV ").grid(row=0, column=3, sticky=W)
        Label(self.varFrame, text="Skip").grid(row=0, column=4, sticky=W)

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

            for i, header in enumerate(headers(self.csv)):
                label= Label(self.varFrame, text=header, fg="blue")
                label.grid(row=i+1, column=0, sticky=W)
                label.bind("<Button-1>", lambda event, i = i, header = header: self.clickHeader(i, header))
                self.varTypes.append(IntVar())
                Radiobutton(self.varFrame, variable=self.varTypes[-1], value=0, command=lambda i=i, j=0: self.changeVarType(i, j)).grid(row=i+1, column=1, sticky=W)
                Radiobutton(self.varFrame, variable=self.varTypes[-1], value=1, command=lambda i=i, j=1: self.changeVarType(i, j)).grid(row=i+1, column=2, sticky=W)
                Radiobutton(self.varFrame, variable=self.varTypes[-1], value=2, command=lambda i=i, j=2: self.changeVarType(i, j)).grid(row=i+1, column=3, sticky=W)
                Radiobutton(self.varFrame, variable=self.varTypes[-1], value=3, command=lambda i=i, j=3: self.changeVarType(i, j)).grid(row=i+1, column=4, sticky=W)

    def clickHeader(self, col, header):
       
       top = Toplevel()
       top.title(header)

       data = '\n'.join(self.csv[:,col])
       msg = Message(top, text=data)
       msg.pack()

       button = Button(top, text="Dismiss", command=top.destroy)
       button.pack()
       return None

    def changeVarType(self, i, newType):
        print "{} to {}".format(i, newType)

    def onExit(self):

        for v in self.varTypes:
          print v.get()
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
