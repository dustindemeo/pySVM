from Tkinter import *

def isNumber(n):
    '''DESCRIPTION: This function determines if a string / value / object can be cast to a number. In other words, the function determines if something is a number.
       PRECONDITIONS: None. Any value can be given to isNumber
       POSTCONDITIONS: True/False will be returned to the calling function.
       SIDE EFFECTS: None.
       RETURN: True if n is a number. False if n is not a number.
       '''
    try:
        float(n)
        return True
    except ValueError:
        return False

class SVMRow(Frame):




    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        validateNumber = self.register(isNumber)
        
        self.kernelVariable = StringVar()
        self.kernelVariable.set('rbf')
        self.kernelVariable.trace('w', lambda name, index, mode, self=self: self.hideShow())
        self.cVariable = StringVar()      #all
        self.cVariable.set('1.0')
        self.gammaVariable = StringVar()  #rbf, poly, sigmoid
        self.gammaVariable.set('0')
        self.coefVariable = StringVar()   #poly, sigmoid
        self.coefVariable.set('0')
        self.degreeVariable = StringVar() #poly
        self.degreeVariable.set('3')

        Label(self, text='Kernel').grid(column=0, row=0, sticky=W)
        self.kernelWidget = OptionMenu(self, self.kernelVariable, "rbf", "linear", "poly", "sigmoid")
        self.kernelWidget.grid(column=0, row=1, sticky=W)
        Label(self, text='C', anchor=E).grid(column=1, row=0, sticky=E)
        self.cWidget = Entry(self, justify=RIGHT, textvariable=self.cVariable, validate='key', validatecommand=(validateNumber, '%P'))
        self.cWidget.grid(column=1, row=1, sticky=E)
        Label(self, text='gamma', anchor=E).grid(column=2, row=0, sticky=E)
        self.gammaWidget = Entry(self, justify=RIGHT, textvariable=self.gammaVariable, validate='key', validatecommand=(validateNumber, '%P'))
        self.gammaWidget.grid(column=2, row=1, sticky=E)
        Label(self, text='coef', anchor=E).grid(column=3, row=0, sticky=E)
        self.coefWidget = Entry(self, justify=RIGHT, textvariable=self.coefVariable, validate='key', validatecommand=(validateNumber, '%P'))
        self.coefWidget.grid(column=3, row=1, sticky=E)
        self.coefWidget.grid_forget()
        Label(self, text='degree', anchor=E).grid(column=4, row=0, sticky=E)
        self.degreeWidget = Entry(self, justify=RIGHT, textvariable=self.degreeVariable, validate='key', validatecommand=(validateNumber, '%P'))
        self.degreeWidget.grid(column=4, row=1, sticky=E)
        self.degreeWidget.grid_forget()

    def hideShow(self):
        if self.kernelVariable.get() == 'rbf':
            self.gammaWidget.grid(column=2, row=1)
            self.coefWidget.grid_forget()
            self.degreeWidget.grid_forget()
        if self.kernelVariable.get() == 'linear':
            self.gammaWidget.grid_forget()
            self.coefWidget.grid_forget()
            self.degreeWidget.grid_forget()
        if self.kernelVariable.get() == 'poly':
            self.gammaWidget.grid(column=2, row=1)
            self.coefWidget.grid(column=3, row=1)
            self.degreeWidget.grid(column=4, row=1)
        if self.kernelVariable.get() == 'sigmoid':
            self.gammaWidget.grid(column=2, row=1)
            self.coefWidget.grid(column=3, row=1)
            self.degreeWidget.grid_forget()


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = svmWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

