#import csv, sys, os
import numpy as np
from sklearn import svm, cross_validation, metrics, preprocessing
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, precision_score, recall_score
import pdb
from sklearn.cross_validation import train_test_split



def skSVM(X, y, scoring, tuned_parameters, test_size):

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=test_size, random_state=1)

    print "Starting the gridding process."
    # find out how many class 0 and class 1 entries we have.
    # we need to use the nimimun number for cross validation 
    # purposes.
    num_class_0 = list(y_train).count(0)
    num_class_1 = list(y_train).count(1)
    cv_size = min(num_class_0, num_class_1)

    """
    Now we loop through the list of kernels and parameter setting 
    to try and get as close as possible to the best setting to
    use for our prediction machine. 
    """

    clf_array = []

    for score in scoring:
        clf_array.append(GridSearchCV(estimator=SVC(), param_grid=tuned_parameters, scoring = score))
    
    for clf in clf_array:
        clf_scores = cross_validation.cross_val_score(clf, X, y, cv=cv_size)
        clf.fit(X_train, y_train)

        print "CLF SCORES: ==================================="
        print  "{}: {:.1f}% (+/- {:.1f}%)".format(clf.get_params(deep=True)['scoring'], clf_scores.mean() * 100, clf_scores.std() * 2 * 100)
        print "==============================================="
        print
        print "Best parameters set found on development set:"
        print clf.best_estimator_
        print
        print "CLF score on train set:"
        print "clf.score(X_train, y_train) = {:.1f}%".format(clf.score(X_train, y_train)*100)
        print
        print "CLF score on test set:"
        print "clf.score(X_test, y_test) = {:.1f}%".format(clf.score(X_test, y_test)*100)
        print 
