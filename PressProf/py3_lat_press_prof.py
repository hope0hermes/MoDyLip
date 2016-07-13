#!/usr/bin/python
#encoding-utf8
import os
import math
"""
.. include:: reST_press_tens_defs.rst

"""


class LatPressProf():
    """
    **Lateral pressure profile**, |Prof|, across a planar bilayer.

    It is assumed that the bilayer normal lies along the |z|-axis, so that the
    definition of |Prof| reduces to:

    |Prof_def|,

    where |P_aa| are the diagonal components of the pressure tensor, |P_ab|,
    across the bilayer
    :math:`\\left(\\mathrm{with}\,\\alpha,\\beta \\in \\{x,y,z\\}\\right)`.

    The equilibrium properties of |Prof| are evaluated from its ensemble
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
    |slabs| **slabs** of **width** |slab_width|. Furthermore, it is assumed
    that, for each realization, the bilayer\'s midplane lies exactly at the
    middle of the simulation box, :math:`z = z_{N/2}`.

    The creation of **PressProf** objects requires passing **tens_file** as a
    unique argument::

        press_prof_object = PressProf(\'pressure_tensor_file.ext\')

    This returns an object containing the average pressure profile and its
    local standard deviations, |Prof_err|, stored in **prof** and **prof_err**,
    respectively.

    The integral momenta of |Prof| are evaluated upon request, by calling the
    method **get_momentum(**\ *int(n)*\ **)**. This returns an array of length
    **slabs**, whose *i-th* entry is the integral momentum of degree *n*,
    centered at :math:`z_{i}\\in[z_{0}, z_{N-1}]` and evaluated over the entire
    simulation box.

    .. Attributes:

    :param height: Discretization of the simulation box along the bilayer
        normal.
    :param prof: Lateral pressure profile across the bilayer: |Prof_def|.
    :param prof_err: Standard deviation of of the lateral pressure profile:
        |Prof_err|.
    :param samples: Number of instantaneous realization of the pressure-tensor
        in the input file.
    :param slabs: Number of slabs across the bilayer normal: |slabs|.
    :param slab_width: Width of the discretization slabs: |slab_width|.
    :type height: [float]
    :type prof: [float]
    :type prof_err: [float]
    :type samples: int
    :type slabs: int
    :type slab_width: float

    """
    def __init__(self, tens_file):
        """
        Initialization is only possible for a properly formated input file.

        :param _momenta: Accumulator of integral momenta arrays: the 1st call
            to **get_momentum()** with the integer argument *n* will be
            appended to the *i-th* entry of this accumulator. Subsequent calls
            to **get_momentum()** with the same argument, *n*, won't re-evaluate
            the integral momentum again, but will refer to the *i-th* entry of
            this accumulator.
        :param _momenta_index: Link to the array of integral momenta of degree
            *n* in the **_momenta** accumulator.
        :type _momenta: [[float]]
        :type _momenta_index: {int: int}

        """
        self.tens_file = self._check_tens_file(tens_file)
        self._momenta = []
        self._momenta_index = {}
        self.height = []
        self.prof = []
        self.prof_err = []
        self.samples = int(0)
        self.slabs = int(0)
        self.slab_width = float(0.)
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

    def get_momentum(self, grade):
        """
        Retrieves the requested integral momenta from **_momenta**.

        If the integral momenta of degree **grade** have not been computed,
        i.e., **grade** is not indexed in **_momenta_index**,
        **_index**\ =\ *-1* and **_Flag**\ =\ *False*, then the requested
        momenta are computed and appended to the momenta accumulator,
        **_momenta**.

        :param grade: Grade of the requested integral momenta.
        :param _index: Link to the array of integral momenta of degree
            **grade** in the _momenta accumulator.
        :param _FLAG: Boolean flag indicating if the requested integral
            momentum as to be computed.
        :type _index: int
        :type _FLAG: boolean
        :returns: Integral momenta of degree **grade** from the **_momenta**.
        :rtype: [float]

        """
        _index, _FLAG = self._get_momenta_index(grade)
        if(not _FLAG): self._evaluate_momentum(grade)
        return(self._momenta[_index])

    def _evaluate_momentum(self, grade):
        """
        Evaluates the integral momentum of degree **grade**.

        The *i-th* entry of the auxiliary array, **momenta**, stores the
        integral momenta of degree **grade**, centered at
        :math:`z_{i}\\in[z_{0}, z_{N-1}]` and evaluated over the entire
        simulation box. When all the centered momenta have been computed, they
        are appended to the instance accumulator **_momenta** and the
        corresponding tuple :math:`\\{index, grade\\}` is updated to
        **_momenta_index**.

        :param grade: Grade of the requested integral momentum.
        :param momenta: Array storing the integral momenta of degree *grade*,
            centered at :math:`z_{i}\\in\\{z_{N/2}, ..., z_{N-1}\\}`.
        :type grade: int
        :type momenta: [float]

        """
        momenta = []
        for i in range(self.slabs):
            suma = float(0.)
            for k in range(self.slabs):
                val = self.prof[k]*((self.height[k] - self.height[i])**grade)
                suma += val
            momenta.append(self.slab_width*suma)
        # Update momentum array and index dictionary.
        self._momenta_index[grade] = int(len(self._momenta))
        self._momenta.append(momenta)

    def _get_momenta_index(self, grade):
        """
        Index of the integral momenta of degree **grade** in **_momenta**.

        If **grade** is found in **_momenta_index**, then the corresponding
        **index** and a \'True\' **Flag** are returned. Otherwise
        **index**\ =\ *-1* and **Flag**\ =\ \'False\'.

        :param grade: Grade of the requested integral momentum.
        :param index: Index of the requested integral momentum in the _momenta
            array.
        :param FLAG: Flag indicating if the requested momentum was found.
        :type grade: int
        :type index: int
        :type FLAG: boolean
        :returns: index, FLAG
        :rtype: int, boolean

        """
        index = -1
        if(isinstance(grade, (int))):
            if(grade in self._momenta_index):
                index = self._momenta_index[grade]
                FLAG = True
            else:
                index = len(self._momenta)
                FLAG = False
        else:
            print('The argument of \'get_momentum()\' should be int')
            print('Aborting...\n')
            exit()
        return(index, FLAG)

    def _get_profile(self):
        """
        Evaluates the lateral density profile and its statistical error.

        Having the sum of linear and square lateral pressure profiles
        (**sum_lin** and **sum_sqr**, respectively) as well an estimation of its
        local mean values (**mean**), the average density profile (**prof**) and
        its unbiased standard deviation (**prof_err**) are computed.

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

        for slab in range(self.slabs):
            # Normalize pressure profile and statistical error.
            self.prof[slab] = mean[slab] + sum_lin[slab]/float(self.samples)
            self.prof_err[slab] = sum_sqr[slab]
            self.prof_err[slab] -= (sum_lin[slab]**2)/float(self.samples)
            self.prof_err[slab] /= float(self.samples - 1.)
            self.prof_err[slab] = math.sqrt(self.prof_err[slab])

    def _get_samples(self):
        """
        Read instantaneous realizations of the pressure profile from input file.

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

        mean, sum_lin, sum_sqr = self._get_1st_sample(tens_stream)
        # Approximation of the local mean from the 1st sample.
        for line in tens_stream:
            if(line == '\n'):
                # Check for new instantaneous profile realization.
                blanks += 1
                if(blanks == 2):
                    blanks = 0
                    self.samples += 1
                    print('Reading the lateral pressure profile from \'{:s}\''\
                        ': Sample {:d}\r'.format(self.tens_file, self.samples)),
            elif(not line.startswith('#')):
                line = line.split()
                prof = 0.5*(float(line[1]) + float(line[2])) - float(line[3])
                sum_lin[slab] += (prof - mean[slab])
                sum_sqr[slab] += (prof - mean[slab])**2
                slab += 1
                if(slab == self.slabs): slab = 0
        print('')
        tens_stream.close()
        return(mean, sum_lin, sum_sqr)

    def _get_1st_sample(self, tens_stream):
        """
        Get the 1st instantaneous realization of the pressure profile.

        Sets the number of **slabs** in the pressure profile and the
        discretization along the bilayer normal (**slab_width**). Also provides
        a 1st approximation of the local mean, which allows the evaluation of
        local variances in a single file-read, without round-off errors due to
        the floating-point arithmetic of large numbers. The local sum of linear
        and squared deviations from the approximated mean are also initialized.

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