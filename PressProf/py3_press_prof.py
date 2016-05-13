#!/usr/bin/python
#encoding-utf8
"""


Measurement of the pressure profile across a planar bilayer.

This programs does statistics on the instantaneous realizations of the pressure
profile of planar bilayers. The program assumes that the **bilayer normal**
points in the **z-direction**.

.. |x| replace:: :math:`x`
.. |y| replace:: :math:`y`
.. |z| replace:: :math:`z`
.. |h| replace:: :math:`h`
.. |region| replace:: :math:`\\left[-h/2, h/2\\right]`
.. |z_0| replace:: :math:`z_{0}`
.. |z_1| replace:: :math:`z_{1}`
.. |z_i| replace:: :math:`z_{i}`
.. |z_N-1| replace:: :math:`z_{N-1}`
.. |slabs| replace:: :math:`N`
.. |slab_width| replace:: :math:`\\Delta z`
.. |Prof| replace:: :math:`\\Gamma(z)`
.. |Prof_def| replace::
    :math:`\Gamma(z) = P_{zz}(z) - \left[P_{xx}(z) + P_{yy}(z)\\right] / 2`
.. |Prof_err| replace:: :math:`\\sigma_{\\Gamma}(z)`
.. |mom_n| replace:: :math:`\\mu_{n}(z_{i})`
.. |mom_n_def_int| replace::
    :math:`\\mu_{n}(z_{i}) = \\int_{z_{i}}^{h/2}\\mathrm{d}z\\Gamma(z)z^{n}`
.. |mom_n_def| replace::
    :math:`\\mu_{n}(z_{i}) = \\Delta z\\sum_{k=z_{N/2+i}}^{N-1}\
        (z_{k}-z_{N/2+i})^{n}\\Gamma(z_{k})`
.. |P_aa| replace:: :math:`P_{\\alpha\\alpha}(z)`
.. |P_ab| replace:: :math:`P_{\\alpha\\beta}(z)`
.. |P_xx| replace:: :math:`P_{xx}(z)`
.. |P_yy| replace:: :math:`P_{yy}(z)`
.. |P_zz| replace:: :math:`P_{zz}(z)`
.. |P_xy| replace:: :math:`P_{xy}(z)`
.. |P_xz| replace:: :math:`P_{xz}(z)`
.. |P_yz| replace:: :math:`P_{yz}(z)`

"""

class CheckPressTensFile():
    """
    Pressure-tensor file properties.

    Verifies the existence and proper format of the provided input file.

    .. Attributes:

    :param tens_file: Pressure-tensor file.
    :type tens_file: string

    """

    def __init__(self, tens_file=''):
        self.tens_file = tens_file
        if(isinstance(tens_file, (list, tuple))):
            for x in self.tens_file:
                self.__check_existence(x)
                self.__check_format(x)
        else:
            self.__check_existence(tens_file)
            self.__check_format(tens_file)

    def __check_existence(self, tens_file):
        """
        Verifies the existence of the input file.

        """
        if(not os.path.isfile(tens_file)):
            print('Couldn\'t find the file \'{:s}\'\nAborting!!!\n'.format(
                tens_file))
            exit()

    def __check_format(self, tens_file):
        """
        Check that the input file has the  required format.

        """
        tens_stream = open(tens_file, "r", buffering=1)
        for line in tens_stream:
            if(not line.startswith('#')):
                line = line.split()
                break
        tens_stream.close()
        # Verify there are 7 columns.
        if(len(line) != 7):
            print('File \'{:s}\' does not have the required format (check '\
                'source documentation)'.format(tens_file))
            exit()

class PressProf(CheckPressTensFile):
    """
    **Pressure profile**, |Prof|, across a planar bilayer.

    It is assumed that the bilayer normal points along the |z| direction and
    that its normal cross-section spans the region |region|. Under these
    assumptions, the definition of |Prof| reduces to:

    |Prof_def|,

    where |P_aa| are the diagonal components of the pressure tensor, |P_ab|,
    across the bilayer
    :math:`\\left(\\mathrm{with}\,\\alpha,\\beta \\in \\{x,y,z\\}\\right)`.

    The equilibrium properties of |Prof| are evaluated from the input file
    **tens_file**, which stores the set of realizations (**samples**) of |P_ab|
    at different time steps. This file should have the following format:

    +---------+--------+--------+--------+--------+--------+--------+
    | height  | |P_xx| | |P_yy| | |P_zz| | |P_xy| | |P_xz| | |P_yz| |
    +=========+========+========+========+========+========+========+
    | ``#`` ``Commented or labeled lines must start with`` ```#```  |
    +---------+--------+--------+--------+--------+--------+--------+
    | |z_0|   | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` |
    +---------+--------+--------+--------+--------+--------+--------+
    | |z_1|   | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` |
    +---------+--------+--------+--------+--------+--------+--------+
    |    .    |   .    |   .    |   .    |   .    |   .    |   .    |
    +---------+--------+--------+--------+--------+--------+--------+
    |    .    |   .    |   .    |   .    |   .    |   .    |   .    |
    +---------+--------+--------+--------+--------+--------+--------+
    |    .    |   .    |   .    |   .    |   .    |   .    |   .    |
    +---------+--------+--------+--------+--------+--------+--------+
    | |z_N-1| | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` | ``%f`` |
    +---------+--------+--------+--------+--------+--------+--------+
    | ``#`` ``Every sample terminates with two blank lines``        |
    +---------+--------+--------+--------+--------+--------+--------+
    | ``\\n``                                                        |
    +---------+--------+--------+--------+--------+--------+--------+
    | ``\\n``                                                        |
    +---------+--------+--------+--------+--------+--------+--------+

    where the first column stores the spatial discretization along the bilayer
    normal, consisting of |slabs| **slabs** of **width** |slab_width|.

    The creation of **PressProf** objects requires passing **tens_file** as a
    unique argument::

        press_prof_object = PressProf(\'pressure_tensor_file.ext\')

    This returns an object containing the average pressure profile (evaluated
    over all the samples) and its corresponding local standard deviations,
    |Prof_err|. These two quantities are stored in **prof** and **prof_err**,
    respectively.

    The *n-th* integral momenta of |Prof|, defined as

    |mom_n_def|,

    is evaluated upon request, by calling the method
    **get_momentum(**\ *int(n)*\ **)** (notice that this returns an array with
    only **slabs / 2** entries).

    .. Attributes:

    :param moms: List of integral momenta arrays.
    :param __moms_index: Dictionary to get the index of the requested integral
        momentum from the array moms.
    :param height: Spatial discretization along the bilayer normal.
    :param prof: Pressure profile across the bilayer: |Prof_def|.
    :param prof_err: Standard deviation of of the pressure profile: |Prof_err|.
    :param samples: Number of instantaneous pressure-tensor measurements in the
        input file.
    :param slabs: Number of slabs across the bilayer normal: |slabs|.
    :param slab_width: Width of the discretization slabs: |slab_width|.
    :type moms: [[float]]
    :type __moms_index: {int: int}
    :type height: [float]
    :type prof: [float]
    :type prof_err: [float]
    :type samples: int
    :type slabs: int
    :type slab_width: float

    """
    def __init__(self, tens_file):
        """
        Initialization is only possible if the input file exists and has the

        expected format.
        """
        self.moms = []
        self.__moms_index = {}
        self.height = []
        self.prof = []
        self.prof_err = []
        self.samples = int(0)
        self.slabs = int(0)
        self.slab_width = float(0.)
        CheckPressTensFile.__init__(self, tens_file)
        self.__get_profile()

    def get_momentum(self, grade):
        """
        Retrieval of integral momenta.


        """
        __index, __FLAG = self.__get_moms_index(grade)
        if(not __FLAG): self.__evaluate_momentum(grade)
        return(self.height[int(self.slabs/2):], self.moms[__index])

    def __evaluate_momentum(self, grade):
        """
        Evaluates the requested integral momentum and appends it to moms array.

        """
        half = int(self.slabs/2)
        mom = []
        for i in range(self.slabs - half):
            val = float(0.)
            for k in range(half + i, self.slabs):
                val += self.prof[k]*(self.height[k]-self.height[half+i])**grade
            mom.append(self.slab_width*val)
        # Update momentum array and index dictionary.
        self.__moms_index[grade] = int(len(self.moms))
        self.moms.append(mom)

    def __get_moms_index(self, grade):
        """
        Return the index of the requested integral momentum in the moms array.

        If the requested momentum is not indexed (has not been evaluated),
        self.__moms_index is updated and a \'False\' flag is returned.

        :param index: Index of the requested integral momentum in the moms
            array.
        :param FLAG: Flag indicating if the requested momentum was found.
        :type index: int
        :type FLAG: boolean
        :returns: index, FLAG
        :rtype: int, boolean

        """
        if(isinstance(grade, (int))):
            if(grade in self.__moms_index):
                index = self.__moms_index[grade]
                FLAG = True
            else:
                index = len(self.moms)
                FLAG = False
        else:
            print('The argument of \'get_momentum()\' should be int')
            print('Aborting...\n')
            exit()
        return(index, FLAG)

    def __get_profile(self):
        """
        Evaluates the density profile and its statistical error.

        Also sets the total number of instantaneous realizations in the input
        file and their spatial discretization.

        .. Attributes:

        :param mean: Guess of the local pressure profile mean.
        :param sum_lin: Sum of linear deviations from the guessed mean.
        :param sum_sqr: Sum of squared deviations from the guessed mean.
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]


        """
        mean, sum_lin, sum_sqr = self.__get_samples()
        # Read realizations of the pressure profile from input file.

        for slab in range(self.slabs):
            # Normalize pressure profile and statistical error.
            self.prof[slab] = mean[slab] + sum_lin[slab]/float(self.samples)
            self.prof_err[slab] = sum_sqr[slab]
            self.prof_err[slab] -= (sum_lin[slab]**2)/float(self.samples)
            self.prof_err[slab] /= float(self.samples - 1.)
            self.prof_err[slab] = math.sqrt(self.prof_err[slab])

    def __get_samples(self):
        """
        Read instantaneous realizations of the pressure profile from input file.

        Set the number of samples to be analyzed and their spatial
        discretization across the bilayer normal (slabs and slab_width).
        Also sets the local sums linear and squared deviations from a
        tentative mean (obtained from the 1st profile sample), which are needed
        for the evaluation of the local averages and standard deviations.

        .. Attributes:

        :param mean: Guess of the local mean values.
        :param sum_lin: Sum of linear deviations from the guessed mean.
        :param sum_sqr: Sum of squared deviations from the guessed mean.
        :param tens_stream: Stream to the input data file.
        :param blanks: Consecutive blank lines in the input stream. Two blanks
            separate individual profile realizations.
        :param slab: Location index across the bilayer discretization.
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]
        :type tens_stream: text_stream
        :type blanks: int
        :type slab: int
        :returns: mean, sum_lin, sum_sqr
        :rtype: [float], [float], [float]

        """
        tens_stream = open(self.tens_file, "r", buffering=1)
        blanks = 0
        slab = 0

        mean, sum_lin, sum_sqr = self.__get_1st_sample(tens_stream)
        # Approximation of the local mean from the 1st sample.

        for line in tens_stream:
            if(line == '\n'):
                # Check for new instantaneous profile realization.
                blanks += 1
                if(blanks == 2):
                    blanks = 0
                    self.samples += 1
            elif(not line.startswith('#')):
                line = line.split()
                prof = float(line[3]) - 0.5*(float(line[1]) + float(line[2]))
                sum_lin[slab] += prof - mean[slab]
                sum_sqr[slab] += (prof - mean[slab])**2
                slab += 1
                if(slab == self.slabs): slab = 0
        tens_stream.close()
        return(mean, sum_lin, sum_sqr)

    def __get_1st_sample(self, tens_stream):
        """
        Get the 1st instantaneous realization of the pressure profile.

        Sets the number of slabs in the pressure profile and the discretization
        along the bilayer normal. It also provides a 1st approximation of the
        local mean, which allows the evaluation of local variances in a single
        file-read, without round-off errors due to the floating-point arithmetic
        of large numbers. The local sum of linear and squared deviations from
        the approximated mean are also initialized.

        Finally, the input stream to the input data file is re-winded before
        termination.

        .. Attributes:

        :param tens_stream: Stream to the input data file.
        :param mean: Guess of the local mean values.
        :param sum_lin: Zeroed sum of linear deviations from the guessed mean.
        :param sum_sqr: Zeroed sum of squared deviations from the guessed mean.
        :param blanks: Consecutive blank lines in the input stream. Two blanks
            separate individual profile realizations.
        :type tens_stream: text_stream
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]
        :type blanks: int
        :returns: mean, sum_lin, sum_sqr
        :rtype: [float], [float], [float]

        """
        mean = []
        sum_lin = []
        sum_sqr = []
        blanks = 0
        for line in tens_stream:
            if(line == '\n'):
                blanks += 1
                if(blanks == 2): break
            elif(not line.startswith('#')):
                line = line.split()
                self.height.append(float(line[0]))
                self.prof.append(float(0.))
                self.prof_err.append(float(0.))
                self.slabs += 1
                prof = float(line[3]) - 0.5*(float(line[1]) + float(line[2]))
                mean.append(prof)
                sum_lin.append(float(0.))
                sum_sqr.append(float(0.))
        tens_stream.seek(0)
        self.slab_width = self.height[1] - self.height[0]
        return(mean, sum_lin, sum_sqr)

class PressTens():
    """
    **Pressure tensor** across the bilayer.

    The pressure tensor is stored in a 2D, nested list of N-1 rows and 6
    columns:

    ====== ====== ====== ====== ====== ======
    |P_xx| |P_yy| |P_zz| |P_xy| |P_xz| |P_yz|
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

def main():
    """
    Main sentinel for standalone and module usage.

    """
    run_prof = []
    CheckPressTensFile(argv[1:])
    for x in argv[1:]:
        prof = PressProf(x)
        prof.get_momentum(2)
        run_prof.append(prof)

        """plt.figure(1)
        plt.subplot(211)
        upper = []
        lower = []
        for slab in range(prof.slabs):
            upper.append(prof.prof[slab] + prof.prof_err[slab])
            lower.append(prof.prof[slab] - prof.prof_err[slab])
        plt.plot(prof.height, prof.prof, prof.height, upper, prof.height, lower)
        plt.subplot(212)
        plt.plot(prof.height, prof.prof_err)
        plt.show()"""

    x, y = run_prof[0].get_momentum(5)
    plt.figure(1)
    plt.subplot(111)
    plt.plot(x, y)
    plt.show()

if __name__ == '__main__':
    from sys import argv
    import matplotlib.pyplot as plt
    import numpy as np
    import math
    import os
    import io
    main()