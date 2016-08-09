#!/usr/bin/python3
#encoding-utf8

def lin_reg_all_features(headers, data, target):
    """
    Perfortm the linear regression analysis of the provided data samples.
    """
    # Get train and test data sets.
    size = 20
    X_train = data[:-size]
    # Get train and test targets (contrary to data, target was left unchanged).
    y_train = target[:-size]
    # Train the classifier (linear regression model).
    clf = linear_model.LinearRegression()
    clf.fit(X_train, y_train)
    # Regression coefficients for each feature (notice there is only one
    # intercept value since features are centered and normalized).
    print('\n{:<7s} {: >9s} {: >9s}'.format('Feature', 'Slope', 'Intercept'))
    for val in headers:
        print('{:<7s} {: >9.3f} {: >9.3f}'.format(
            headers[val], clf.coef_[val], clf.intercept_))

def lin_reg_single_feature(headers, data, target):
    # Select the feature to be analized.
    feat = 1
    # Get train and test data sets.
    size = 150
    X_train = data[:-size,[feat]]
    X_test = data[-size:,[feat]]
    # Get training and true X_test matching labels.
    y_train = target[:-size]
    y_true = target[-size:]
    # Train the classifier.
    least = linear_model.LinearRegression()
    least.fit(X_train, y_train)
    ridge = linear_model.Ridge(alpha = 0.1)
    ridge.fit(X_train, y_train)
    print('\nRegression parameters for {:s}'.format(headers[feat]))
    print('{:<20s} {:>10s} {:>10s}'.format('Model', 'Slope', 'intercept'))
    print('{:<20s} {:10.3f}, {:10.3f}'.format(
        'LSR', least.coef_[0], least.intercept_))
    print('{:<20s} {:10.3f}, {:10.3f}'.format(
        'Ridge', ridge.coef_[0], ridge.intercept_))
    # Predict for the 'test' data sample.
    y_least = least.predict(X_test)
    y_ridge = ridge.predict(X_test)
    plt.scatter(X_test, y_true, label = 'Data')
    plt.plot(X_test, y_least, label = 'Least squares', color = 'b')
    plt.plot(X_test, y_ridge, label = 'Ridge', color = 'r')
    plt.legend(loc = 4)
    plt.show()

def log_reg(header, data, target):
    # Features to be analyzed.
    feat = [0,1]
    # Set the training dataset.
    X = data[:,feat]
    y = target[:]
    # Setup the classifier.
    clf = linear_model.LogisticRegression(C=1e5)
    clf.fit(X, y)
    print('\nLogistic regression coefficients\n', clf.coef_)
    # PLOT BOUNDARY REGIONS.
    # Set grid.
    h = 0.02
    X1_min, X1_max = X[:,[0]].min() - 0.5, X[:,[0]].max() + 0.5
    X2_min, X2_max = X[:,[1]].min() - 0.5, X[:,[1]].max() + 0.5
    XX1,XX2 = np.meshgrid(np.arange(X1_min,X1_max,h),np.arange(X2_min,X2_max,h))
    # Concatenate meshgrid into coordinated pairs.
    in_data = np.c_[XX1.ravel(), XX2.ravel()]
    # Make prediction over coordinated pairs and reshape into matrix.
    Z = clf.predict(in_data).reshape(XX1.shape)
    # Plot boundaries.
    plt.figure()
    plt.pcolormesh(XX1, XX2, Z)
    # Plot trainig dataset.
    plt.scatter(X[:,0], X[:,1], c = y, edgecolors = 'k')
    plt.xlabel(header[0])
    plt.ylabel(header[1])
    plt.show()

def main():
    # LINEAR REGRESSION.
    # Import the diabetes dataset and set its header, which is not included in
    # the sklearn documentation. The original feataures are: age, sex, body mass
    # index, average blood pressure and 6 blood serum measurements. All these
    # columns, however, have been normalized to have zero mean and unitary
    # variance (Euclidian norm?), as pointed out in
    # http://www.stanford.edu/%7Ehastie/Papers/LARS/
    diab_head = {0:'AGE', 1:'SEX', 2:'BMI', 3:'BP', 4:'S1', 5:'S2', 6:'S3',
        7:'S4', 8:'S5', 9:'S6'}
    diabetes = datasets.load_diabetes()
    lin_reg_all_features(diab_head, diabetes.data, diabetes.target)
    lin_reg_single_feature(diab_head, diabetes.data, diabetes.target)
    # LOGISTIC REGRESSION.
    iris_head = {0:'Sepal_length', 1:'Sepal_width',
        2:'Petal_length', 3:'Petal_width'}
    iris = datasets.load_iris()
    log_reg(iris_head, iris.data, iris.target)

if(__name__ == '__main__'):
    from sklearn import datasets
    from sklearn import linear_model
    import numpy as np
    import matplotlib.pyplot as plt
    main()
