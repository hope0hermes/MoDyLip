#!/usr/bin/python3
#encoding-utf8

# Classify leaflets.
self.MoveTo([0., 0., 0.])
self.Backfold()
#self._LabelLeaflets()
my_up = self.GetSubset(
    leaflet='lower',
    arch=None,
    block='head',
    target='single',
    points=[32,32])
self.PlotConfig(my_up, prop='block')

def main():
    """

    """

if __name__ == '__main__':
    from sys import args
    import numpy as np
    import copy
    import os

    import py3_config as config

    main()
