#!/usr/bin/python3
#encoding-utf8
"""
16th tutorial from the series:

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
        ax3.legend(loc = 4)
        plt.show()
    # Delete locally added information.
    hpi.drop([add_std1, add_std2, add_corr], axis = 1, inplace = True)

def analyze_hpi_mortgage(hpi, hpi_avg, mort):
    """
    Merge HPI per state and national avg ans well as the 30 years mortgage rate

    and perform the analysis of the complete data set.
    """
    housing = hpi.join(mort)
    #housing = housing.join(hpi_avg)
    # Lets find out the correlation between the mortgage rate and the HPI.
    print('\nCorrelation between 30 years mortgage rate and HPI')
    print(housing.corr()['M30'].describe())

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
            mnt = get_quandl_single_column(key, col_name = str(st_abb),
                quandl_label = st_name, init_date = '1975-01-01',
                FLAG_WR = False)
            if hpi.empty:
                hpi = mnt
            else:
                hpi = hpi.join(mnt)
        hpi.to_csv(hpi_name)
    return(hpi)

def get_quandl_single_column(key, col_name, quandl_label, init_date,
    res = [], FLAG_WR = True):
    """
    Get the requested single-column data file from Quandl.

    If the requested data has been downloaded before, then it will be read
    directly from file_name, otherwise it will be downloaded from Quandl.
    """
    file_name = 'dat_' + col_name + '.csv'
    if(os.path.isfile(file_name)):
        print('\nReading ' + col_name + ' from ' + file_name)
        mnt = pd.read_csv(file_name, index_col = 0, header = 0,
            parse_dates = True)
    else:
        print('\nDownloading ' + col_name + ' from Quandl')
        mnt = qd.get(quandl_label, trim_start = init_date, authtoken = key)
        # Get only the last column.
        mnt = mnt.iloc[:,[-1]]
        mnt.columns = [col_name]
        # Normalize data with respect to the initial date.
        mnt[col_name] = 100*(mnt[col_name] - mnt[col_name][0])/mnt[col_name][0]
        # Apply the requested resampling procedures.
        for typ in res:
            mnt = mnt.resample(typ).mean()
            mnt = mnt.resample(typ).mean()
        if(FLAG_WR):
            mnt.to_csv(file_name)
    return(mnt)

def machine_learning_1st_try(hpi_state, econ_idxs):
    """
    A first approach to machine learning techniques.

    Applying methods to entire columns.
    """
    # Merge HPI per state with the global economy indicators.
    hpi_all = hpi_state.join(econ_idxs)
    # Focus on the relative changes between consecutive years.
    hpi_all = hpi_all.pct_change()
    # We want to train the algorithm to identify when it tis a good opportunity
    # to buy a house. That should happen every time that the HPI decreases in
    # comparison to the previous year, So lets compare the actual HPI to that of
    # the next year, creating a new column called 'HPI_FUT'.
    hpi_all['HPI_FUT'] = hpi_all['HPI_US'].shift(-1)
    # Compare the current and future values.
    hpi_all['HPI_LAB'] = list(map(labeler,hpi_all['HPI_FUT'],hpi_all['HPI_US']))
    # Drop NaN's and inf's.
    hpi_all.replace([np.inf,-np.inf], np.nan, inplace = True)
    hpi_all.dropna(inplace = True)
    print(hpi_all)

def labeler(x1, x2):
    """
    Returns 1 if x1 > x2 and 0 otherwise.
    """
    if(x1 > x2):
        return(1)
    else:
        return(0)

def machine_learning_2nd_try(hpi_state, econ_idxs):
    """
    A second approach to machine learning techniques.

    SKLeard classifier.
    """
    # Merge HPI per state with the global economy indicators.
    hpi_all = hpi_state.join(econ_idxs)
    # Focus on the relative changes between consecutive years.
    hpi_all = hpi_all.pct_change()
    # We want to train the algorithm to identify when it tis a good opportunity
    # to buy a house. That should happen every time that the HPI decreases in
    # comparison to the previous year, So lets compare the actual HPI to that of
    # the next year, creating a new column called 'HPI_FUT'.
    hpi_all['HPI_FUT'] = hpi_all['HPI_US'].shift(-1)
    # Compare the current and future values.
    hpi_all['HPI_LAB'] = list(map(labeler,hpi_all['HPI_FUT'],hpi_all['HPI_US']))
    # Drop NaN's and inf's.
    hpi_all.replace([np.inf,-np.inf], np.nan, inplace = True)
    hpi_all.dropna(inplace = True)
    # Set the feature and labels for the machine learning classifier.
    X = np.array(hpi_all.drop(['HPI_LAB','HPI_FUT'], axis = 1))
    X = preprocessing.scale(X)
    y = np.array(hpi_all['HPI_LAB'])
    # Now is time to train and test.
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y,
        test_size = 0.2)
    clf = svm.SVC(kernel = 'linear')
    clf.fit(X_train, y_train)
    # print the results of the training.
    print(clf.score(X_test, y_test))

def main():
    # I guess that this sets the plotting style to emulate R's ggplot2.
    style.use('fivethirtyeight')
    # Read private key for Quandl account.
    key = get_quandl_key()
    # Get list of abbreviations from wikipedia.
    abb = get_state_abbreviations()
    # Get house price index (HPI) from Quandal (or local file, if existing).
    hpi_state = get_hpi(key, abb)
    # Get HPI's national average from Quandal (or local file, if existing).
    hpi_avg = get_quandl_single_column(key = key, col_name = 'HPI_US',
        quandl_label = 'FMAC/HPI_USA', init_date = '1975-01-01')
    # Find the HPI correlation between all the states.
    get_hpi_correlation(hpi_state)
    # Resample data for a single state, annually.
    resample_for_state(hpi_state, state = 'TX', FLAG_plot = False)
    # Handling missing data.
    handle_missing_data(hpi_state, state ='AK', FLAG_plot = False)
    # Computing moving/rolling stats.
    rolling_stats(hpi_state, stat1 ='TX', stat2 = 'AK', FLAG_plot = False)
    # Read 30 year mortgage.
    mort = get_quandl_single_column(key = key, col_name = 'M30',
        quandl_label = 'FMAC/MORTG', init_date = '1975-01-01',
        res = ['1D', 'M'])
    # Analyze the joint HPI + mortgage data.
    analyze_hpi_mortgage(hpi_state, hpi_avg, mort)
    # Get stock market indicator.
    sp500 = get_quandl_single_column(key = key, col_name = 'SP500',
        quandl_label = 'YAHOO/INDEX_GSPC', init_date = '1975-01-01',
        res = ['M'])
    print(sp500.head())
    # Get gross domestic product.
    gdp = get_quandl_single_column(key = key, col_name = 'GDP',
        quandl_label = 'BCB/4385', init_date = '1975-01-01',
        res = ['M'])
    # Find the correlation between national economic indicators/indexes.
    econ_idxs = mort.join([sp500,gdp,hpi_avg])
    print(econ_idxs.corr())
    # Lets have a 1st try on machine learning algorithms. Applying methods to
    # data frame columns.
    machine_learning_1st_try(hpi_state, econ_idxs)
    # 2nd machine learning try. SKLearn classifiers.
    machine_learning_2nd_try(hpi_state, econ_idxs)

if __name__ == '__main__':
    import os.path
    import numpy as np
    import pandas as pd
    import quandl as qd
    import matplotlib.pyplot as plt
    from matplotlib import style
    from sklearn import svm, preprocessing, cross_validation

    main()
