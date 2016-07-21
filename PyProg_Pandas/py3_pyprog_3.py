#!/usr/bin/python3
#encoding-utf8
"""
3rd tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Set data frame from CSV file.
    df = pd.read_csv('ZILL-Z77006_3B.csv')
    print('\nOriginal data')
    print(df.head())
    # Set 1st column as index.
    df.set_index('Date', inplace=True)
    print('\nData frame with new index')
    print(df.head())
    # Setting desired index at the very moment of reading the CSV file.
    df1 = pd.read_csv('ZILL-Z77006_3B.csv', index_col=0)
    print('\nWhen setting the index while reading the CSV file')
    print(df1.head())
    # Setting a new column name.
    df1.columns = ['Austin_HPI']
    print('\nAfter setting the new column name')
    print(df1.head())

if __name__ == '__main__':
    import pandas as pd

    main()