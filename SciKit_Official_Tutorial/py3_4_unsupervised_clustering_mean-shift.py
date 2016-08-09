#!/usr/bin/python3
#encoding-utf8

def mean_shift():
    """
    MeanShift discovers blobs in a smooth density of samples. It is a centroid
    algorithm which works by updating candidates for centroids to be the mean
    of the positions within a given region. These candidates are then filtered
    in a post-processing stage to eliminate near-duplicates and form the final
    list of centroids.
    """
    # Set a generic data sample.
    centers = [ [-1.,0.], [0.,1.], [1.,0.] ]
    n_samples = 3000
    std = 0.5
    seed = 0
    data, target = make_blobs(n_samples = n_samples, centers = centers,
        random_state = seed, cluster_std = std)

    # Set bandwidth for the mean shift classifier.
    width = estimate_bandwidth(data, quantile = 0.2,
        n_samples = int(n_samples / 5))
    # Setup the classifier.
    clf = MeanShift(bandwidth = width, bin_seeding = True)
    ms_y = clf.fit_predict(data)

    # Evaluate accuracy.
    cnt = int(0)
    for idx in range(n_samples):
        if(ms_y[idx] != clf.labels_[idx]): cnt += 1
    acc = float(cnt) / float(n_samples)

    # Print results.
    print('Approximated number of centroids ', len(clf.cluster_centers_))
    print('Accuracy ', acc)

    # Plot clusters.
    plt.figure(figsize = (8,8))
    plt.scatter(data[:,0], data[:,1], c = ms_y, s = 30)
    plt.title('Clusters found with the Mean-shift method')
    plt.show()

def main():
    mean_shift()

if(__name__ == '__main__'):
    from sklearn.cluster import MeanShift, estimate_bandwidth
    from sklearn.datasets.samples_generator import make_blobs
    import numpy as np
    import matplotlib.pyplot as plt

    main()
