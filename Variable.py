from Tkinter import StringVar

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
        self.defaultType = self.getDefaultType()
        self.selectedType = StringVar()
        self.selectedType.set(self.defaultType)
        self.catDict = None
        #self.numEmpty = countEmpty(self.values)

    def makeCatDict(self):
        catDict = {}
        i = 0
        for v in self.values:
            if v not in catDict:
                catDict[v] = i
                i += 1
        return catDict

    def getDefaultType(self):
        for v in self.values:
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
    
