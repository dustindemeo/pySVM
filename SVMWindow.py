from Tkinter import *
from EntryFrame import EntryFrame

class SVMWindow(Frame):
    def __init__(self, master, **args):
        Frame.__init__(self, master, args)
        
        self.scoring = LabelFrame(self, text='Scoring')
        self.scoring.grid(column=0, row=0, sticky=NSEW)
        self.accuracyVariable = IntVar()
        self.accuracyCheckbutton = Checkbutton(self.scoring, text='accuracy', variable=self.accuracyVariable)
        self.accuracyCheckbutton.grid(column=0, row=0, sticky=W)
        self.average_precisionVariable = IntVar()
        self.average_precisionCheckbutton = Checkbutton(self.scoring, text='avg precision', variable=self.average_precisionVariable)
        self.average_precisionCheckbutton.grid(column=0, row=1, sticky=W)
        self.f1Variable = IntVar()
        self.f1Checkbutton = Checkbutton(self.scoring, text='f1', variable=self.f1Variable)
        self.f1Checkbutton.grid(column=0, row=2, sticky=W)
        self.precisionVariable = IntVar()
        self.precisionCheckbutton = Checkbutton(self.scoring, text='precision', variable=self.precisionVariable)
        self.precisionCheckbutton.grid(column=0, row=3, sticky=W)
        self.recallVariable = IntVar()
        self.recallCheckbutton = Checkbutton(self.scoring, text='recall', variable=self.recallVariable)
        self.recallCheckbutton.grid(column=0, row=4, sticky=W)
        self.roc_aucVariable = IntVar()
        self.roc_aucCheckbutton = Checkbutton(self.scoring, text='roc_auc', variable=self.roc_aucVariable)
        self.roc_aucCheckbutton.grid(column=0, row=5, sticky=W)

        self.kernel = LabelFrame(self, text='Kernels')
        self.kernel.grid(column=1, row=0, sticky=NSEW)
        self.rbfVariable = IntVar()
        self.rbfCheckbutton = Checkbutton(self.kernel, text='rbf', variable=self.rbfVariable)
        self.rbfCheckbutton.grid(column=0, row=0, sticky=W)
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
        scores = []
        if self.accuracyVariable.get() == 1:
            scores.append('accuracy')
        if self.average_precisionVariable.get() == 1:
            scores.append('average_precision')
        if self.f1Variable.get() == 1:
            scores.append('f1')
        if self.precisionVariable.get() == 1:
            scores.append('precision')
        if self.recallVariable.get() == 1:
            scores.append('recall')
        if self.roc_aucVariable.get() == 1:
            scores.append('roc_auc')
        return scores

    def getTunedParameters(self):
        tuned_parameters = []
        C = list(set(self.cFrame.getValues()))
        C.sort(reverse=True)
        gamma = list(set(self.gammaFrame.getValues()))
        gamma.sort(reverse=True)
        coef0 = list(set(self.coefFrame.getValues()))
        coef0.sort(reverse=True)
        degree = list(set(self.degreeFrame.getValues()))
        degree.sort(reverse=True)

        if self.rbfVariable.get() == 1:
            tuned_parameters.append({'kernel':'rbf', 'C':C, 'gamma':gamma})
        if self.linearVariable.get() == 1:
            tuned_parameters.append({'kernel':'linear', 'C':C})
        if self.sigmoidVariable.get() == 1:
            tuned_parameters.append({'kernel':'sigmoid', 'C':C, 'gamma':gamma, 'coef0':coef0})
        if self.polyVariable.get() == 1:
            tuned_parameters.append({'kernel':'poly', 'C':C, 'gamma':gamma, 'coef0':coef0, 'degree':degree})

        return tuned_parameters

if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='SVM Window').pack()
    sw = SVMWindow(tk)
    sw.pack(expand=YES,fill=BOTH)
    tk.mainloop()

