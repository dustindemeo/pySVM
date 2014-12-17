from Tkinter import *
from EntryFrame import EntryFrame

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
        int(str)
    except ValueError:
        return False

    if int(str) <= 80 and int(str) >0:
        return True
    else:
        return False

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        validateInt = self.register(isValid)
        
        self.scoring = LabelFrame(self, text='A. Optimize Estimator for:')
        self.scoring.grid(column=0, row=0, sticky=NSEW)
        self.scoringVariable = StringVar()
        self.accuracyRadiobutton = Radiobutton(self.scoring, text='Accuracy', variable=self.scoringVariable, value='accuracy', indicatoron=False, width=20)
        self.accuracyRadiobutton.grid(column=0, row=0, sticky=W)
        self.accuracyRadiobutton.select()
        self.precisionRadiobutton = Radiobutton(self.scoring, text='Precision', variable=self.scoringVariable, value='precision', indicatoron=False, width=20)
        self.precisionRadiobutton.grid(column=0, row=1, sticky=W)
        self.recallRadiobutton = Radiobutton(self.scoring, text='Recall', variable=self.scoringVariable, value='recall', indicatoron=False, width=20)
        self.recallRadiobutton.grid(column=0, row=2, sticky=W)
        self.f1Radiobutton = Radiobutton(self.scoring, text='F1', variable=self.scoringVariable, value='f1', indicatoron=False, width=20)
        self.f1Radiobutton.grid(column=0, row=3, sticky=W)
        self.avgPrecisionRadiobutton = Radiobutton(self.scoring, text='Avg. Precision', variable=self.scoringVariable, value='average_precision', indicatoron=False, width=20)
        self.avgPrecisionRadiobutton.grid(column=0, row=4, sticky=W)
        self.rocAUCRadiobutton = Radiobutton(self.scoring, text='ROC AUC', variable=self.scoringVariable, value='roc_auc', indicatoron=False, width=20)
        self.rocAUCRadiobutton.grid(column=0, row=5, sticky=W)

        self.gridding = LabelFrame(self, text='B. Gridding Parameters:')
        self.gridding.grid(column=1, row=0, sticky=NSEW)

        self.kernel = LabelFrame(self.gridding, text='i. Kernels')
        self.kernel.grid(column=1, row=0, sticky=NSEW)
        self.rbfVariable = IntVar()
        self.rbfCheckbutton = Checkbutton(self.kernel, text='rbf', variable=self.rbfVariable)
        self.rbfCheckbutton.grid(column=0, row=0, sticky=W)
        self.rbfCheckbutton.select()
        self.linearVariable = IntVar()
        self.linearCheckbutton = Checkbutton(self.kernel, text='linear', variable=self.linearVariable)
        self.linearCheckbutton.grid(column=0, row=1, sticky=W)
        self.sigmoidVariable = IntVar()
        self.sigmoidCheckbutton = Checkbutton(self.kernel, text='sigmoid', variable=self.sigmoidVariable)
        self.sigmoidCheckbutton.grid(column=0, row=2, sticky=W)
        self.polyVariable = IntVar()
        self.polyCheckbutton = Checkbutton(self.kernel, text='poly', variable=self.polyVariable)
        self.polyCheckbutton.grid(column=0, row=3, sticky=W)

        self.c = LabelFrame(self.gridding, text='ii. C Values')
        self.c.grid(column=2, row=0, sticky=NSEW)
        self.cFrame = EntryFrame(self.c, 3)
        self.cFrame.grid(column=0, row=0)

        self.gamma = LabelFrame(self.gridding, text='iii. Gammas')
        self.gamma.grid(column=3, row=0, sticky=NSEW)
        self.gammaFrame = EntryFrame(self.gamma, 1)
        self.gammaFrame.grid(column=0, row=0)

        self.coef = LabelFrame(self.gridding, text='iv. Coefficients')
        self.coef.grid(column=4, row=0, sticky=NSEW)
        self.coefFrame = EntryFrame(self.coef, 1)
        self.coefFrame.grid(column=0, row=0)

        self.degree = LabelFrame(self.gridding, text='v. Degrees')
        self.degree.grid(column=5, row=0, sticky=NSEW)
        self.degreeFrame = EntryFrame(self.degree, 1)
        self.degreeFrame.grid(column=0, row=0)

        self.crossValidation = LabelFrame(self.gridding, text='vi. Cross-validation:')
        self.crossValidation.grid(column=6, row=0, sticky=NSEW)
        self.crossValidationVariable = StringVar()
        self.stratifiedKFoldRadiobutton = Radiobutton(self.crossValidation, text='Stratified K-fold', variable=self.crossValidationVariable, value='skf', command=self.selectKFold)
        self.stratifiedKFoldRadiobutton.grid(column=0, columnspan=2, row=0, sticky=W)
        self.kFoldRadiobutton = Radiobutton(self.crossValidation, text='K-fold', variable=self.crossValidationVariable, value='kf', command=self.selectKFold)
        self.kFoldRadiobutton.grid(column=0, columnspan=2, row=1, sticky=W)
        self.stratifiedShuffleSplitRadiobutton = Radiobutton(self.crossValidation, text='Strat. Shuffle Split', variable=self.crossValidationVariable, value='sss', command=self.selectShuffleSplit)
        self.stratifiedShuffleSplitRadiobutton.grid(column=0, columnspan=2, row=2, sticky=W)
        self.shuffleSplitRadiobutton = Radiobutton(self.crossValidation, text='Shuffle Split', variable=self.crossValidationVariable, value='ss', command=self.selectShuffleSplit)
        self.shuffleSplitRadiobutton.grid(column=0, columnspan=2, row=3, sticky=W)
        self.loloRadiobutton = Radiobutton(self.crossValidation, text='Leave-one-label-out', variable=self.crossValidationVariable, value='lolo', command=self.selectLOLO)
        self.loloRadiobutton.grid(column=0, columnspan=2, row=4, sticky=W)
        self.lploRadiobutton = Radiobutton(self.crossValidation, text='Leave-p-label-out', variable=self.crossValidationVariable, value='lplo', command=self.selectLPLO)
        self.lploRadiobutton.grid(column=0, columnspan=2, row=5, sticky=W)
        self.foldsVariable = StringVar()
        self.foldsVariable.set(3)
        self.foldsLabel = Label(self.crossValidation, text='   Folds')
        self.foldsLabel.grid(column=0, row=6, sticky=W)
        self.foldsEntry = Entry(self.crossValidation, justify=RIGHT, width=4, textvariable=self.foldsVariable, validate='key', validatecommand=(validateInt, '%P'))
        self.foldsEntry.grid(column=1, row=6, sticky=W)
        self.nIterVariable = StringVar()
        self.nIterVariable.set(3)
        self.nIterLabel = Label(self.crossValidation, text='   Iterations')
        self.nIterEntry = Entry(self.crossValidation, justify=RIGHT, width=4, textvariable=self.nIterVariable, validate='key', validatecommand=(validateInt, '%P'))
        self.cvTestSizeVariable = StringVar()
        self.cvTestSizeVariable.set(25)
        self.cvTestSizeLabel = Label(self.crossValidation, text='   Test Size(%)')
        self.cvTestSizeEntry = Entry(self.crossValidation, justify=RIGHT, width=4, textvariable=self.cvTestSizeVariable, validate='key', validatecommand=(validateInt, '%P'))
        self.pVariable = StringVar()
        self.pVariable.set(3)
        self.pLabel = Label(self.crossValidation, text='   Leave P Out')
        self.pEntry = Entry(self.crossValidation, justify=RIGHT, width=4, textvariable=self.pVariable, validate='key', validatecommand=(validateInt, '%P'))
        self.stratifiedKFoldRadiobutton.select()

    def selectKFold(self):
        self.foldsLabel.grid(column=0, row=6, sticky=W)
        self.foldsEntry.grid(column=1, row=6, sticky=W)
        self.nIterLabel.grid_forget()
        self.nIterEntry.grid_forget()
        self.cvTestSizeLabel.grid_forget()
        self.cvTestSizeEntry.grid_forget()
        self.pLabel.grid_forget()
        self.pEntry.grid_forget()

    def selectLOLO(self):
        self.foldsLabel.grid_forget()
        self.foldsEntry.grid_forget()
        self.nIterLabel.grid_forget()
        self.nIterEntry.grid_forget()
        self.cvTestSizeLabel.grid_forget()
        self.cvTestSizeEntry.grid_forget()
        self.pLabel.grid_forget()
        self.pEntry.grid_forget()

    def selectLPLO(self):
        self.foldsLabel.grid_forget()
        self.foldsEntry.grid_forget()
        self.nIterLabel.grid_forget()
        self.nIterEntry.grid_forget()
        self.cvTestSizeLabel.grid_forget()
        self.cvTestSizeEntry.grid_forget()
        self.pLabel.grid(column=0, row=9, sticky=W)
        self.pEntry.grid(column=1, row=9, sticky=W)

    def selectShuffleSplit(self):
        self.foldsLabel.grid_forget()
        self.foldsEntry.grid_forget()
        self.nIterLabel.grid(column=0, row=7, sticky=W)
        self.nIterEntry.grid(column=1, row=7, sticky=W)
        self.cvTestSizeLabel.grid(column=0, row=8, sticky=W)
        self.cvTestSizeEntry.grid(column=1, row=8, sticky=W)
        self.pLabel.grid_forget()
        self.pEntry.grid_forget()

    def getScores(self):
        return self.scoringVariable.get()

    def getCVParameters(self):
        cv_parameters = {}
        cv_parameters['cvType'] = self.crossValidationVariable.get()
        cv_parameters['folds'] = int(self.foldsVariable.get())
        cv_parameters['nIter'] = int(self.nIterVariable.get())
        cv_parameters['testSize'] = int(self.cvTestSizeVariable.get())/100.
        cv_parameters['p'] = int(self.pVariable.get())
        return cv_parameters

    def getTunedParameters(self):
        tuned_parameters = []
        C = list(set(self.cFrame.getValues()))
        C = [float(x) for x in C]
        C.sort(reverse=True)
        gamma = list(set(self.gammaFrame.getValues()))
        gamma = [float(x) for x in gamma]
        gamma.sort(reverse=True)
        coef0 = list(set(self.coefFrame.getValues()))
        coef0 = [float(x) for x in coef0]
        coef0.sort(reverse=True)
        degree = list(set(self.degreeFrame.getValues()))
        degree = [float(x) for x in degree]
        degree.sort(reverse=True)

        if self.rbfVariable.get() == 1:
            tuned_parameters.append({'kernel':['rbf'], 'C':C, 'gamma':gamma})
        if self.linearVariable.get() == 1:
            tuned_parameters.append({'kernel':['linear'], 'C':C})
        if self.sigmoidVariable.get() == 1:
            tuned_parameters.append({'kernel':['sigmoid'], 'C':C, 'gamma':gamma, 'coef0':coef0})
        if self.polyVariable.get() == 1:
            tuned_parameters.append({'kernel':['poly'], 'C':C, 'gamma':gamma, 'coef0':coef0, 'degree':degree})

        return tuned_parameters

if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = SVMWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

