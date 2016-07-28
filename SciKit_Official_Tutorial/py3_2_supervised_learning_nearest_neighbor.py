#!/usr/bin/python3
#encoding-utf8

def original_example():
    """
    Supervised learning is a link between two data sets: the observed data 'X'
    and an external variable 'y' that we are trying to predict, which is usually
    denoted as 'target' or 'label'.

    If the prediction task is to classify the observations in a set of finite
    labels ('name' the observed objects), the task is said to be a
    'classification'. On the other hand, if the goal is to predict a continuous
    target variable, it said to be a regression task.

    When doing classifications, 'y' is a vector of integers or strings.
    """

    """
    K nearest neighbors: find K of training samples closest in distance to the
    new data point and predict the label from these, i.e., the new data point is
    assigned the data class which has the most representatives within the K
    nearest neighbors of the point.

    The distance can, in general, be any metric measure.
    """
    # Load the iris data set.
    iris = datasets.load_iris()
    # get a randomized pointer to the data set.
    np.random.seed()
    idx = np.random.permutation(len(iris.data))
    # Get training and test sets.
    size = 100
    X = iris.data[idx[:-size]]
    y = iris.target[idx[:-size]]
    X_test = iris.data[idx[-size:]]
    y_true = iris.target[idx[-size:]]
    # Train the classifier.
    clf = KNeighborsClassifier(n_neighbors = 20)
    clf.fit(X, y)
    # Make prediction for the test data set.
    y_test = clf.predict(X_test)
    # Get the prediction score.
    cnt = int(0)
    for n in range(size):
        if(y_test[n] != y_true[n]): cnt += 1
        print(y_test[n], y_true[n])
    score = clf.score(X_test,y_true)
    print('There were {:d} mismatches'.format(cnt))
    print('The score in this run was', score)

def my_example():
    # Load the iris data set.
    iris = datasets.load_iris()
    # get a randomized pointer to the data set.
    np.random.seed()
    idx = np.random.permutation(len(iris.data))
    # Get training and test sets.
    size = 50
    X = iris.data[idx[:-size]]
    X = X[:,[0,2]]
    y = iris.target[idx[:-size]]
    for n,val in enumerate(y):
        if(val == 2): y[n] = 1
    X_test = iris.data[idx[-size:]]
    X_test = X_test[:,[0,2]]
    y_true = iris.target[idx[-size:]]
    for n,val in enumerate(y_true):
        if(val == 2): y_true[n] = 1
    # Train the classifier.
    clf = KNeighborsClassifier(n_neighbors = 5)
    clf.fit(X, y)
    # Make prediction for the test data set.
    y_test = clf.predict(X_test)
    # Get the prediction score.
    cnt = int(0)
    for n in range(size):
        if(y_test[n] != y_true[n]): cnt += 1
        print(y_test[n], y_true[n])
    score = clf.score(X_test,y_true)
    print('There were {:d} mismatches'.format(cnt))
    print('The score in this run was', score)
    col = {0:'k', 1:'r'}
    for n in range(len(X[:,0])):
        plt.scatter(X[n,0], X[n,1], color = col[y[n]])
    col = {0:'r', 1:'k'}
    for n in range(len(X_test[:,0])):
        plt.scatter(X_test[n,0], X_test[n,1], edgecolor = col[y_test[n]],
            marker = '*', s = 150)
    plt.show()

def main():
    #original_example()
    my_example()

if(__name__ == '__main__'):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.neighbors import KNeighborsClassifier

    main()