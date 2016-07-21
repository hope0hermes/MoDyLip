#!/usr/bin/python3
#encoding-utf8

class Mean_Shift:
    """
    Mean shift algorithm for clustering.
    """
    def __init__(self, rad = float(4)):
        self.rad = rad

    def fit(self, data):
        """
        Trains the machine with the provided set of data points.
        """
        # Cluster centroids.
        centroids = {}
        # Originaly all data points are considered as centroids.
        for idx, point in enumerate(data):
            centroids[idx] = point
        # Iterate until all possible clusters have been found.
        cnt = 0
        while(True):
            new_cent = []
            # For every centroid, find all data points that are within its
            # working radius.
            for idx, cent in centroids.items():
                within_rad = []
                for point in data:
                    if(np.linalg.norm(point - cent) < self.rad):
                        within_rad.append(point)
                # Get center of mass of all points within the working radius of
                # current centroid.
                cm = np.average(within_rad, axis = 0)
                print('(iteration, index), old_centroid, new_centroid -> '\
                '({:d}, {:d}), ({:0.3f}, {:0.3f}),  ({:0.3f}, {:0.3f})'.format(
                    cnt, idx, cent[0], cent[1], cm[0], cm[1]))
                new_cent.append(tuple(cm))
            cnt += 1
            # Many centroids will converge to the same point during the
            # optimization proces. Filter repeated points and keep track of
            # immedidte previous centroids to set the convergence criteria.
            old_cent = dict(centroids)
            unique = sorted(list(set(new_cent)))
            centroids = {}
            for idx, cent in enumerate(unique):
                centroids[idx] = np.array(cent)
            # Stop once that the old and current centriods are the same.
            check = False
            for idx in centroids:
                if(np.linalg.norm(centroids[idx] - old_cent[idx]) < 1.e-5):
                    check = True
                else:
                    check = False
            if(check):
                break
        self.centroids = centroids

def main():
    # Original data set.
    X = np.array([ [1,2],[1.5,1.8],[5,8],[8,8],[1,.6],[9,11],[8,2],[10,2],
                   [2,1],[1.8,1.5],[8,5],[8,8],[.6,1],[11,9],[2,8],[2,10]])
    clf = Mean_Shift(rad = 1)
    clf.fit(X)
    centroids = clf.centroids
    plt.scatter(X[:,0], X[:,1], s=150)
    for c in centroids:
        plt.scatter(centroids[c][0], centroids[c][1], color='k', marker='*', s=150)
    plt.show()

if(__name__ == '__main__'):
    import numpy as np
    import matplotlib as mlp
    import matplotlib.pyplot as plt

    main()
