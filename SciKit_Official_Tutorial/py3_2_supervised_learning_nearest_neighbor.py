#!/usr/bin/python3
#encoding-utf8

def my_example():
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
    # Get a randomized pointer to the data set.
    np.random.seed()
    idx = np.random.permutation(len(iris.data))
    # Get training and test feature sets.
    size = 50
    X = iris.data[idx[:-size]]
    X_test = iris.data[idx[-size:]]
    # In this particular example we will only be interested in the first two
    # features; 'sepal lenght' and 'sepal widtht'.
    X = X[:,[0,1]]
    X_test = X_test[:,[0,1]]
    # Get training and test labels.
    y = iris.target[idx[:-size]]
    y_true = iris.target[idx[-size:]]
    # Train the classifier.
    clf = KNeighborsClassifier(n_neighbors = 5)
    clf.fit(X, y)
    # Make prediction for the test data set.
    y_test = clf.predict(X_test)
    # Print missclasifications.
    for idx, predic in enumerate(y_test):
        real = y_true[idx]
        if(real != predic):
            print('(real, predicted) = ({:d}, {:d})'.format(predic, real))
    # Get prediction's score.
    score = clf.score(X_test,y_true)
    print('The score in this run was', score)
    # Print traing and test data sets.
    col = {0:'k', 1:'r', 2:'g'}
    for n in range(len(X[:,0])):
        plt.scatter(X[n,0], X[n,1], color = col[y[n]])
    for n in range(len(X_test[:,0])):
        plt.scatter(X_test[n,0], X_test[n,1], marker = 'o', s = 100,
        linewidth = '2', facecolor = 'none', edgecolor = col[y_test[n]])
    plt.show()

def main():
    my_example()

if(__name__ == '__main__'):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.neighbors import KNeighborsClassifier

    main()
