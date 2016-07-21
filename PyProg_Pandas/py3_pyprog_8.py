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
    Read house pricing index (HPI) for each US state and the national average.

    If HPI haven't been read before, it will be downloaded from the quandl and
    then printed to 'dat_hpi_per_state.csv'. On the contrary, hpi data frame
    will be directly read from 'dat_hpi_per_state.csv'.
    """
    hpi_name = 'dat_hpi_per_state.csv'
    if(os.path.isfile(hpi_name)):
        print('\nReading data from ' + hpi_name)
        hpi = pd.read_csv(hpi_name, index_col = 0, header = 0)
    else:
        print('\nLoading HPI data from Quandl')
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
    return(hpi)

def get_hpi_benchmark(key = ''):
    """
    Get national average HPI.

    If the national average has been downloaded before, then it will be directly
    read from 'dat_hpi_national_avg.csv', otherwise it will be downloaded from
    Quandl.
    """
    hpi_name = 'dat_hpi_national_avg.csv'
    label = 'HPI_AVG'
    if(os.path.isfile(hpi_name)):
        print('\nReading national average HPI from Quandl')
        mnt = pd.read_csv(hpi_name, index_col = 0, header = 0)
    else:
        print('\nDownloading national average HPI from Quandl')
        mnt = qd.get('FMAC/HPI_USA', authtoken = key)
        mnt.columns = [label]
        # Normalize data with respect to the initial date.
        mnt[label] = 100 * (mnt[label] - mnt[label][0]) / mnt[label][0]
        mnt.to_csv(hpi_name)
    return(mnt)

def main():
    key = get_quandl_key()
    abb = get_state_abbreviations()
    hpi = get_hpi(key, abb)
    hpi_avg = get_hpi_benchmark(key)
    # Find the HPI correlation between all the states.
    print('\nHPI correlation between states')
    hpi_corr = hpi.corr()
    print(hpi_corr)
    print('\nHPI correlation (Summary)')
    print(hpi_corr.describe())

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    hpi.plot(ax = ax1)
    hpi_avg.plot(ax = ax1, color = 'k', linewidth = 10)
    plt.show()

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import os.path
    import matplotlib.pyplot as plt

    #main_main()
    main()
