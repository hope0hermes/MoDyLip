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
        sub = cfg.GetSubset(
            leaflet='upper',
            arch=cfg.ch_arch[1],
            block='head')
        conf.Configuration.PlotConfig(sub, prop='leaf')
        run.append(sub)

    print(len(run))

if __name__ == '__main__':
    from sys import argv
    import numpy as np
    import copy
    import os

    import py3_config as conf

    main()
