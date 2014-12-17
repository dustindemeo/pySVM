import pprint
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.cross_validation import cross_val_score, KFold, StratifiedKFold, LeaveOneOut, LeavePOut, ShuffleSplit, StratifiedShuffleSplit

def skSVM(X, y, scoring, tuned_parameters, test_size, cv_parameters):

    split = KFold(n=len(y), n_folds=int(1./test_size), shuffle=True, random_state=40)
    split = StratifiedKFold(y=y, n_folds=int(1./test_size), shuffle=True, random_state=40)

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

    if cv_parameters['cvType'] == 'skf':
        n_folds = min(cv_parameters['folds'], numLabel0, numLabel1, numFiveFolds)
        cv = StratifiedKFold(y=y_train, n_folds=n_folds, shuffle=True, random_state=42)
    elif cv_parameters['cvType'] == 'kf':
        n_folds = min(cv_parameters['folds'], numLabel0, numLabel1, numFiveFolds)
        cv = KFold(n=len(y_train), n_folds=n_folds, shuffle=True, random_state=42)
    elif cv_parameters['cvType'] == 'sss':
        cv = StratifiedShuffleSplit(y=y_train, n_iter=cv_parameters['nIter'], test_size=cv_parameters['testSize'], random_state=42)
    elif cv_parameters['cvType'] == 'ss':
        cv = ShuffleSplit(n=len(y_train), n_iter=cv_parameters['nIter'], test_size=cv_parameters['testSize'], random_state=42)
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
    print "Cross-validation scores on training data:"
    print "  Accuracy:  {:.1f} +/- {:.1f}%".format(accuracy_scores.mean() * 100, accuracy_scores.std() * 100)
    print "  Precision: {:.1f} +/- {:.1f}%".format(precision_scores.mean() * 100, precision_scores.std() * 100)
    print "  Recall:    {:.1f} +/- {:.1f}%".format(recall_scores.mean() * 100, recall_scores.std() * 100)
    print "  F1:        {:.1f} +/- {:.1f}%".format(f1_scores.mean() * 100, f1_scores.std() * 100)
    print "Trained estimator scores on training data:"
    print "  Accuracy:  {:.1f}%".format(accuracy_score(y_train, y_train_pred)*100)
    print "  Precision: {:.1f}%".format(precision_score(y_train, y_train_pred, average='weighted')*100)
    print "  Recall:    {:.1f}%".format(recall_score(y_train, y_train_pred, average='weighted')*100)
    print "  F1:        {:.1f}%".format(f1_score(y_train, y_train_pred, average='weighted')*100)
    print "Trained estimator scores on testing data:"
    print "  Accuracy:  {:.1f}%".format(accuracy_score(y_test, y_test_pred)*100)
    print "  Precision: {:.1f}%".format(precision_score(y_test, y_test_pred, average='weighted')*100)
    print "  Recall:    {:.1f}%".format(recall_score(y_test, y_test_pred, average='weighted')*100)
    print "  F1:        {:.1f}%".format(f1_score(y_test, y_test_pred, average='weighted')*100)
    print
    '''
    print "Grid scores:"
    print grid.grid_scores_
    print
    print "Best estimator:"
    print grid.best_estimator_
    print 
    print "Best score:"
    print grid.best_score_
    print
    print "Best params:"
    print grid.best_params_
    print
    print "Scorer:"
    print grid.scorer_
    print
    print "test"
    print y_test
    print "pred"
    print y_test_pred
    print
    '''

    print "Classification report on test set:"
    print classification_report(y_test, y_test_pred)

    '''
    plt.set_cmap(pl.cm.Paired)
    plt.figure(1)
    plt.clf()
    plt.scatter(X[:,0], X[:,1], c=y, zorder=10)
    plt.scatter(X_test[:,0], X_test[:, 1], s=80, facecolors='none', zorder=10)
    plt.axis('tight')
    x_min = X[:,0].min()
    x_max = X[:,0].max()
    y_min = X[:,1].min()
    y_max = X[:,1].max()
    y_min = X[:,1].min()
    y_max = X[:,1].max()
    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])
    # Put the result into a color plot
    Z = Z.reshape(XX.shape)
    plt.pcolormesh(XX, YY, Z > 0)
    plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])
    plt.title('Test')
    '''
