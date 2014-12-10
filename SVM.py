import csv, sys, os
import numpy as np
from sklearn import svm, cross_validation, metrics, preprocessing
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, precision_score, recall_score
import pdb


def skSVM(X, y):
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
    of accurate predictions is printed
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
