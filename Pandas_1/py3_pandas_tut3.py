#!/usr/bin/python3
#encoding-utf8
"""
Small script to familiarize myself with the use of Pandas.

Lesson 3 in:

http://pandas.pydata.org/pandas-docs/version/0.18.1/tutorials.html

"""

def CreateDataSet(dat_file):
    np.random.seed(111)
    Output = []
    Number = 4

    for i in range(Number):
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')
        # Create random data
        data = np.random.randint(low=25,high=1000,size=len(rng))
        # Status pool
        status = [1,2,3]
        # Make a random list of statuses
        random_status = [status[np.random.randint(low=0,high=len(status))]
            for i in range(len(rng))]
        # State pool
        states = ['GA','FL','fl','NY','NJ','TX']
        # Make a random list of states
        random_states = [states[np.random.randint(low=0,high=len(states))]
            for i in range(len(rng))]
        Output.extend(zip(random_states, random_status, data, rng))
    # Create data frame and export it into an excel file.
    df = pd.DataFrame(data = Output,
        columns = ['State', 'Status', 'Customers', 'Date'])
    df.to_excel(dat_file, index= False)

def main():
    # Crate data set and print it into an excel file.
    dat_file = 'dat_pandas_tut3.xlsx'
    CreateDataSet(dat_file)
    # Read data from file.
    df = pd.read_excel(io = dat_file, header = 0, index_col = 'Date')
    # Capitalize 'State' labels and merge result belonging to the dame State.
    df.State = df.State.apply(lambda x: x.upper())
    # Select records with status 1 only (boolean vector method).
    df = df[df['Status'] == 1] # Or -> mask = df['Status'] == 1; df = df[mask]
    # Merge 'NJ' register with those of 'NY'.
    df.State[df['State'] == 'NJ'] = 'NY'
    #df.Customers.plot(figsize = (15, 5))
    #plt.show()
    # Group data by State and Date. The 'groupby' operation, however, only takes
    # column arguments and, at this point, 'Date' is not a column of the data
    # frame but the index 'label'. Therefore as to be reincorporate as a column.
    df.reset_index(inplace = True)
    gp = df.groupby(['State', 'Date'])
    df = gp.aggregate(np.sum)
    # Get ride of 'Status' column.
    del df['Status']
    #print(df.loc['FL']['2012':])
    # Group by State, year and month.
    l_sta = df.index.get_level_values(0)
    l_yea = df.index.get_level_values(1).year
    l_mon = df.index.get_level_values(1).month
    sym = df.groupby([l_sta, l_yea, l_mon]).sum()
    sym.index.set_names(['State', 'Year', 'Month'],
        level = [0, 1, 2], inplace = True)
    #print(sym.loc['FL'])
    #print(sym.loc['FL', 2012])
    # Get the maximum number of customers per year and month.
    print('Following the canonical approach')
    for sta in sym.index.get_level_values(0).unique():
        print(sym['Customers'].loc[sta].idxmax())
        print(sym['Customers'].loc[sta].max())

if __name__ == '__main__':
    # Importing specific functions.
    from pandas import DataFrame, read_csv
    from sys import argv
    # Importing libraries.
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    main()