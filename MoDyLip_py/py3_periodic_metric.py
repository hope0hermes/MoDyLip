# #!/usr/bin/python3
# #encoding-utf8

import numpy as np

class PeriodicMetric():
    """

    """
    def __init__(self, box):
        self.halfBox = 0.5*box
        self.dim = int(len(box))

    def Distance(self, x, y):
        dist = 0.
        for idx in range(self.dim):
            temp = (y[idx] - x[idx])
            if(temp > self.halfBox[idx]):
                dist += (temp - 2.*self.halfBox[idx])**2
            else:
                dist += (temp)**2
        # Normalize.
        return(np.sqrt(dist))



