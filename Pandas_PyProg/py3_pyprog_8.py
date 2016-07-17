#!/usr/bin/python3
#encoding-utf8
"""
8th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def get_quandl_key():
    return(str(open('key_quandl.key','r').read().strip()))

def get_state_abbreviations():
    """
    Read US states abbreviations.

    If abbreviatons haven't been read before, they will be downloaded from the
    wikipedia page and then printed to 'dat_states_abbv.dat'. On the contrary,
    they will be directly read from 'dat_states_abbv.dat'.
    """
    abb_name = 'dat_states_abbv.dat'
    if(os.path.isfile(abb_name)):
        abb = []
        for line in open(abb_name, 'r').readlines():
            abb.append(str(line.strip()))
    else:
        domain = 'https://simple.wikipedia.org/wiki/List_of_U.S._states'
        abb = pd.read_html(domain)[0][0][1:]
        abb_file = open(abb_name, 'w')
        for name in abb: abb_file.write(name + '\n')
        abb_file.close()
    return(abb)

def get_hpi(key = '', abb = []):
    """
    Read house pricing index (HPI) for aech state in the US.

    If HPI haven't been read before, it will be downloaded from the the
    corresponding quandl page and then printed to 'dat_hpi_per_state.csv'. On
    the contrary, hpi data frame will be directly read from
    'dat_hpi_per_state.csv'.
    """
    hpi_name = 'dat_hpi_per_state.csv'
    if(os.path.isfile(hpi_name)):
        print('\nReading data from ' + hpi_name)
        hpi = pd.read_csv(hpi_name, index_col = 0, header = 0)
    else:
        print('\nLoading data from Quandl')
        hpi = pd.DataFrame()
        for st_abb in abb:
            st_name = 'FMAC/HPI_' + str(st_abb)
            print('Loading data for ' + st_name + '\r', end = '')
            mnt = qd.get(st_name, authtoken = key)
            mnt.columns = [st_abb]
            # Normalize data with respect to the initial date.
            mnt[st_abb] = 100 * (mnt[st_abb] - mnt[st_abb][0]) / mnt[st_abb][0]
            if hpi.empty:
                hpi = mnt
            else:
                hpi = hpi.join(mnt)
        hpi.to_csv(hpi_name)
    hpi.plot()
    plt.show()
    return(hpi)

def main():
    key = get_quandl_key()
    #print(key)
    abb = get_state_abbreviations()
    #print(abb)
    hpi = get_hpi(key, abb)
    print(hpi.head())

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import os.path
    import matplotlib.pyplot as plt

    #main_main()
    main()
