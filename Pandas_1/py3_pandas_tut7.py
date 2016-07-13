#!/usr/bin/python3
#encoding-utf8

def Outlier_1(df):
    """Measuring deviations from mean in the whole data set"""
    print('\nMethod 1')
    sdf = df.copy()
    sdf['Rev-Mean'] = abs(sdf['Revenue'] - sdf['Revenue'].mean())
    sdf['cutoff'] = 1.96*sdf['Revenue'].std()
    sdf['Outlier'] = abs(sdf['Revenue'] - sdf['Revenue'].mean()) > sdf['cutoff']
    print(sdf.ix[:,:])

def Outlier_2_1(df):
    """Measuring deviations from the mean per state"""
    print('\nMethod 2.1')
    sdf = df.copy()
    ob = sdf.groupby('State')
    sdf['Rev-Mean'] = ob.transform(lambda x: abs(x - x.mean()))
    sdf['cutoff'] = ob.transform(lambda x: 1.96*x.std())
    sdf['Outlier'] = ob.transform(lambda x: abs(x - x.mean()) > 1.96*x.std())
    print(sdf.ix[:,:])

def Outlier_2_2(df):
    """Measuring deviations from the mean per state and month"""
    print('\nMethod 2.2')
    sdf = df.copy()
    ob = sdf.groupby(['State', lambda x: x.month])
    sdf['Rev-Mean'] = ob.transform(lambda x: abs(x - x.mean()))
    sdf['cutoff'] = ob.transform(lambda x: 1.96*x.std())
    sdf['Outlier'] = ob.transform(lambda x: abs(x - x.mean()) > 1.96*x.std())
    print(sdf.ix[:,:])

def main():
    # Create a 1st data frame with date index.
    sta = ['NY', 'NY', 'NY', 'NY', 'FL', 'FL', 'GA', 'GA', 'FL', 'FL']
    val = [1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dat = pd.date_range(start = '1/1/2012', periods = 10, freq = 'MS')
    df1 = pd.DataFrame(data  = val, index = dat, columns = ['Revenue'])
    df1['State'] = sta
    print('\n1st data frame')
    print(df1.ix[:,:])
    print(df1.index)
    # Create a 2nd data frame.
    val = [10.0, 10.0, 9, 9, 8, 8, 7, 7, 6, 6]
    dat = pd.date_range('1/1/2013', periods=10, freq='MS')
    df2 = pd.DataFrame(data = val, index = dat, columns = ['Revenue'])
    df2['State'] = sta
    print('\n2nd data frame')
    print(df2.ix[:,:])
    print(df2.index)
    # Merge the two initial data frames.
    df = pd.concat([df1,df2])
    print('\nMerged data frame')
    print(df.ix[:,:])
    print(df.index)
    # Evaluate outliers.
    Outlier_1(df)
    Outlier_2_1(df)
    Outlier_2_2(df)

if(__name__ == '__main__'):
    import pandas as pd
    import numpy as np
    main()