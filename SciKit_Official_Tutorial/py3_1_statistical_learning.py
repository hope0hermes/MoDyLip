#!/usr/bin/python3
#encoding-utf8

def main():
    """
    Scikit learn deals with data sets represented as 2D arrays, where (usually)
    the 1st axis represents the 'samples' and the 2nd axis represents the
    features. If the input data does not have the format (n_samples, m_data),
    then it has to be reshaped. An example of this is the digits data set, which
    consists of 1797 images of hand-written numbers, each of these being a 2D
    array of 8x8 pixels.
    """
    digits = datasets.load_digits()
    print('\nShape of the digits data set')
    print(digits.images.shape)

    """
    Within scikit-learn, an estimator is any object that learns from data; it
    may be a classification, regression or clustering algorithm or a transformer
    that extracts/filters features from raw data.

    All estimator objects expose a 'fit' method that takes a data set.

        >>> estimator.fit(data)

    All the parameters of an estimator can be set when it is instantiated or by
    modifying the corresponding attribute.

        >>> estimator = Estimator(param1 = 1.0, param2 = 2.0)
        >>> estimator.param1 = 9.0

    When data is fitted with an estimator, parameters are estimated with the
    data at hand. All the estimated parameters are attributes of the estimator
    object ending by an underscore.

        >>> estimator.estimated_param_
    """


if(__name__ == '__main__'):
    from sklearn import datasets
    from sklearn import svm

    main()