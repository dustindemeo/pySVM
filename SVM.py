import pprint
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.cross_validation import cross_val_score, KFold, StratifiedKFold, LeaveOneOut, LeavePOut, ShuffleSplit, StratifiedShuffleSplit

def skSVM(X, y, scoring, tuned_parameters, data_parameters, cv_parameters):

    if data_parameters['stratify']:
        split = StratifiedKFold(y=y, n_folds=int(1./data_parameters['testSize']), shuffle=True, random_state=data_parameters['random'])
    else:
        split = KFold(n=len(y), n_folds=int(1./data_parameters['testSize']), shuffle=True, random_state=data_parameters['random'])

    for train, test in split:
        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]
        break

    print "Starting the gridding process."
    print

    numLabel1 = np.count_nonzero(y_train)
    numLabel0 = len(y_train) - numLabel1
    numFiveFolds = len(y_train) % 5
    n_folds = max(2, min(cv_parameters['folds'], numLabel0, numLabel1, numFiveFolds))

    if cv_parameters['cvType'] == 'skf':
        cv = StratifiedKFold(y=y_train, n_folds=n_folds, shuffle=True, random_state=data_parameters['random'])
    elif cv_parameters['cvType'] == 'kf':
        cv = KFold(n=len(y_train), n_folds=n_folds, shuffle=True, random_state=data_parameters['random'])
    elif cv_parameters['cvType'] == 'sss':
        cv = StratifiedShuffleSplit(y=y_train, n_iter=cv_parameters['nIter'], test_size=cv_parameters['testSize'], random_state=data_parameters['random'])
    elif cv_parameters['cvType'] == 'ss':
        cv = ShuffleSplit(n=len(y_train), n_iter=cv_parameters['nIter'], test_size=cv_parameters['testSize'], random_state=data_parameters['random'])
    elif cv_parameters['cvType'] == 'lolo':
        cv = LeaveOneOut(n=len(y_train))
    elif cv_parameters['cvType'] == 'lplo':
        cv = LeavePOut(n=len(y_train), p=cv_parameters['p'])

    grid = GridSearchCV(estimator=SVC(), param_grid=tuned_parameters, scoring = scoring, cv=cv)
    grid.fit(X_train, y_train)
    clf = grid.best_estimator_
    clf.fit(X_train, y_train)
    accuracy_scores = cross_val_score(clf, X_train, y_train, scoring='accuracy', cv=cv)
    precision_scores = cross_val_score(clf, X_train, y_train, scoring='precision', cv=cv)
    recall_scores = cross_val_score(clf, X_train, y_train, scoring='recall', cv=cv)
    f1_scores = cross_val_score(clf, X_train, y_train, scoring='f1', cv=cv)
    y_test_pred = clf.predict(X_test)
    y_train_pred = clf.predict(X_train)

    print
    print "ESTIMATOR SELECTED FOR OPTIMAL {}:".format(grid.get_params(deep=True)['scoring'].upper())
    print "Parameters:"
    pprint.pprint(grid.best_params_, width=1)
    print
    print "Cross-validation scores on training data:"
    print "  Accuracy:  {:.1f} +/- {:.1f}%".format(accuracy_scores.mean() * 100, accuracy_scores.std() * 100)
    print "  Precision: {:.1f} +/- {:.1f}%".format(precision_scores.mean() * 100, precision_scores.std() * 100)
    print "  Recall:    {:.1f} +/- {:.1f}%".format(recall_scores.mean() * 100, recall_scores.std() * 100)
    print "  F1:        {:.1f} +/- {:.1f}%".format(f1_scores.mean() * 100, f1_scores.std() * 100)
    print
    print "Trained estimator scores on testing data:"
    print "  Accuracy:  {:.1f}%".format(accuracy_score(y_test, y_test_pred)*100)
    print "  Precision: {:.1f}%".format(precision_score(y_test, y_test_pred, average='weighted')*100)
    print "  Recall:    {:.1f}%".format(recall_score(y_test, y_test_pred, average='weighted')*100)
    print "  F1:        {:.1f}%".format(f1_score(y_test, y_test_pred, average='weighted')*100)
    print
    print "Trained estimator classification report on testing data:"
    print
    print classification_report(y_test, y_test_pred, target_names=['Fail', 'Pass'])

