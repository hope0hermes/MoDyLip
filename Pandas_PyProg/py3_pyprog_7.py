#!/usr/bin/python3
#encoding-utf8
"""
7th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Set user key for Quandl account.
    my_key = 'ThswsmTcwysrvCzeo6Rc'
    # Getting a list of the US states abbreviations. NOTE: read_html actually
    # returns a list of data frames. After going though all the elements in the
    # list, we realize that the data table displayed in the wikipage is stored
    # on the 1st element of the list.
    st = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    print('\nReading US states abbreviations from wikipedia')
    print('\n1st element in the list')
    print(st[0])
    # The abbreviations we need, however, are contained in the 1st column of the
    # 1st data frame.
    print('\nGetting HPI data from Quandl for all US states\n')
    df = pd.DataFrame()
    for abb in st[0][0][1:]:
        st_name = 'FMAC/HPI_' + str(abb)
        # Get HPI for each state and append to the main data structure.
        print('Reading and appending data from ' + st_name + '\r', end = '')
        mnt = qd.get(st_name, authtoken = my_key)
        mnt.columns = [abb]
        if df.empty:
            df = mnt
        else:
            df = df.join(mnt)
    print('\nThis is the final data frame read from Quandl')
    print(df.head())
    df.plot()
    plt.show()

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import matplotlib.pyplot as plt

    main()
