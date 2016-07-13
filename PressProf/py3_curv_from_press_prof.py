#!/usr/bin/python
#encoding-utf8

def plot_mom1_vs_lat_press_prof(run):
    """
    Plot the lateral pressure profile and its 1st integral momentum.

    :param run: List with the different pressure profiles.
    :type run: [LatPressProf]

    """
    fig,axes=plt.subplots(2,sharex=True,sharey=False,figsize=(8.0,10.0))
    fig.subplots_adjust(hspace=0)
    for ax in axes:
        ax.xaxis.grid(True,'major')
        ax.yaxis.grid(True,'major')
    for prof in run:
        axes[0].plot(prof.height, prof.prof)
        axes[1].plot(prof.height, prof.get_momentum(1))
    plt.show()

def main():
    """
    Main sentinel for standalone and module usage.

    """
    run_tens = []
    run_prof = []
    #CheckPressTensFile(argv[1:])
    for x in argv[1:]:
        # Lateral pressure profile.
        prof = lpp.LatPressProf(x)
        prof.get_momentum(0)
        prof.get_momentum(1)
        run_prof.append(prof)

        # Pressure tensor.
        #tens = pt.PressTens(x)
        #run_tens.append(tens)
    plot_mom1_vs_lat_press_prof(run_prof)

    """plt.figure(1)
    x = run_prof[0].height
    y1 = run_prof[0].get_momentum(1)
    y2 = run_prof[1].get_momentum(1)
    plt.subplot(111)
    plt.plot(x, y1, x, y2)
    plt.show()"""

if __name__ == '__main__':
    from sys import argv
    import matplotlib.pyplot as plt
    import py3_lat_press_prof as lpp
    import py3_press_tens as pt
    import numpy as np
    import math
    import os
    import io
    main()