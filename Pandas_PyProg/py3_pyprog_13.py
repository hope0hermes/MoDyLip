#!/usr/bin/python3
#encoding-utf8
"""
13th tutorial from the series:

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
        hpi = pd.read_csv(hpi_name, index_col = 0, header = 0,
            parse_dates = True)
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
        print('\nReading national average HPI from ' + hpi_name)
        mnt = pd.read_csv(hpi_name, index_col = 0, header = 0,
            parse_dates = True)
    else:
        print('\nDownloading national average HPI from Quandl')
        mnt = qd.get('FMAC/HPI_USA', authtoken = key)
        mnt.columns = [label]
        # Normalize data with respect to the initial date.
        mnt[label] = 100 * (mnt[label] - mnt[label][0]) / mnt[label][0]
        mnt.to_csv(hpi_name)
    return(mnt)

def resample_for_state(hpi, state = '', FLAG_plot = False):
    """
    Resample data for a single state.
    """
    print(hpi[state].head())
    st_1yr = hpi[state].resample('4A').mean()
    # Plot if requested.
    if(FLAG_plot):
        fig = plt.figure()
        ax1 = plt.subplot2grid((1,1), (0,0))
        hpi[state].plot(ax = ax1, label = 'Monthly HPI for ' + state)
        st_1yr.plot(ax = ax1, label = 'Yearly HPI for ' + state)
        plt.legend(loc = 4)
        plt.show()
    return(st_1yr)

def get_hpi_correlation(hpi):
    print('\nHPI correlation between states')
    hpi_corr = hpi.corr()
    print(hpi_corr)
    print('\nHPI correlation (Summary)')
    print(hpi_corr.describe())

def handle_missing_data(hpi, state = '', FLAG_plot = False):
    """
    Resample data for a single state.
    """
    period = 'A'
    added = state + '_' + period
    hpi[added] = hpi[state].resample(period).mean()
    print('\nOriginal data frame')
    print(hpi[[state,added]].head())
    # DROPPING NaN VALUES.
    # Dropping all rows with NaN in any column.
    drp_any = hpi.dropna()
    print('\nAfter dropping rows with NaN\'s in any column')
    print(drp_any[[state,added]].head())
    # Dropping rows were all its columns are NaN's.
    drp_all = hpi.dropna(how = 'all')
    print('\nAfter dropping rows were all the columns are NaN\'s')
    print(drp_all[[state,added]].head())
    # FILLING NaN VALUES.
    # Replacing NaN's with -999.
    fill_999 = hpi.fillna(value = -999)
    print('\nAfter replacing NaN\'s with -999')
    print(fill_999[[state,added]].head())
    # Filling forward.
    fill_fwd = hpi.fillna(method = 'ffill')
    print('\nAfter filling forward')
    print(fill_fwd[[state,added]].head())
    # Filling backwards.
    fill_rev = hpi.fillna(method = 'bfill')
    print('\nAfter filling forward')
    print(fill_rev[[state,added]].head())
    # Plot if requested.
    if(FLAG_plot):
        fig = plt.figure()
        ax1 = plt.subplot2grid((1,1), (0,0))
        hpi[state].plot(ax = ax1, label = 'Original')
        fill_fwd[added].plot(ax = ax1, label = 'forw')
        fill_rev[added].plot(ax = ax1, label = 'back')
        plt.legend(loc = 4)
        plt.show()
    # Delete locally added information.
    hpi.drop(added, axis = 1, inplace = True)

def rolling_stats(hpi, stat1 ='', stat2 = '', FLAG_plot = False):
    """
    Computing stats over desired time windows.
    """
    window = 12
    add_std1 = stat1 + '_STD' + str(window)
    add_std2 = stat2 + '_STD' + str(window)
    add_corr = stat1 + '_' + stat2 + '_CORR' + str(window)
    hpi[add_std1] = hpi[stat1].rolling(window = window, center = True).std()
    hpi[add_std2] = hpi[stat2].rolling(window = window, center = True).std()
    hpi[add_corr] = hpi[stat1].rolling(window = window,
        center = True).corr(hpi[stat2])
    # Plot if requested.
    if(FLAG_plot):
        fig = plt.figure()
        ax1 = plt.subplot2grid((3,1), (0,0))
        ax2 = plt.subplot2grid((3,1), (1,0), sharex = ax1)
        ax3 = plt.subplot2grid((3,1), (2,0), sharex = ax1)
        hpi[stat1].plot(ax = ax1, label = stat1)
        hpi[stat2].plot(ax = ax1, label = stat2)
        hpi[add_std1].plot(ax = ax2, label = add_std1)
        hpi[add_std2].plot(ax = ax2, label = add_std2)
        hpi[add_corr].plot(ax = ax3, label = add_corr)
        ax1.legend(loc = 2)
        ax2.legend(loc = 2)
        ax3.legend(loc = 2)
        plt.show()
    # Delete locally added information.
    hpi.drop([add_std1, add_std2, add_corr], axis = 1, inplace = True)

def get_mortgage_30y(key = ''):
    """
    Get the national 30 years mortgage rate.

    If the mortgage rate has been downloaded before, then it will be read
    directly from 'dat_30y_mortgage.csv', otherwise it will be downloaded from
    Quandl.
    """
    mort_name = 'dat_30y_mortgage.csv'
    label = 'MORT_30Y'
    if(os.path.isfile(mort_name)):
        print('\nReading 30 year mortgage rate from ' + mort_name)
        mort = pd.read_csv(mort_name, index_col = 0, header = 0,
            parse_dates = True)
    else:
        print('\nDownloading 30 years mortgage rate from Quandl')
        mort =qd.get('FMAC/30US', trim_start = '1975-01-01', authtoken = key)
        mort.columns = [label]
        # Normalize data with respect to the initial date.
        mort[label] = 100 * (mort[label] - mort[label][0]) / mort[label][0]
        # Cheat data so that entries appear at the end of the month and not at
        # the beginning.
        mort = mort.resample('D')
        mort = mort.resample('M')
        mort.to_csv(mort_name)
    return(mort)

def analyze_hpi_mortgage(hpi, hpi_avg, mort):
    """
    Merge HPI per state and national avg ans well as the 30 years mortgage rate

    and perform the analysis of the complete data set.
    """
    housing = hpi.join(mort)
    #housing = housing.join(hpi_avg)
    # Lets find out the correlation between the mortgage rate and the HPI.
    print('\nCorrelation between 30 years mortgage rate and HPI')
    print(housing.corr()['MORT_30Y'].describe())

def main():
    # I guess that this sets the plotting style to emulate R's ggplot2.
    style.use('fivethirtyeight')
    # Read private key for Quandl account.
    key = get_quandl_key()
    # Get list of abbreviations from wikipedia.
    abb = get_state_abbreviations()
    # Get house price index (HPI) from Quandal (or local file, if existing).
    hpi = get_hpi(key, abb)
    # Get HPI's national average from Quandal (or local file, if existing).
    hpi_avg = get_hpi_benchmark(key)
    # Find the HPI correlation between all the states.
    get_hpi_correlation(hpi)
    # Resample data for a single state, annually.
    resample_for_state(hpi, state = 'TX', FLAG_plot = False)
    # Handling missing data.
    handle_missing_data(hpi, state ='AK', FLAG_plot = False)
    # Computing moving/rolling stats.
    rolling_stats(hpi, stat1 ='TX', stat2 = 'AK', FLAG_plot = False)
    # Read 30 year mortgage.
    mort = get_mortgage_30y(key)
    # Analyze the joint HPI + mortgage data.
    analyze_hpi_mortgage(hpi, hpi_avg, mort)

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import os.path
    import matplotlib.pyplot as plt
    from matplotlib import style

    main()
