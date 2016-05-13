#!/usr/bin/python
#encoding-utf8
"""


Measurement of the pressure profile across planar bilayers.

This programs does statistics on the instantaneous realizations of the pressure
profile of planar bilayers. The program assumes that the **bilayer normal**
points in the **z-direction**.


"""

class PressProf():
    """
    **Pressure profile** and its integral momenta across a planar bilayer.

    These quantities are independently stored as the 1D lists:

    :param height: Spatial discretization along the bilayer normal.
    :param prof: Pressure profile across the bilayer:
        :math:`\Gamma(z) = P_{zz}(z) - \left[P_{xx}(z) + P_{yy}(z)\\right] / 2`.

    :param prof_err: Standard deviation of the pressure profile across the
        bilayer.
    :param mom0: 0th integral momenta across the bilayer:
        :math:`\\int\\mathrm{d}z\\Gamma(z)`.
    :param mom1: 1st integral momenta across the bilayer:
        :math:`\\int\\mathrm{d}z\\Gamma(z)z`.

    **mom0[i]** and **mom1[i]** store the corresponding integral momenta
    evaluated on the interval **[z_{i}, z_{N-1}]**.
    :type height: [float]
    :type prof: [float]
    :type prof_err: [float]
    :type mom0: [float]
    :type mom1: [float]

    """
    def __init__(self, height=[], prof=[], prof_err=[], mom0=[], mom1=[]):
        self.height = height
        self.prof = prof
        self.prof_err = prof_err
        self.mom0 = mom0
        self.mom1 = mom1

class PressTens():
    """
    **Pressure tensor** across the bilayer.

    The pressure tensor is stored in a 2D, nested list of N-1 rows and 6
    columns:

    ====== ====== ====== ====== ====== ======
    P_{xx} P_{yy} P_{zz} P_{xy} P_{xz} P_{yz}
    ====== ====== ====== ====== ====== ======
    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
      .      .      .      .      .      .
      .      .      .      .      .      .
      .      .      .      .      .      .
    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
    ====== ====== ====== ====== ====== ======

    where columns represent the different Cartesian components of the pressure
    tensor and rows stand for the spatial discretization along the bilayer
    normal (which is assumed to point along the z-direction). A similar data
    structure stores the local standard deviation of each tensor component.

    :param tens: Average value of the different pressure tensor components.
    :param tens_err: Standard deviation of the pressure tensor components.
    :param height: Spatial discretization along the bilayer normal (z-axis).
    :type tens: [[float]]
    :type tens_err: [[float]]
    :type height: [float]

    """
    def __init__(self, tens=[], tens_err=[], height=[]):
        self.tens = tens
        self.tens_err = tens_err
        self.height = height

class GetPress():
    """
    **Data acquisition** and setup of PressTens and PressProf structures for

    each input file.

    :param run_tens: List storing the pressure tensor data structures of all
        the input files.
    :param run_prof: List storing the pressure profile data structures of all
        the input files.
    :param in_files: List of density-profile files to be analyzed.
    :type run_tens: [PressTens]
    :type run_prof: [PressProf]
    :type in_files: [string]

    """
    def __init__(self, in_files):
        """
        Initialization only if all provided files exist.

        """
        for x in in_files:
            if(not os.path.isfile(x)):
                print('{:s} is not a file\n'.format(x))
                exit()
        self.run_tens = []
        self.run_prof = []
        self.in_files = in_files

def main():
    """
    Main sentinel for standalone and module usage.

    """
    ctrl = GetPress(argv[1:])
    for x in ctrl.in_files: print(x)

if __name__ == '__main__':
    from sys import argv
    import os
    main()