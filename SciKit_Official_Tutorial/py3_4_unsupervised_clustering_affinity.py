#!/usr/bin/python3
#encoding-utf8

def affinity_propagation():
    """
    AffinityPropagation creates clusters by sending messages between pairs of
    samples until convergence. The messages sent between pairs represent the
    suitability for one sample to be the exemplar of the other, which is updated
    in response to the values from other pairs. this updates occurs iteratively
    until convergence, at which point the final exemplars are chosen and hence
    the final cluster is given.

    Algorithm:

    The message sent between pairs belongs to one of two categories. The first
    is the responsibility, r(i,k), which is the accumulated evidence that sample
    k should the exemplar for sample i. The second is the availability, a(i,k),
    which is the accumulated evidence that sample i should chose sample k to be
    its exemplar, and considers the values for all other samples that k should
    be an exemplar. In this case exemplars are chosen by samples if they are:

        - similar enough to many samples, and
        - chosen by many samples to be representative of themselves.
    """
    # Generate a generic data sample.
    n_samples = 300
    std = 0.3
    seed = 0
    centers = [ [-1., 0.], [0., 1.5], [1., 0.] ]
    data, target = make_blobs(n_samples = n_samples, centers = centers,
        cluster_std = std, random_state = seed)

    # Set the preference for each point: samples with large preference values
    # are more likely to be chosen as exemplars. The number of exemplars, i.e.,
    # clusters, is influenced by the input preference values. If preferences are
    # not passed as arguments, they will be set to the median of the input
    # similarities.
    # pref = [ np.random.randint(low = -50, high = 0) for x in range(n_samples)]
    pref = -50
    # Compute affinity propagation.
    clf = AffinityPropagation(preference = pref)
    aff_y = clf.fit_predict(data)
    # Find mismatches between predicted and true values.
    cnt = int(0)
    for idx in range(n_samples):
        if(target[idx] != aff_y[idx]): cnt += 1
    # Print results.
    print('Approximated number of clusters ', len(clf.cluster_centers_indices_))
    print('Accuracy ', float(n_samples - cnt) / float(n_samples))
    print('Homogeneity ', metrics.homogeneity_score(target, clf.labels_))
    print('Completeness ', metrics.completeness_score(target, clf.labels_))

    # Plot resulting clusters.
    plt.figure(figsize = (8,8))
    plt.scatter(data[:,0], data[:,1], c = aff_y, s = 50)
    plt.title('Affinity clustering')
    plt.show()

def main():
    affinity_propagation()

if(__name__ == '__main__'):
    from sklearn import metrics
    from sklearn.cluster import AffinityPropagation
    from sklearn.datasets.samples_generator import make_blobs
    import matplotlib.pyplot as plt
    import numpy as np

    main()
