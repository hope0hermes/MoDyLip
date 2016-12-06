#!/usr/bin/python3
#encoding-utf8

def PlotClusters_1(cfg, lab, box):
    """
    Plot clusters

    """
    fig = plt.figure(figsize=(12,12))
    ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3)
    ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=3)
    ax3 = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1)

    win = 0.7
    ax2.set_xlim([int(-win*box[0]),int(win*box[0])])
    ax2.set_ylim([int(-win*box[1]),int(win*box[1])])

    sat = 0.8
    size = 60
    my_s = []
    negro = 0
    balnc = 0
    for val in lab:
        if val == -1:
            zz = size / 4
            negro += 1
        else:
            zz = size
            balnc += 1
        my_s.append(zz)

    ax1.scatter(cfg[:,0], cfg[:,2], c=lab, s=my_s, alpha=sat)
    ax2.scatter(cfg[:,0], cfg[:,1], c=lab, s=my_s, alpha=sat)
    ax3.scatter(cfg[:,2], cfg[:,1], c=lab, s=my_s, alpha=sat)

    plt.show()

def PlotClusters(cfg, cfg_old, lab, box):
    """
    Plot clusters

    """
    fig = plt.figure(figsize=(21,12))
    ax0 = plt.subplot2grid((4,7), (1,0), rowspan=3, colspan=3)
    ax1 = plt.subplot2grid((4,7), (0,3), rowspan=1, colspan=3)
    ax2 = plt.subplot2grid((4,7), (1,3), rowspan=3, colspan=3)
    ax3 = plt.subplot2grid((4,7), (1,6), rowspan=3, colspan=1)

    win = 0.7
    ax0.set_xlim([int(-win*box[0]),int(win*box[0])])
    ax0.set_ylim([int(-win*box[1]),int(win*box[1])])
    ax2.set_xlim([int(-win*box[0]),int(win*box[0])])
    ax2.set_ylim([int(-win*box[1]),int(win*box[1])])

    sat = 0.8
    size = 60
    my_s = []
    negro = 0
    balnc = 0
    for val in lab:
        if val == -1:
            zz = size / 4
            negro += 1
        else:
            zz = size
            balnc += 1
        my_s.append(zz)

    lab_old = [int(x) for x in cfg_old[:,3]]

    ax0.scatter(cfg_old[:,0], cfg_old[:,1], c=lab_old, s=0.5*size, alpha=sat)
    ax1.scatter(cfg[:,0], cfg[:,2], c=lab, s=my_s, alpha=sat)
    ax2.scatter(cfg[:,0], cfg[:,1], c=lab, s=my_s, alpha=sat)
    ax3.scatter(cfg[:,2], cfg[:,1], c=lab, s=my_s, alpha=sat)

    plt.show()

def FindClusters(cfg, cfg_old, eps=1.5, min_samples=6, periodic=False, box=[]):
    """
    Find density clusters in the

    """
    if(not periodic):
        clf = DBSCAN(eps=eps, min_samples=min_samples)
    else:
        myMetric = metric.PeriodicMetric(box)
        algo = 'brute'
        clf = DBSCAN(eps=eps, min_samples=min_samples,
            algorithm=algo, metric=myMetric.Distance)

    clf.fit(cfg)

    # Plot clusters.
    mySet = set(clf.labels_)
    print(mySet)
    PlotClusters(cfg, cfg_old, clf.labels_, box)

def main():
    """
    Nothing to be done

    """
    # Check existence of input files
    for in_file in argv[1:]:
        assert os.path.isfile(in_file), 'Can\'t open ' + in_file
    run = []
    for in_file in argv[1::1]:
        print(in_file)
        cfg = conf.Configuration(in_file)
        cfg.Backfold()
        cfg.MoveTo([0.,0.,0.])
        sub_new = cfg.GetSubset(
            leaflet='upper',
            arch=cfg.ch_arch[0],
            block='head',
            cm=True)
        coord = [0,1,2]
        cfg_new = sub_new[:,coord]
        box = cfg.box[coord]
        print('box = ', box)
        print('len(cfg_new) = ', len(cfg_new))

        cfg_old = cfg.GetSubset(
            leaflet='upper',
            arch=None,
            block='head',
            cm=False)

        FindClusters(cfg_new, cfg_old, eps=1.7, min_samples=5, periodic=True, box=box)

        # lab = DBSCAN(eps=1.2, min_samples=8).fit_predict(cfg)
        # clf = DBSCAN(eps=1.5, min_samples=8)
        # clf.fit(cfg)


        # Plot clusters.
        # lab = clf.labels_
        # PlotClusters(cfg, lab)


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
    import py3_periodic_metric as metric

    main()
