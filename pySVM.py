#Note: this is a draft of the project. You must use the DrColby_data2.csv file (attached) because
#      the results are merged into Yes for Success and No for Fail (i.e. no longer 5 results categories)
# this is a test
#Note: You have to install numpy and sklearn to get this to work

import numpy as np
import itertools
from sklearn.svm import SVC

#load the csv into a numpy array
csv = np.loadtxt(open("DrColby_data.csv", "rb"), dtype='string', delimiter=",", skiprows=0)

#make a dictionary to store how to treat each column - categoical, scalar, or skip
data_types = {'Patient_Number':'skip', \
              'Successful':'categorical', \
              'age':'scalar', \
              'gender':'categorical', \
              'race':'categorical', \
              'num_aneurysms_tx':'scalar', \
              'anterior_circulation_aneurysms':'categorical', \
              'Posterior_circulation_aneurysms':'categorical', \
              'aneurysm_size':'categorical', \
              'aneurysm_type':'categorical', \
              'Procedural_Access':'categorical', \
              'Guide_catheter':'categorical', \
              'Marksman_catheter_length_(cm)':'scalar', \
              'Num_PEDs_anterior':'scalar', \
              'Num_PEDs_posterior':'scalar', \
              'Immediate_angiographic_result_post_PED_deployment':'dependent', \
              'Mean_post_procedure_hospital_stay_anterior(days)':'scalar', \
              'Mean_post_procedure_hospital_stay_Posterior(days)':'scalar', \
              'Patient_dischsrged_home_anterior':'skip', \
              'Patient_dischsrged_home_posterior':'skip'}
              
#make a dictionary to store how to treat binary dependent variable - 1 = pass, 0 = fail
outcomes = {'N':1, \
            'MI':1, \
            'MO':0, \
            'P':0, \
            'C':0}
              
#delete all columns that should be skipped
mask_columns = []
for i, column in enumerate(csv[0,:]):
    if data_types[column] == 'skip':
        mask_columns.append(i)
clean_column = np.delete(csv, mask_columns, axis=1)

#delete all rows that have empty values
mask_rows = []
for i, row in enumerate(clean_column):
    for column in row:
        if column.strip(' \t\n\r') == '':
            mask_rows.append(i)
clean_all = np.delete(clean_column, mask_rows, axis=0)

#split data into header and data
header = clean_all[0,:]
data = clean_all[1:,:]

#separate data into indepdendent variables and dependent variables
DV_column_index = np.where(header=='Immediate_angiographic_result_post_PED_deployment')[0][0]
DV = data[:,DV_column_index]
IV = np.delete(data,DV_column_index,1)

#build dictionaries for categorical values per column
#leave floats and integers and remove patient id
col_dicts = []
for i in range(len(IV[0])):
    col_dicts.append({})
    if data_types[header[i]] == 'categorical':
        k = 0
        for j in IV[:,i]:
            if j not in col_dicts[i]:
                col_dicts[i][j] = k
                k += 1

#build a new matrix using the converted data (i.e. categorical values have been converted to integers per category)
#this is the matrix we will use for IVs
X = np.copy(IV)
for i, row in enumerate(X):
    for j, val in enumerate(row):
        if data_types[header[j]] == 'categorical':
            X[i][j] = int(col_dicts[j][val])
        elif data_types[header[j]] == 'scalar':
            X[i][j] = float(X[i][j])
            
# and this is the matrix we will use for DVs
temp = []
for i in DV:
    temp.append(outcomes[i])
y = np.array(temp, dtype=int)

'''BEGIN DR. WESLEY CODE'''

import csv, sys, os
import numpy as np
from sklearn import svm, cross_validation, metrics, preprocessing
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, precision_score, recall_score
import pdb

# Now perform "gridding" to help find the best SVM kernel and parameters.
"""
The following variables specify the kernels that we wish to test for.
"""
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.0, 1e-2, 1e-3, 1e-4], 'C': [1, 10, 100, 1000, 10000] }, \
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000, 10000] }, \
                    {'kernel': ['poly'], 'degree': [1, 2, 3], 'coef0': [0.0, 1., 2.], 'C': [1, 10, 100, 1000, 10000] }, \
                    {'kernel': ['sigmoid'], 'degree': [1, 2, 3],  'coef0': [0.0, 1., 2.],  'gamma': [0.0, 1e-2, 1e-3, 1e-4], 'C': [1, 10, 100, 1000, 10000]}  ]
"""
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.0, 1e-2], 'C': [1, 10] },\
                    {'kernel': ['linear'], 'C': [1, 10] }]

tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.0, 1e-2, 1e-3, 1e-4], 'C': [1, 10, 100] }]
"""

# What types of scores do we wist to optimize for
scores = [ ('accuracy', 'accuracy'), ('average_precision', 'average_precision'), ('recall', 'recall')]

print "Starting the gridding process."
# find out how many class 0 and class 1 entries we have.
# we need to use the nimimun number for cross validation 
# purposes.
num_class_0 = list(y).count(0)
num_class_1 = list(y).count(1)
cv_size = min(num_class_0, num_class_1)

"""
Now we loop through the list of kernels and parameter setting 
to try and get as close as possible to the best setting to
use for our prediction machine. 
"""

clf_array = []

for score_name, score_func in scores:
    clf_array.append(GridSearchCV( SVC(C=1), tuned_parameters, scoring = score_func))
    
for clf in clf_array:
    clf.fit(X, y)
    #"""
    clf_scores = cross_validation.cross_val_score(clf, X, y, cv = cv_size)
    print
    print "CLF SCORES: ==================================="
    print  score_name, ": %0.2f (+/- %0.2f)" % (clf_scores.mean(), clf_scores.std() * 2)
    print "==============================================="
    print "Best parameters set found on development set:"
    print
    print clf.best_estimator_
    print 
    print
    
"""
Below is an example of how to generate training and test data sets
using sklean's  functions. In this example, the test_size=0.2
parameter extracts a test data set that is 20% of the entire
dataset. You can change the percentage to whatever you like, but
values between 20% and 50% are not unreasonable, depending on
the size of the original data set.
"""
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=0)
print "X_train shape =", X_train.shape, "  y_train shape=", y_train.shape
print "X_test shape =", X_test.shape, "  y_test shape=", y_test.shape
print

"""
The following lines train the SVM using our extracted training dataset and
is parameterized based on the gridding results. Then the trained SVM is
used to carry out predictions on the test data set. The percentage 
of accuract predictions is printed
"""
#clf = svm.SVC(kernel='rbf', C=1, gamma = 0.0, degree = 3.0, coef0 = 0.0).fit(X_train, y_train)
clf_array[0].fit(X_train, y_train)
print "clf.get_params(deep=True) =", clf_array[0].get_params(deep=True)
print "clf.score(X_test, y_test) = {0}%".format(int((clf_array[0].score(X_test, y_test) * 10000))/100.)
print

clf_array[1].fit(X_train, y_train)
print "clf.get_params(deep=True) =", clf_array[1].get_params(deep=True)
print "clf.score(X_test, y_test) = {0}%".format(int((clf_array[1].score(X_test, y_test) * 10000))/100.)
print

clf_array[2].fit(X_train, y_train)
print "clf.get_params(deep=True) =", clf_array[2].get_params(deep=True)
print "clf.score(X_test, y_test) = {0}%".format(int((clf_array[2].score(X_test, y_test) * 10000))/100.)
print 

'''
#slice training matrix
#TODO: randomize which 80% and make sure you have an equal number from each class
train = np.delete(transcribed,14,1)[:25]
train_results = transcribed[:25,14].flatten()

#slice testing matrix (note, there is actually a testing function so we don't need to iterate through these with predict)
test = np.delete(transcribed,14,1)[25:]
test_results = transcribed[25:,14].flatten()

clf = SVC()
clf.fit(train, train_results)
for t, r in itertools.izip (test, test_results):
    if clf.predict(t) == r:
        print "yay!"
        
#look up gridding to determine best cross validation (look for cross validation of 90-95%)
#todo: still need to convert values back into original format (lookup from dict)

#TODO: lookup principle component analysis to determine which variables are the most important
#TODO: ask for datasets for other devices so that we can predict which device is best for a patient
#TODO: return marginal cases and flag for further testing (see support vectors aka marginal vectors)'''