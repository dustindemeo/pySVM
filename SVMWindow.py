from Tkinter import *
from EntryFrame import EntryFrame

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        
        self.scoring = LabelFrame(self, text='Select Estimator Based on:')
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

        self.kernel = LabelFrame(self, text='Kernels')
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

        self.c = LabelFrame(self, text='C')
        self.c.grid(column=2, row=0, sticky=EW)
        self.cFrame = EntryFrame(self.c, 3)
        self.cFrame.grid(column=0, row=0)

        self.gamma = LabelFrame(self, text='gamma')
        self.gamma.grid(column=3, row=0, sticky=EW)
        self.gammaFrame = EntryFrame(self.gamma, 1)
        self.gammaFrame.grid(column=0, row=0)

        self.coef = LabelFrame(self, text='coef')
        self.coef.grid(column=4, row=0, sticky=EW)
        self.coefFrame = EntryFrame(self.coef, 1)
        self.coefFrame.grid(column=0, row=0)

        self.degree = LabelFrame(self, text='degree')
        self.degree.grid(column=5, row=0, sticky=EW)
        self.degreeFrame = EntryFrame(self.degree, 1)
        self.degreeFrame.grid(column=0, row=0)

        Button(self, text='test', command=self.getTunedParameters).grid(column=6, row=0)

    def getScores(self):
        return self.scoringVariable.get()

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

