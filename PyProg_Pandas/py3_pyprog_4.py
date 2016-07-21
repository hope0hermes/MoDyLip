#!/usr/bin/python3
#encoding-utf8
"""
4th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Importing House Price Index (HPI) for Alaska
    df = qd.get('FMAC/HPI_AK')
    print('\nImporting HPI for Alaska')
    print(df.head())
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
    print('\nSelecting what we want to query')
    for abb in st[0][0][1:]: print('FMAC/HPI_' + abb)

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd

    main()