#!/usr/bin/python3
#encoding-utf8
"""
1st tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # I guess that this sets the plotting style to emulate R's ggplot2.
    style.use('ggplot')
    # Initialize the time windows for the data to be handled in this tutorial.
    start = datetime.datetime(year = 2010, month = 1, day = 1)
    #end = datetime.datetime(year = 2015, month = 1, day = 1)
    end = datetime.datetime.today()
    # Import financial information of Exxon Mobil Corporation 'XOM' from Yahoo.
    df = web.DataReader('XOM', 'yahoo', start, end)
    print(df.head())
    df['Adj Close'].plot()
    plt.show()

if __name__ == '__main__':
    import pandas as pd
    import datetime
    #import pandas.io.data as web
    import pandas_datareader.data as web
    import matplotlib.pyplot as plt
    from matplotlib import style

    main()