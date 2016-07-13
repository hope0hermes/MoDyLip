#!/usr/bin/python
#encoding-utf8
import os
import math
"""
.. include:: reST_press_tens_defs.rst

"""

class PressTens():
    """
    **Pressure tensor**, |P_ab|, across a planar bilayer.

    It is assumed that the bilayer normal lies along the |z|-axis.

    The equilibrium properties of |P_ab| are evaluated from its ensemble
    average, over a set of realizations (**samples**), at different time steps.
    These realizations should be provided as an input data file, **tens_file**,
    with the following format:

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

    where the first column stores the homogeneous, spatial discretization of the
    simulation box along the bilayer normal, i.e., it consist of an array of
    |slabs| **slabs** of **width** |slab_width|, and where Greek sub-indexes,
    :math:`\mathrm{with}\,\\alpha,\\beta \\in \\{x,y,z\\}`, represent the
    corresponding components of the pressure tensor. Furthermore, it is assumed
    that, for each realization, the bilayer\'s midplane lies exactly at the
    middle of the simulation box, :math:`z = z_{N/2}`.

    where the first column stores the spatial discretization along the bilayer
    normal, consisting of |slabs| **slabs** of **width** |slab_width|.

    The creation of **TensProf** objects requires passing **tens_file** as a
    unique argument::

        tens_prof_object = TensProf(\'pressure_tensor_file.ext\')

    This returns an object containing the average pressure tensor and its
    local standard deviations, |P_ab_err|, stored in **tens** and **tens_err**,
    respectively.

    .. Attributes:

    :param height: Spatial discretization along the bilayer normal.
    :param tens: Pressure tensor across the bilayer: |P_ab|.
    :param tens_err: Standard deviation of of the pressure tensor: |P_ab_err|.
    :param samples: Number of instantaneous pressure-tensor samples in the input
        file.
    :param slabs: Number of slabs across the bilayer normal: |slabs|.
    :param slab_width: Width of the discretization slabs: |slab_width|.
    :param comps: Number of independent components in the pressure tensor.
    :type height: [float]
    :type tens: [[float]]
    :type tens_err: [[float]]
    :type samples: int
    :type slabs: int
    :type slab_width: float
    :type comps: int

    """
    def __init__(self, tens_file):
        """
        Initialization is only possible if the input file exists and has the

        expected format.
        """
        self.tens_file = self._check_tens_file(tens_file)
        self.height = []
        self.tens = []
        self.tens_err = []
        self.samples = int(0)
        self.slabs = int(0)
        self.slab_width = float(0.)
        self.comps = int(0)
        self._get_profile()

    def _check_tens_file(self, tens_file):
        """
        Verifies the existence and proper format of the input file.

        Returns the validated name of the input file in case it exist and has
        the expected format. On the contrary, the program is terminated with an
        error message.

        :param tens_file: Input file with the instantaneous realizations of the
            pressure tensor.
        :type tens_file: string
        :returns: tens_file
        :rtype: string

        """
        if(not os.path.isfile(tens_file)):
            print('Couldn\'t find the file \'{:s}\n'.format(tens_file))
            exit()
        else:
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
        return(tens_file)

    def _get_profile(self):
        """
        Evaluates the average pressure tensor and its statistical error.

        Having the sum of linear and square pressure tensor components (
        **sum_lin** and **sum_sqr**, respectively) as well as an estimation of
        its local mean values (**mean**), the average components of the pressure
        tensor (**tens**) and its unbiased standard deviation (**tens_err**) are
        computed.

        .. Attributes:

        :param mean: Guess of the local pressure profile mean.
        :param sum_lin: Sum of linear deviations from the guessed mean.
        :param sum_sqr: Sum of squared deviations from the guessed mean.
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]


        """
        mean, sum_lin, sum_sqr = self._get_samples()
        # Read realizations of the pressure profile from input file.

        for comp in range(self.comps):
            for slab in range(self.slabs):
                # Normalize pressure profile and statistical error.
                self.tens[comp][slab] = mean[comp][slab]\
                    + sum_lin[comp][slab]/float(self.samples)
                self.tens_err[comp][slab] = sum_sqr[comp][slab]
                self.tens_err[comp][slab] -= (sum_lin[comp][slab]**2)\
                    /float(self.samples)
                self.tens_err[comp][slab] /= float(self.samples - 1.)
                self.tens_err[comp][slab] = math.sqrt(self.tens_err[comp][slab])

    def _get_samples(self):
        """
        Read instantaneous realizations of the pressure tensor from input file.

        Set the number of **samples** to be analyzed. Also sets the local sums
        linear and squared deviations from a tentative mean (obtained from the
        1st profile sample), which are needed for the evaluation of the local
        averages and standard deviations.

        .. Attributes:

        :param mean: Guess of the local mean values.
        :param sum_lin: Sum of linear deviations from the guessed mean.
        :param sum_sqr: Sum of squared deviations from the guessed mean.
        :param tens_stream: Stream to the input data file.
        :param blanks: Consecutive blank lines in the input stream. Two blanks
            separate individual profile realizations.
        :param slab: Location index across the bilayer discretization.
        :param comps: Number of independent components in the pressure tensor.
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]
        :type tens_stream: text_stream
        :type blanks: int
        :type slab: int
        :type comps: int
        :returns: mean, sum_lin, sum_sqr
        :rtype: [float], [float], [float]

        """
        tens_stream = open(self.tens_file, "r", buffering=1)
        blanks = 0
        slab = 0

        mean, sum_lin, sum_sqr = self._get_1st_sample(tens_stream)
        # Approximation of the local mean from the 1st sample.

        for line in tens_stream:
            if(line == '\n'):
                # Check for new instantaneous profile realization.
                blanks += 1
                if(blanks == 2):
                    blanks = 0
                    self.samples += 1
                    print('Reading the pressure tensor from \'{:s}\''\
                        ': Sample {:d}\r'.format(self.tens_file, self.samples)),
            elif(not line.startswith('#')):
                line = line.split()
                for comp in range(self.comps):
                    prop = float(line[comp+1])
                    #print('(comp, slab) -> ({:d}, {:d})'.format(comp, slab))
                    sum_lin[comp][slab] += prop - mean[comp][slab]
                    sum_sqr[comp][slab] += (prop - mean[comp][slab])**2
                slab += 1
                if(slab == self.slabs): slab = 0
        print('')
        tens_stream.close()
        return(mean, sum_lin, sum_sqr)

    def _get_1st_sample(self, tens_stream):
        """
        Get the 1st instantaneous realization of the pressure tensor.

        Sets the number of **slabs** in the pressure tensor and the
        discretization along the bilayer normal (**slab_width**). Also provides
        a 1st approximation of the local mean, which allows the evaluation of
        local variances in a single file-read, without round-off errors due to
        the floating-point arithmetic of large numbers. The local sum of linear
        and squared deviations from the approximated mean are also initialized.

        Finally, the input stream to the input data file is re-winded before
        termination.

        .. Attributes:

        .. Attributes:

        :param tens_stream: Stream to the input data file.
        :param mean: Guess of the local mean values.
        :param sum_lin: Zeroed sum of linear deviations from the guessed mean.
        :param sum_sqr: Zeroed sum of squared deviations from the guessed mean.
        :param blanks: Consecutive blank lines in the input stream. Two blanks
            separate individual profile realizations.
        :param comps: Number of independent components in the pressure tensor.
        :type tens_stream: text_stream
        :type mean: [float]
        :type sum_lin: [float]
        :type sum_sqr: [float]
        :type blanks: int
        :type comps: int
        :returns: mean, sum_lin, sum_sqr
        :rtype: [float], [float], [float]

        """
        mean = []
        sum_lin = []
        sum_sqr = []
        blanks = 0
        FLAG = True
        for line in tens_stream:
            if(line == '\n'):
                blanks += 1
                if(blanks == 2): break
            elif(not line.startswith('#')):
                line = line.split()
                self.slabs += 1
                if(FLAG):
                    self.comps = int(len(line)-1)
                    FLAG = False
                    self.height.append(float(line[0]))
                    for comp in range(self.comps):
                        self.tens.append([])
                        self.tens_err.append([])
                        mean.append([])
                        sum_lin.append([])
                        sum_sqr.append([])

                        self.tens[comp].append(float(0.))
                        self.tens_err[comp].append(float(0.))
                        mean[comp].append(float(line[comp+1]))
                        sum_lin[comp].append(float(0.))
                        sum_sqr[comp].append(float(0.))
                else:
                    self.height.append(float(line[0]))
                    for comp in range(self.comps):
                        self.tens[comp].append(float(0.))
                        self.tens_err[comp].append(float(0.))
                        mean[comp].append(float(line[comp+1]))
                        sum_lin[comp].append(float(0.))
                        sum_sqr[comp].append(float(0.))
        tens_stream.seek(0)
        self.slab_width = self.height[1] - self.height[0]
        return(mean, sum_lin, sum_sqr)