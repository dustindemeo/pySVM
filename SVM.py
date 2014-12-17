import numpy as np
from sklearn import svm, cross_validation, metrics
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, precision_score, recall_score
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as pl
from sklearn.cross_validation import KFold


def skSVM(X, y, scoring, tuned_parameters, test_size, folds):

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=test_size, random_state=1)

    print "Starting the gridding process."
    # find out how many class 0 and class 1 entries we have.
    # we need to use the nimimun number for cross validation 
    # purposes.
    #if folds <= 0:
    #    num_class_0 = list(y).count(0)
    #    num_class_1 = list(y).count(1)
    #    cv_size = min(num_class_0, num_class_1)
    #else:
    #    cv_size = folds

    cv_size = KFold(n=len(y_train), n_folds=3, shuffle=False, random_state=0)

    """
    Now we loop through the list of kernels and parameter setting 
    to try and get as close as possible to the best setting to
    use for our prediction machine. 
    """

    for score in scoring:
        clf = GridSearchCV(estimator=SVC(), param_grid=tuned_parameters, scoring = score, cv=2)
        clf.fit(X_train, y_train)
        clf2 = clf.best_estimator_
        clf2.fit(X_train, y_train)
        clf_scores = cross_validation.cross_val_score(clf2, X_train, y_train, cv=2)
        print clf.get_params(deep=True)

        print "CROSS-VALIDATION SCORES: ======================"
        print "{}: (mean +/- std): {:.1f}% +/- {:.1f}%".format(clf.get_params(deep=True)['scoring'], clf_scores.mean() * 100, clf_scores.std() * 100)
        print "==============================================="
        print
        print "Grid scores:"
        print clf.grid_scores_
        print
        print "Best estimator:"
        print clf.best_estimator_
        print 
        print "Best score:"
        print clf.best_score_
        print
        print "Best params:"
        print clf.best_params_
        print
        print "Scorer:"
        print clf.scorer_
        print
        print "CLF score on train set:"
        print "clf.score(X_train, y_train) = {:.1f}%".format(clf2.score(X_train, y_train)*100)
        print
        print "CLF score on test set:"
        print "clf.score(X_test, y_test) = {:.1f}%".format(clf2.score(X_test, y_test)*100)
        print


        y_true, y_pred = y_test, clf.predict(X_test)
        print "Classification report on test set:"
        print classification_report(y_true, y_pred)

        '''
        pl.set_cmap(pl.cm.Paired)
        pl.figure(1)
        pl.clf()
        pl.scatter(X[:,0], X[:,1], c=y, zorder=10)
        pl.scatter(X_test[:,0], X_test[:, 1], s=80, facecolors='none', zorder=10)
        pl.axis('tight')
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
        pl.pcolormesh(XX, YY, Z > 0)
        pl.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])
        pl.title('Test')
        '''
