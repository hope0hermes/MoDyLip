#!/usr/bin/python3
#encoding-utf8

def main():
    """
    The goal of machine learning is to predict features from unknown data sets.

    Learning problems can be separated in two categories:

        - Supervised: Which include classifying target attributes. The
          algorithms applied to this kind of problems include 'classifiers' and
          'regression'.

        - Unsupervised: Which do not include target attributes. The algorithms
          applied to these problems include 'clustering' and
          'density estimation'.

    Scikit learn includes (within the 'datasets' module) sample data bases to
    explore the implementation of machine learning algorithms ('iris', 'digits',
    'boston', 'diabetes' and 'linnerud'). The data an target features of these
    data sets are stored in homonymous attributes of the corresponding class
    instance.
    """
    dat_set = datasets.load_digits()
    print('\ndat_set.data = ')
    print(dat_set.data)
    print('\ndat_set.target')
    print(dat_set.target)

    """
    The learning process consist on using a subset of the input data to train or
    fit an 'estimator' or classifier. After the training process, the estimator
    can be used to predict or classify new data.

    In scikit-learn, an estimator for classification is a Python object that
    implements the methods 'fit(X, y)'' and 'predict(T)'. The constructor of an
    estimator takes as arguments the parameters of the model. These parameters,
    however, can be automatically found with the aid of tools such as
    'grid search' or 'cross validation'.

    An example of an estimator is the class 'sklearn.svm.SVC' that implements
    support vector classification.
    """
    clf = svm.SVC(gamma = 0.001, C = 100.)
    clf.fit(dat_set.data[:-1], dat_set.target[:-1])
    res = clf.predict(dat_set.data[-1])
    print('\nPrediction for the last point in dat_set')
    print(res)


if(__name__ == '__main__'):
    from sklearn import datasets
    from sklearn import svm

    main()