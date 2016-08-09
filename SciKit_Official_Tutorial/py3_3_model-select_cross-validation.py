#!/usr/bin/python3
#encoding-utf8

def simple_score():
    """
    Simple fit quality estimation from the score attribute.
    """
    # Load train and test data.
    size = 200
    digits = datasets.load_digits()
    X_train = digits.data[:-size]
    X_test = digits.data[-size:]
    y_train = digits.target[:-size]
    y_true = digits.target[-size:]
    # Set and train the classifier.
    clf = svm.SVC(C = 1., kernel = 'linear')
    clf.fit(X_train, y_train)
    # Predict for the test dataset.
    score = clf.score(X_test, y_true)
    print('The accurary in the prediction of {:d} samples is {:0.5f}'.format(
        size, score))

def manual_kfold_score():
    """
    Prediction accuracy from the manual splitting into small folds.
    """
    # Load the dataset to be analyzed.
    digits = datasets.load_digits()
    X = digits.data
    y = digits.target
    # Split original data into 'n_subs' subsets.
    n_subs = int(10)
    X_fold = np.array_split(X, n_subs)
    y_fold = np.array_split(y, n_subs)
    # Compute prediction accuracy when testing for one subset, after having
    # trained over the remaining ones.
    scores = list()
    clf = svm.SVC(kernel = 'linear', C = float(1.))
    for idx in range(n_subs):
        # Start with the complete collection of n_subs subsets.
        X_train = list(X_fold)
        y_train = list(y_fold)
        # Remove the idx-th subset and set it as the sample to predict for.
        X_test = X_train.pop(idx)
        y_true = y_train.pop(idx)
        # Merge remaining subsets.
        X_train = np.concatenate(X_train)
        y_train = np.concatenate(y_train)
        # Evaluate scores for each subset.
        scores.append(clf.fit(X_train, y_train).score(X_test, y_true))
    # Print the score of all the runs.
    print('\nScores from the manual implementation')
    for idx in range(n_subs):
        print('run[{:d}] = {:.5f}'.format(idx, scores[idx]))

def auto_kfold_score():
    """
    Automated KFold prediction accuracy using 'cross_validation'
    """
    # Load dataset to be analyzed.
    digits = datasets.load_digits()
    X = digits.data
    y = digits.target
    # Setup the classifier.
    clf = svm.SVC(kernel = 'linear', C = float(1.))
    # Split original data into K folds, train on K-1 and then test on left-out.
    n_subs = int(10)
    k_fold = cv.KFold(len(X), n_subs)
    scores = list()
    for idx_train, idx_test in k_fold:
        scores.append(
            clf.fit(X[idx_train], y[idx_train]).score(X[idx_test], y[idx_test]))
    # Print the score of all the runs.
    print('\nScores from the automated implementation')
    for idx in range(n_subs):
        print('run[{:d}] = {:.5f}'.format(idx, scores[idx]))

def grid_search_optimization():
    """
    sklearn provides an object that, given data, computes the score during the
    fit of an estimator on a parameter grid and chooses the parameters to
    maximize the cross-validation score. The object takes an estimator during
    the construction and exposes an estimator API.
    """
    # Load dataset to be analyzed.
    digits = datasets.load_digits()
    X = digits.data
    y = digits.target
    # Set the list of parameter values to be tried.
    Cs = np.logspace(-3, 3, num = 7, base = 10)
    kernels = ['linear', 'rbf']
    # Create a dictionary with parameter names as keys and list of parameter
    # settings to try as values.
    params = dict(C = Cs, kernel = kernels)
    # Select estimator.
    estim = svm.SVC()
    # Setup classifier and parameters for the cross-validation optimization over
    # the set of parameters 'params'.
    n_folds = int(2)
    clf = GridSearchCV(estimator = estim, param_grid = params, cv = n_folds)
    # Train the classifier.
    clf.fit(X, y)
    print('\nScores for each set of parameters')
    for score in clf.grid_scores_:
        print(score)
    print('\nThe best score from this analysis is ', clf.best_score_)
    print('\nWhich corresponds to the set of parameters ', clf.best_params_)
    print('\nTherefore, the best estimator is ',clf.best_estimator_)

def main():
    # simple_score()
    # manual_kfold_score()
    # auto_kfold_score()
    grid_search_optimization()

if(__name__ == '__main__'):
    from sklearn import datasets, svm
    from sklearn.grid_search import GridSearchCV
    import sklearn.cross_validation as cv
    import numpy as np

    main()
