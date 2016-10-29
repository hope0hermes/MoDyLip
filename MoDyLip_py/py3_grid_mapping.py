# #!/usr/bin/python3
# #encoding-utf8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class GridMap():
    """
    Discretized mapping of a scalar quantity (average), 'y', over a 2D-surface,
    'X'.

    .. Attributes:

    :param domain: Input 2d surface along which the discretization will be
        evaluated
    :param target: Quantity to be averaged, 'y'
    :param map: 2D array with the local discretization of 'y
    :param points: Number of grid points along each tangential direction
    :param width: Slab's width along each tangential direction

    :type map: np.array((points[0], points[1]), dtype=float)
    :type points: [int]
    :type width: [float]

    """
    def __init__(self, domain, target, points=[32, 32]):
        """
        :param domain: Input 2d surface along which the discretization will be
            evaluated
        :param target: Quantity to be averaged
        :param points: Number of grid points along each tangential direction

        :type domain: ndarray([n_samples, 2], dtype=float)
        :type target: ndarrat([n_samples], dtype=float)
        :type points: [int]

        """
        assert domain.shape[0] == len(target), 'Unequal samples!!!'
        self.points = points
        self.start = None
        self.width = None
        self.map = None
        self._SetMapping(domain, target)

    def _SetMapping(self, domain, target):
        """
        Parses input domain and target and returns an initialized grid mapping.

        :param domain: Input 2d surface along which the discretization will be
            evaluated
        :param target: Quantity to be averaged

        :type domain: ndarray([n_samples, 2], dtype=float)
        :type target: ndarrat([n_samples], dtype=float)

        """
        # Gird dimensions and boundaries.
        self.start = domain.min(axis=0)
        self.width = (domain.max(axis=0) - self.start) / self.points
        # Evaluate mapping.
        counts = np.zeros((self.points[0]+1, self.points[1]+1), dtype=int)
        self.map = np.zeros((self.points[0]+1, self.points[1]+1), dtype=float)
        for sample in range(len(target)):
            i = int((domain[sample,0] - self.start[0]) / self.width[0])
            j = int((domain[sample,1] - self.start[1]) / self.width[1])
            counts[i,j] += 1
            self.map[i,j] += target[sample]
        # Normalize.
        for i in range(self.points[0] + 1):
            for j in range(self.points[1] + 1):
                if(counts[i,j] != 0): self.map[i,j] /= float(counts[i,j])

    def ClassifyPoint(self, point):
        """
        Determines if the point with tangential coordinates
        ('point[0], point[1]') and normal 'point[2]', lies above or below the
        local average normal.

        """
        # Find slab.
        i = int((point[0] - self.start[0]) / self.width[0])
        j = int((point[1] - self.start[1]) / self.width[1])
        if(point[2] >= self.map[i,j]):
            return 1
        else:
            return 0

    def Plot(self):
        """
        Density plot of the coarse-grained quantity.

        """
        x_min = self.start[0]
        y_min = self.start[1]
        x_max = self.start[0] + self.points[0]*self.width[0]
        y_max = self.start[1] + self.points[1]*self.width[1]
        plt.imshow(self.map[:-1, :-1], extent=(x_min, x_max, y_min, y_max),
            interpolation='bicubic', cmap='seismic')
        plt.colorbar()
        plt.show()
