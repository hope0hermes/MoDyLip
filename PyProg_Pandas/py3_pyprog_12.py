#!/usr/bin/python3
#encoding-utf8
"""
12th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Setting plotting style to emulate R's ggplot2.
    style.use('fivethirtyeight')
    # Define a new data set.
    height = {'meters':
        [10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}
    # Read data into a data frame.
    df = pd.DataFrame(data = height)
    df['STD'] = df['meters'].rolling(window = 2).std()
    print('\nOriginal data set')
    print(df.ix[:,:])
    height_std = float(df.std()['meters'])
    # Standard deviation of the entire data set ('meters' column).
    print('\nStandard deviation of the entire data set')
    print(height_std)
    # Selecting only those entries whose local standard deviation is smaller
    # than that of the whole data set.
    print('\nSTD filtered data set')
    df = df[ df['STD'] < height_std ]
    print(df.ix[:,:])
    df['meters'].plot()
    plt.legend()
    plt.show()

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import os.path
    import matplotlib.pyplot as plt
    from matplotlib import style

    main()
