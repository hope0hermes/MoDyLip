#!/usr/bin/python3
#encoding-utf8

import numpy as np
import os

class Configuration():
    """
    Parses an input configuration file and returns an object with the complete
    information of the system at a particular time.

    The input file should comprise two parts:

    - A header, with the status of the simulation control parameters.
    - A body, with the position, velocity and type of each particle.

    This information must be provided in the following format (pay particular
    attention to the header spacing!!!)::

            # L=%f %f %f t=%f blocks=%d
            # v=%f ...  w=%f ...
            # a2=%f a3=%f Re=%f N=%d ks=%f kb=%f l0=%f
            # n=%d N=%d name=%s
            # r_x r_y r_z v_x v_y v_z type   <- This line can be omitted
              %f  %f  %f  %f  %f  %f  %d
              %f  %f  %f  %f  %f  %f  %d
              %f  %f  %f  %f  %f  %f  %d
               .   .   .   .   .   .   .
               .   .   .   .   .   .   .
               .   .   .   .   .   .   .
              %f  %f  %f  %f  %f  %f  %d
              %f  %f  %f  %f  %f  %f  %d
              %f  %f  %f  %f  %f  %f  %d

    .. Attributes:

    :param box: Lateral dimensions of the simulation box along the X, Y and Z
        directions: ``L``
    :param sim_time: Simulation time step: ``t``
    :param vir2: 2nd order virial coefficients: ``v``
    :param vir3: 3rd order virial coefficients: ``w``
    :param cutoff2: Cutoff radius for the 2nd order weighting densities: ``a2``
    :param cutoff3: Cutoff radius for the 3rd order weighting densities: ``a3``
    :param Re: End-to-end distance of a single lipid
    :param ks: Spring constant for the harmonic potential
    :param l0: Rest length for the harmonic potential
    :param kb: Strength of the bond-angle bending potential
    :param n_chains: Number of lipids in the system: ``n``
    :param ch_len: Number of beads per lipid: ``N``

    :type box: [float]
    :type sim_time: float
    :type vir2: [float]
    :type vir3: [float]
    :type cutoff2: float
    :type cutoff3: float
    :type Re: float
    :type ks: float
    :type l0: float
    :type kb: float
    :type n_chains: int
    :type ch_len: int

    """
    def __init__(self, in_file=''):
        assert os.path.isfile(in_file), 'Can\'t open ' + in_file
        stream = open(in_file, "r", buffering=1)
        self.in_file = in_file
        # Read control parameters.
        self._ParseHeader(stream)
        print(self.time)
        print(self.box)
        print(self.vir2)
        print(self.vir3)
        print(self.cutoff2)
        print(self.cutoff3)
        print(self.Re)
        print(self.ks)
        print(self.kb)
        print(self.l0)
        print(self.ch_len)
        print(self.n_chains)
        # Read configuration.
        _ParseBody(stream)

        # Close file.
        stream.close()

    def _ParseBody(self, stream):
        """
        Read particles' position, velocity and type.

        """
        self.cfg = np.array([self.n_beads, 7], dtype=np.float)
        count =


    def _ParseHeader(self, stream):
        """
        Read simulation control parameters and set the total number of beads.

        """
        base_msn = 'Header of \'{:s}\': '.format(self.in_file)
        # Read header of the configuration file.
        for line in stream:
            if(line.startswith('# L=')):
                # Simulation time.
                line = line.strip('# L=')
                line, sep, tail = line.partition(' t=')
                self.time = float(tail.split()[0])
                assert self.time >= 0., base_msn + 't < 0.'
                # Simulation box.
                self.box = np.array([float(x) for x in line.split()])
                assert len(self.box) == 3, base_msn + 'L != %f %f %f'
                for idx, x in enumerate(self.box):
                    assert x > 0, base_msn + 'L[%d] <= 0' % idx
            elif(line.startswith('# v=')):
                line = line.strip('# v=')
                line, sep, tail = line.partition(' w=')
                # 2nd and 3rd order virial coefficients.
                self.vir2 = np.array([float(x) for x in line.split()])
                self.vir3 = np.array([float(x) for x in tail.split()])
                assert len(self.vir2) > 0, base_msn + 'v= in empty'
                assert len(self.vir3) > 0, base_msn + 'w= in empty'
            elif(line.startswith('# a2=')):
                # Rest length of the harmonic potential.
                line, sep, tail = line.partition(' l0=')
                self.l0 = float(tail)
                assert self.l0 >= 0., base_msn + 'l0 < 0.'
                # Force constant for the angular potential.
                line, sep, tail = line.partition(' kb=')
                self.kb = float(tail)
                assert self.kb >= 0., base_msn + 'kb < 0.'
                # Force constant for the harmonic potential.
                line, sep, tail = line.partition(' ks=')
                self.ks = float(tail)
                assert self.ks >= 0., base_msn + 'ks < 0.'
                # Chain length.
                line, sep, tail = line.partition(' N=')
                self.ch_len = int(tail)
                assert self.ch_len > 0, base_msn + 'N <= 0'
                # End-to-end distance.
                line, sep, tail = line.partition(' Re=')
                self.Re = float(tail)
                assert self.Re > 0., base_msn + 'Re <= 0.'
                # Cutoff radius for 3rd order weighting functions.
                line, sep, tail = line.partition(' a3=')
                self.cutoff3 = float(tail)
                assert self.cutoff3 > 0., base_msn + 'a3 <= 0.'
                # Cutoff radius for 2nd order weighting functions.
                line, sep, tail = line.partition(' a2=')
                self.cutoff2 = float(tail)
                assert self.cutoff2 > 0., base_msn + 'a2 <= 0.'
                assert self.cutoff3 > self.cutoff2, base_msn + 'a3 < a2'
            elif(line.startswith('# n=')):
                # Number of chains and beads.
                line = line.strip('# n=')
                line, sep, tail = line.partition(' N=')
                self.n_chains = int(line)
                assert self.n_chains >= 0., base_msn + 'n < 1.'
                self.n_beads = sefl.n_chains * self.ch_len
            else:
                break

def main():
    """
    Pero mira que programita.

    """
    cfg = Configuration('configuration_00000000.cfg')
    #cfg = Configuration()


if __name__ == '__main__':
    main()