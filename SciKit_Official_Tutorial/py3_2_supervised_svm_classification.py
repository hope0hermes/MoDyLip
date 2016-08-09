#!/usr/bin/python3
#encoding-utf8

class Mesh:
    """
    Grid discretization of the analysis region.
    """
    def __init__(self, X, Y, h = float(0.01)):
        self.set_mesh_(X, Y, h)

    def set_mesh_(self, X, Y, h = 0.02):
        """
        Sets an evenly-spaced mesh ((xx, yy) with grid spacing h) over the
        region:

            D = (X_min, X_max) x (Y_min, Y_max)

        'pair_list' stores the list of coordinated pairs in D and 'shape'
        stores the grid's number of rows and columns.
        """
        x_min, x_max = X.min() - 0.5, X.max() + 0.5
        y_min, y_max = Y.min() - 0.5, Y.max() + 0.5
        self.xx, self.yy = np.meshgrid(
            np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        self.pair_list = np.c_[self.xx.ravel(), self.yy.ravel()]
        self.shape = self.xx.shape

def plot_boundaries(head, data, target, mesh, Z, method):
    """
    Plot boundaries as evaluated by the classifier 'method'.
    """
    plt.figure()
    # Region boundaries.
    plt.pcolormesh(mesh.xx, mesh.yy, Z)
    # Training dataset.
    plt.scatter(data[:,[0]], data[:,[1]], c = target)
    # Enable interactive mode.
    # plt.ion()
    # Axes labels.
    plt.xlabel(head[0]), plt.ylabel(head[1])
    plt.title(method)
    plt.legend(loc = 4)
    plt.show()

def classifier_svc_linear(head, data, target, mesh, reg):
    """
    Boundary regions evaluated with SVC using the linear kernel.
    """
    # Setup SVC classifier.
    clf = svm.SVC(kernel = 'linear', C = reg)
    clf.fit(data, target)
    # Evaluate boundaries.
    Z = clf.predict(mesh.pair_list).reshape(mesh.shape)
    # Plot boundaries.
    plot_boundaries(head, data, target, mesh, Z, 'SVC(linear)')

def classifier_svc_rbf(head, data, target, mesh, reg):
    """
    Boundary regions evaluated with SVC using the rbf kernel.
    """
    # Setup SVC classifier.
    clf = svm.SVC(kernel = 'rbf', gamma = 0.7, C = reg)
    clf.fit(data, target)
    # Evaluate boundaries.
    Z = clf.predict(mesh.pair_list).reshape(mesh.shape)
    # Plot boundaries.
    plot_boundaries(head, data, target, mesh, Z, 'SVC(rbf)')

def classifier_svc_poly(head, data, target, mesh, reg, deg):
    """
    Boundary regions evaluated with SVC using the polynomial kernel of degree
    deg.
    """
    # Setup SVC classifier.
    clf = svm.SVC(kernel = 'poly', degree = deg, C = reg)
    clf.fit(data, target)
    # Evaluate boundaries.
    Z = clf.predict(mesh.pair_list).reshape(mesh.shape)
    # Plot boundaries.
    plot_boundaries(head, data, target, mesh, Z, 'SVC(poly)')

def main():
    # Data header and features to be investigated.
    head = {0:'Sepal_length',1:'Sepal_width',2:'Petal_length',3:'Petal_width'}
    feat = [0,1]
    # Set training data and labels from the iris dataset.
    iris = datasets.load_iris()
    data = iris.data[:,feat]
    target = iris.target[:]
    # Set meshgrid to evaluate the class boundaries.
    mesh = Mesh(X = data[:,[0]], Y = data[:,[1]], h = 0.01)
    # Set regularization parameter for all SVC classifiers.
    reg = float(1.)
    # Evaluate boundaries with different SVC classifiers.
    classifier_svc_linear(head, data, target, mesh, reg)
    classifier_svc_rbf(head, data, target, mesh, reg)
    classifier_svc_poly(head, data, target, mesh, reg, deg = 3)

if(__name__ == '__main__'):
    from sklearn import datasets, svm
    import matplotlib.pyplot as plt
    import numpy as np

    main()
