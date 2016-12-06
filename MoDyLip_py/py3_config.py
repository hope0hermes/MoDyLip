# #!/usr/bin/python3
# #encoding-utf8

import numpy as np
import copy
import os
import matplotlib.pyplot as plt
from operator import itemgetter

import py3_grid_mapping as gmp

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
        # Header parameters.
        self.n_beads = None
        self.time = None
        self.box = None
        self.vir2 = None
        self.vir3 = None
        self.l0 = None
        self.kb = None
        self.ks = None
        self.ch_len = None
        self.Re = None
        self.cutoff3 = None
        self.cutoff2 = None
        self.n_chains = None
        self.n_beads = None
        # Configuration body.
        self.cfg = None
        self._cm = None
        self.ch_arch = None
        # Leaflet identifier.
        self._leaf = None

        # Read control parameters.
        self._ParseHeader(stream)
        # Read configuration.
        self._ParseBody(stream)
        # Close file.
        stream.close()

    @classmethod
    def PlotConfig(self, cfg, prop='leaf', sat=0.2, size=50):
        """
        Plot the three principal projections of the configuration.

        """
        # Check input parameters.
        prop_dict = {'block':3, 'leaf':4}
        assert prop in prop_dict, 'Invalid \'prop\' to be plotted'
        col = prop_dict[prop]
        assert (sat > 0. and sat <= 1.), '\'sat\' should be in (0, 1]'
        assert size > 0, 'Invalid size'

        fig = plt.figure(figsize=(12,12))
        ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3)
        ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=3)
        ax3 = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1)

        ax1.scatter(cfg[:,0], cfg[:,2], c=cfg[:,col], s=size, alpha=sat)
        ax2.scatter(cfg[:,0], cfg[:,1], c=cfg[:,col], s=size, alpha=2*sat)
        ax3.scatter(cfg[:,2], cfg[:,1], c=cfg[:,col], s=size, alpha=sat)

        plt.show()

    def GetSubset(self, leaflet=None, arch=None, block=None,
        target='single', points=[32,32], cm=False):
        """
        Returns a subset of beads, characterized by the leaflet, chain
        architecture and lipid sub-block.

        """
        # Check if leaflets have been labeled.
        if(self._leaf is None):
            self._LabelLeaflets(target, points)
        # Parse flag values from input parameters.
        leaf_flag, arch_flag, block_flag = self._ParseInputGetSubset(leaflet,
            arch, block)
        sub = []
        buff = [ 5*[0] for y in range(self.ch_len)]
        for bd_base in range(0, self.n_beads, self.ch_len):
            leaf_val = int(self._leaf[bd_base])
            arch_val = int(self.cfg[bd_base, 6])
            buff_len = int(0)
            for bd in range(bd_base, bd_base + self.ch_len):
                block_val = int(self.cfg[bd, 6])
                sel = self._SelectBead(
                    leaf_val, arch_val, block_val,
                    leaf_flag, arch_flag, block_flag)
                if(sel):
                    for k in range(3): buff[buff_len][k] = float(self.cfg[bd,k])
                    buff[buff_len][3] = int(self.cfg[bd,6])
                    buff[buff_len][4] = int(self._leaf[bd])
                    buff_len += 1
            if(buff_len > 0):
                if(cm):
                    buff, buff_len = self._CoarseGrainSubset(buff, buff_len)
                for idx in range(buff_len):
                    sub.append(copy.deepcopy(buff[idx][:]))
        return(np.array(sub))

    def _CoarseGrainSubset(self, buff, buff_len):
        """
        Evaluate the center of mass of the selected block within a single chain.

        If necessary, the chain will be unfolded and the resulting center of
        mass will be brought back into the simulation region.

        """
        cm = buff[0][0:3]
        for idx in range(1,buff_len):
            for k in range(3):
                cm[k] += buff[idx][k]
                dist = buff[idx][k] - buff[0][k]
                if(dist > 0.5*self.box[k]):
                    cm[k] -= self.box[k]
                elif(dist < -0.5*self.box[k]):
                    cm[k] += self.box[k]

        tot_cm = np.mean(self.cfg[:, 0:3], axis=0)

        for k in range(3):
            buff[0][k] = cm[k] / buff_len
            if( cm[k] >= ( tot_cm[k] + 0.5*self.box[k] ) ):
                cm[k] -= self.box[k]
            elif( cm[k] <= ( tot_cm[k] - 0.5*self.box[k] ) ):
                cm[k] += self.box[k]

        return(buff, 1)

    def _SelectBead(self, leaf_val, arch_val, block_val,
        leaf_flag, arch_flag, block_flag):
        """
        Check if a bead belongs to the requested subset, which is defined by
        the input flags.

        """
        leaf_sel = False
        arch_sel = False
        block_sel = False
        if((leaf_flag is None) or (leaf_val == leaf_flag)):
            leaf_sel = True
        if((arch_flag is None) or (arch_val == arch_flag)):
            arch_sel = True
        if((block_flag is None) or
            ((block_flag == -1) and (block_val > 0)) or
            (block_val == block_flag)):
            block_sel = True
        return(leaf_sel and arch_sel and block_sel)

    def _ParseInputGetSubset(self, leaflet, arch, block):
        """
        Parses parameters passed in to 'GetSubset' and return the set of values
        to be drawn from the different columns of 'self.cfg'

        """
        leaf_flag = None
        arch_flag = None
        block_flag = None
        # Parse leaflet.
        if(leaflet is None):
            leaf_flag = None
        else:
            leaflet = leaflet.lower()
            if((leaflet == 'upper') or (leaflet == 'outer')):
                leaf_flag = 1
            elif((leaflet == 'lower') or (leaflet == 'inner')):
                leaf_flag = 0
            else:
                assert False, 'Invalid \'leafalet\' option'
        # Parse chain architecture.
        if(arch is None):
            arch_flag = None
        else:
            arch_flag = int(arch[0])
        # Parse block.
        if(block is None):
            block_flag = None
        else:
            block = block.lower()
            if(arch_flag is None):
                if(block == 'head'):
                    block_flag = -1
                elif(block == 'tail'):
                    block_flag = 0
                else:
                    assert False, 'Invalid \'block\' option'
            else:
                if(block == 'head'):
                    block_flag = arch_flag
                elif(block == 'tail'):
                    block_flag = 0
                else:
                    assert False, 'Invalid \'block\' option'
        return(leaf_flag, arch_flag, block_flag)

    def _LabelLeaflets(self, target='single', points=[32,32]):
        """
        Labels chains according to its leaflet.

        """
        try:
            self.bilayer_cm
        except AttributeError:
            self.bilayer_cm = gmp.GridMap(self.cfg[:, [0,1]], self.cfg[:, 2],
                points)

        self._leaf = np.empty([self.n_beads,1], dtype=int)
        point = [float] * 3
        for bd_base in range(0, self.n_beads, self.ch_len):
            if(target == 'cm'):
                for k in range(3): point[k] = 0.
                for bd in range(bd_base, bd_base + self.ch_len):
                    for k in range(3): point[k] += self.cfg[bd, k] / self.ch_len
            elif(target == 'single'):
                for k in range(3): point[k] = self.cfg[bd_base, k]
            else:
                assert False, 'Specify \'cm\' or \'single\''
            val = self.bilayer_cm.ClassifyPoint(point)
            for bd in range(bd_base, bd_base + self.ch_len):
                self._leaf[bd] = val

    def Backfold(self):
        """
        Wraps particles into the simulation box.

        """
        orig = self._cm - 0.5*self.box
        for row in range(self.n_beads):
            for col in range(3):
                rel_pos = self.cfg[row, col] - orig[col]
                self.cfg[row, col] = np.mod(rel_pos, self.box[col]) + orig[col]

    def MoveTo(self, location=[0., 0., 0.]):
        """
        Translates configuration center of mass to the specified location.

        :param location: New configuration center of mass.

        :type location: [float]

        """
        shift = location - self._cm
        if(np.linalg.norm(shift) > 1.e-3):
            self.cfg[:, 0:3] += shift

    def GetCenterOfMass(self):
        """
        Evaluates and returns the configuration center of mass.

        """
        self._cm = np.mean(self.cfg[:, 0:3], axis=0)
        return(self._cm)

    def _ParseBody(self, stream):
        """
        Read particles' position, velocity and type.

        Returns a ndarray of shape (n_beads, 7), where the 6 attributes
        (columns) are the coordinated bead position and velocities, and the last
        attribute is the bead type. It also identifies the different chain
        architectures (returned in self.ch_arch) and the center of mass of the
        system (returned in self._cm).

        :param stream: Data stream to the input configuration file
        :param cfg: Array of shape (n_beads, 7) storing the three coordinated
            positions and velocities of each particles and its type
        :param ch_arch: Chain architectures identified in the input file
        :param _cm: Center of mass of the system

        :type stream: File object
        :type cfg: ndarray([n_beads, 7], dtype=float)
        :type ch_arch: []
        :type _cm: ndarray([3], dtype=float)

        """
        # Declarations.
        self.cfg = np.empty([self.n_beads, 7], dtype=np.float)
        self._cm = np.zeros(3, dtype=np.float)
        self.ch_arch = []
        buff = [float(0)] * self.ch_len
        # Rewind array.
        stream.seek(0)
        row = int(0)
        bead = int(0)
        for line in stream:
            line = line.split()
            if line[0].startswith('#'):
                continue
            elif(len(line) == 7):
                # Position.
                for col in range(3):
                    self.cfg[row, col] = float(line[col])
                    self._cm[col] += self.cfg[row, col]
                # Velocity.
                for col in range(3, 6):
                    self.cfg[row, col] = float(line[col])
                # Type.
                self.cfg[row, 6] = float(line[6])
                buff[bead] = self.cfg[row, 6]
                bead += 1
                if(bead == self.ch_len):
                    self._IdentifyChainArch(buff)
                    bead = 0
                # Read the next bead.
                row += 1
            else:
                continue
        assert self.n_beads == row, 'n_beads != n_chains * ch_len'
        self._cm /= self.n_beads
        # Sort chain architectures by their 1st head-group bead.
        print('Chain architectures')
        self.ch_arch.sort(key=itemgetter(0))
        for ch in self.ch_arch: print(ch)

    def _IdentifyChainArch(self, buff):
        """
        Identifies new chain architectures in the passed in buffer and appends
        them to ch_arch.

        :param buff: Input chain architecture
        :param ch_arch: List storing all the different chain architectures.

        :type buff: [float]
        :type ch_arch: [[float]]

        """
        num_archs = len(self.ch_arch)
        if(num_archs == 0):
            self.ch_arch.append(copy.deepcopy(buff))
        else:
            mismatch = 0
            for ch in self.ch_arch:
                if(buff[0] != ch[0]): mismatch += 1
            if(mismatch == num_archs):
                self.ch_arch.append(copy.deepcopy(buff))

    def _ParseHeader(self, stream):
        """
        Read simulation control parameters and set the total number of beads.

        :param stream: Data stream to the input configuration file

        :type stream: File object

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
                self.n_beads = self.n_chains * self.ch_len
            else:
                break

# def main():
#     cof = Configuration('configuration_00000000.cfg')
#
# if __name__ == '__main__':
#     main()
