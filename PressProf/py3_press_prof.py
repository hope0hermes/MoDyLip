#!/usr/bin/python3
#encoding-utf8
"""
Measurement of the pressure profile across planar bilayers.

This programs does statistics on the instantaneous realizations of the pressure
profile of planar bilayers.
"""


class PressProf():
    """
    Different components of the stress profile across a planar bilayer.

    The stress components are stored in a 2D, nested list of N rows and 7
    columns:

    ====== ====== ====== ====== ====== ====== ======
    height P_{xx} P_{yy} P_{zz} P_{xy} P_{xz} P_{yz}
    ====== ====== ====== ====== ====== ====== ======
    z_0    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
    z_1    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
     .        .      .      .      .      .      .
     .        .      .      .      .      .      .
     .        .      .      .      .      .      .
    z_N    ``%f`` ``%f`` ``%f`` ``%f`` ``%f`` ``%f``
    ====== ====== ====== ====== ====== ====== ======

    where {x,y,z} represent Cartesian coordinates and the numerical subindex
    stands for the profile discretization along the bilayer normal (which is
    assumed to point along the z-direction).
    """

    def __init__(self, prof=[], prof_err=[], mom_0=[0.]*7, mom_1=[0.]*7):
        """
        :param prof: Average value of the different stress profile components.
        :param prof_err: Standard deviation of the stress profile components.
        :param mom_0: 0th integral momentum of the stress profile components.
        :param mom_1: 1st integral momentum of the stress profile components.

        :type prof: [[]] (2D nested list)
        :type prof_std: [[]] (2D nested list)
        :type mom_0: [] (list)
        :type mom_1: [] (list)
        """

        self.prof = prof

def main():
    """
    Main sentinel for standalone and module usage.
    """

if __name__ == 'main':
    main()