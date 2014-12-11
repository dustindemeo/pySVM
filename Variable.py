#NAME: Variable.py
#DATE CREATED: 12/10/2014
#AUTHORS: Abhinandan Halemane, Dustin DeMeo, Mahshid Aimaq, Vinitha Raja

'''
DESCRIPTION:
This module holds accessory functions and base classes for the core SVM functionality. 

Currently, the only accessory function is the isNumber function to determine if a string/value can be cast to a number. 

Currently, the only class is the Variable class which holds all data relevant to a variable, equivalent to a column in the original CSV file. More classes will be modularized out of the main code before project submission.

MODIFICATION HISTORY:
12/10/14: File created. Added field to Variable class. 
AUTHOR: Abhinandan Halemane, Dustin DeMeo, Mahshid Aimaq, Vinitha Raja
Description: isNumber function and Variable class removed from main routine to modularize code. Added numEmpty to Variable class in order to track the number of empty values to alert users.
'''

from Tkinter import StringVar

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

class Variable():
    '''DESCRIPTION: This class holds all pertinent information regarding each variable. This is a combination of the information from the CSV (by column) and from user input via the GUI. Note, each column in the spreadsheet can be thought of as a Variable.
    ATTRIBUTES: index = int. the column number in the CSV file
                name = string. the header cell in the CSV file
                values = list of strings. a list of the values, aka the cells below the header
                defaultType = string. a guess at the type of variable - 'Scalar IV' if all numerical values, 'Categorical IV' otherwise
                selectedType = TkInter StringVar. a StringVar bound to the GUI radioboxes for user defined variable type ('Scalar IV', 'Categorical IV', 'Binary DV', or 'Skip')
                catDict = dictionary. uninitialized unless variable used as 'Categorical IV' or 'Binary DV'. one to one mapping of unique values with sequential integers
                numEmpty = int. the number of empty values for the Variable (aka '' in the cell of the column of the CSV)
    FUNCTIONS: makeCatDict = makes a catDict from values in the Variable
               getDefaultType = determines if a Variable can be Scalar (i.e. if all values are numerical)
               countEmpty = counts the number of empty values in a Variable (i.e. how many cells in a column are '')'''

    def __init__(self, index, column):
        '''DESCRIPTION: Initializes the Variable class. Auto initializes all attributes except for catDict which is only created if the Variable is 'Categorical IV' or 'Binary DV' during SVM initialization.
        PRECONDITIONS: index = int. the column number that the Variable came from in the CSV file/matrix. Error if it is not an integer.
                       column = numpy record array. the column of the csv file. Error if no values.
        POSTCONDITIONS: Variable instance will be returned to the calling function
        SIDE EFFECTS: None
        RETURN: Variable instance with attributes initialized.
        >>> Variable(0, scalarColumn).index
        0
        >>> Variable(1, categoricalColumn).index
        1
        >>> Variable(2, emptyColumn).index
        2
        '''
        
        self.index = index
        self.name = column[0]
        self.values = column[1:,]
        self.defaultType = self.getDefaultType()
        self.selectedType = StringVar()
        self.selectedType.set(self.defaultType)
        self.catDict = None
        self.numEmpty = self.countEmpty()

    def makeCatDict(self):
        '''DESCRIPTION: Makes a dictionary of all the categories for a 'Catigorical IV'
        PRECONDITIONS: Called on a Variable instance. Requires that the Variable instance have values.
        POSTCONDITIONS: returns catDict to the calling function
        SIDE EFFECTS: None
        RETURN: dictionary. dictionary of unique values mapped to unique sequential integers
        '''

        catDict = {}
        i = 0
        for v in self.values:
            if v not in catDict:
                catDict[v] = i
                i += 1
        return catDict

    def getDefaultType(self):
        '''DESCRIPTION: Guesses a default type of independent variable
        PRECONDITIONS: Called on a Variable instance. Requires that the Variable instance have values.
        POSTCONDITIONS: returns defaultType to the calling function
        SIDE EFFECTS: None
        RETURN: string. 'Scalar IV' if all values are numerical. 'Categorical IV' otherwise
        '''

        for v in self.values:
            if v == '':
                pass
            elif not isNumber(v):
                return 'Categorical IV'
        return 'Scalar IV'

    def countEmpty(self):
        '''DESCRIPTION: Counts the number of empty values in Variable (useful to determine which to skip)
        PRECONDITIONS: Called on a Variable instance. Requires that the Variable instance have values.
        POSTCONDITIONS: returns the number of empty values in Variable (aka empty cells in column)
        SIDE EFFECTS: None
        RETURN: int. number of empty values in a variable
        '''

        numEmpty = 0
        for v in self.values:
            if v == '':
                numEmpty += 1
        return numEmpty

if __name__ == "__main__":
    import doctest
    import numpy as np
    from Tkinter import Tk
    Tk()
    scalarColumn = np.array([('Scalar Header', 1, 2, 3, 4, 5)], dtype=('a20,i,i,i,i,i'))
    categoricalColumn = np.array([('Categorical Header', 'one', 'two', 'three', 'four', 'five')], dtype=('a20,a20,a20,a20,a20,a20'))
    emptyColumn = np.array([('Empty Column')], dtype=('a20'))
    doctest.testmod(extraglobs={'scalarColumn': scalarColumn, 'categoricalColumn': categoricalColumn, 'emptyColumn': emptyColumn, \
                                's': Variable(1, scalarColumn), 'c': Variable(1, categoricalColumn), 'e': Variable(2, emptyColumn)})
