#!/usr/bin/python3
#encoding-utf8

def main():
    """
    Nothing to be done

    """
    # Check existence of input files
    for in_file in argv[1:]:
        assert os.path.isfile(in_file), 'Can\'t open ' + in_file
    run = []
    for in_file in argv[1::10]:
        print(in_file)
        cfg = conf.Configuration(in_file)
        cfg.Backfold()
        cfg.MoveTo([0.,0.,0.])
        sub = cfg.GetSubset(
            leaflet='upper',
            arch=cfg.ch_arch[0],
            block='head')
        #conf.Configuration.PlotConfig(sub, prop='block')
        #run.append(sub)

        cfg = sub[:,[0,1]]
        lab = DBSCAN(eps=1.0, min_samples=9).fit_predict(cfg)
        # lab = MeanShift(cluster_all=True).fit_predict(cfg)

        sat = 0.2
        size = 80

        fig = plt.figure(figsize=(12,12))
        ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3)
        ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=3)
        ax3 = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1)

        #ax1.scatter(cfg[:,0], cfg[:,2], c=lab, s=size, alpha=sat)
        ax2.scatter(cfg[:,0], cfg[:,1], c=lab, s=size, alpha=2*sat)
        #ax3.scatter(cfg[:,2], cfg[:,1], c=lab, s=size, alpha=sat)

        plt.show()

    print(len(run))

if __name__ == '__main__':
    from sys import argv
    import numpy as np
    import copy
    import os
    import matplotlib.pyplot as plt
    from sklearn.cluster import DBSCAN
    from sklearn.cluster import MeanShift

    import py3_config as conf

    main()
