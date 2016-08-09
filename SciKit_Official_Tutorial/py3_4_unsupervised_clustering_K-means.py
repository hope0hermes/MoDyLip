#!/usr/bin/python3
#encoding-utf8

def kMeans_normal():
    """
    The k-means algorithm clusters data by training to separate samples in k
    groups of equal variance, minimizing the 'inertia' or the within-cluster
    sum-of-squares.

    The algorithm basically follows 3 steps:

        - Chooses the k initial centroids from the dataset X and loop in the
          following way until centroids' position converges:

            - Assign each sample to its closer centroid.
            - Create new centroids by evaluating center of mass of all samples
              within the previously assigned centroid.

    Drawbacks of this algorithm are:

        - Although centroids' convergence is guaranteed, the final result is
          highly dependent on the initial state (the algorithm can converge to a
          local minima).
        - Inertia makes the assumption that clusters are convex and isotropic:
          poor response to elongated or irregular shapes.
    """
    # Setup number of samples and seed of random number generator.
    samples = 1500
    seed = 170

    # DIFFERENT BLOBS TO BE ANALYZED.
    # Gaussian.
    X, y = make_blobs(n_samples = samples, random_state = seed)
    # Anisotropic.
    trans_mat = [[ 0.60834549, -0.63667341], [-0.40887718, 0.85253229]]
    X_any = np.dot(X, trans_mat)
    # Inhomogeneous.
    X_in, _ = make_blobs(n_samples = samples, cluster_std = [1.0,2.5,0.5],
        random_state = seed)
    # Different size.
    X_size = np.vstack((X[y == 0][:500], X[y == 1][:100], X[y == 2][:10]))


    # SETUP THE DIFFERENT CLASSIFIERS.
    # Gaussian.
    y_2 = KMeans(n_clusters = 2, random_state = seed).fit_predict(X)
    # Anisotropic.
    y_any = KMeans(n_clusters = 3, random_state = seed).fit_predict(X_any)
    # Inhomogeneous.
    y_in = KMeans(n_clusters = 3, random_state = seed).fit_predict(X_in)
    # Different size.
    y_size = KMeans(n_clusters = 3, random_state = seed).fit_predict(X_size)

    # PLOT DIFFERENT ANALYSIS.
    plt.figure(figsize = (12, 12))
    # Wrong # of clusters.
    plt.subplot(221)
    plt.scatter(X[:,0], X[:,1], c = y_2)
    plt.title('Wrong number of clusters')
    # Anisotropic.
    plt.subplot(222)
    plt.scatter(X_any[:,0], X_any[:,1], c = y_any)
    plt.title('Anisotropic')
    # Inhomogeneous.
    plt.subplot(223)
    plt.scatter(X_in[:,0], X_in[:,1], c = y_in)
    plt.title('Inhomogeneous')
    # Different size.
    plt.subplot(224)
    plt.scatter(X_size[:,0], X_size[:,1], c = y_size)
    plt.title('Different size')
    plt.show()

def kMeans_miniBatches():
    """
    MiniBatchKMeans is a variant of k-mens that uses mini-batches to reduce the
    computing time, while still targeting the same objective function.

    The new algorithm iterates over two major steps:

        - b samples are drawn randomly from the dataset to
          form a minibatch. These are then assigned to the nearest centroid.
        - For each sample in the minibatch, the assigned centroid is updated by
          by taking the streaming average of the sample and all previous samples
          assigned to that centroid. This has the effect of decreasing the rate
          of change for a centroid over time.

    These steps are repeated until convergence or a predefined number of
    iteration steps is reached.
    """
    # SETUP DATASET TO BE ANALYZED.
    np.random.seed()
    seed = np.random.randint(100)
    batch_size = 45
    centers = [ [-1.,0], [0.,1.], [1.,0.] ]
    samples = 3000
    data, target = make_blobs(n_samples = samples, centers = centers,
        cluster_std = 0.4, random_state = seed)

    # ANAYSIS WITH STANDARD KMeans.
    km_clf = KMeans(n_clusters = 3,
        random_state = seed)
    t0 = time.time()
    km_y = km_clf.fit_predict(data)
    km_time = time.time() - t0
    km_labels = km_clf.labels_
    km_labels_unique = np.unique(km_labels)
    km_centers = km_clf.cluster_centers_

    # ANAYSIS WITH Batch KMeans.
    batch_clf = MiniBatchKMeans(n_clusters = 3, batch_size = batch_size,
        random_state = seed)
    t0 = time.time()
    batch_y = batch_clf.fit_predict(data)
    batch_time = time.time() - t0
    batch_labels = batch_clf.labels_
    batch_labels_unique = np.unique(batch_labels)
    batch_centers = batch_clf.cluster_centers_

    # RESULTS FROM BOTH METHODS.
    # Evaluation time.
    print(100*'\n')
    # Centroids.
    print('{:<10s} {:>10s} {:>10s} {:>10s} {:>10s}'.format(
        'Centroids', 'km_x', 'km_y', 'batch_x', 'batch_y'))
    for idx in range(3):
        print('{:<10d} {: >10.4f} {: >10.4f} {: >10.4f} {: >10.4f}'.format(idx,
            km_centers[idx][0], km_centers[idx][1],
            batch_centers[idx][0], batch_centers[idx][1]))
    print('\n{:<10s} {:>10s} {:>10s} {:>10s} {:>10s}'.format(
        '', '', 'KMeans', '', 'Batch'))
    print('\n{:<10s} {:>10s} {:>10.4f} {:>10s} {:>10.4f}'.format(
        'time', '', km_time, '', batch_time))

    miss = int(0)
    for idx in range(samples):
        if(km_labels[idx] != batch_labels[idx]): miss += 1
    print('\nThere were {:d} miss matches out of {:d} samples'.format(
        miss, samples))


    # Plot clusters from both methods.
    plt.figure(figsize = (6, 12))
    # Standard KMeans.
    plt.subplot(211)
    plt.scatter(data[:,0], data[:,1], c = km_y)
    plt.title('Standard KMeans')
    # Batch KMeans.
    plt.subplot(212)
    plt.scatter(data[:,0], data[:,1], c = batch_y)
    plt.title('Batch KMeans')

    plt.show()

def main():
    # kMeans_normal()
    kMeans_miniBatches()

if(__name__ == '__main__'):
    from sklearn.cluster import MiniBatchKMeans, KMeans
    from sklearn.datasets import make_blobs
    import time
    import numpy as np
    import matplotlib.pyplot as plt

    main ()
