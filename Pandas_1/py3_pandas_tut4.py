#!/usr/bin/python3
#encoding=utf8

def main():
    # Data set.
    d = [0,1,2,3,4,5,6,7,8,9]
    # Create data frame from data set.
    df = pd.DataFrame(d)
    # Set column name.
    df.columns = ['Rev']
    # Adding a column.
    df['NewCol'] = 5
    # Modifying the new column.
    df['NewCol'] = df['NewCol'] + 1
    # Deleting the last column.
    del df['NewCol']
    # Creating two additional columns.
    df['test'] = 3
    df['col'] = df['Rev']
    # Changing indexes.
    my_idx = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    df.index = my_idx
    print(df.head(10))
    # Get specific rows of data by the index label.
    print('\nFirst row');
    print(df.loc['a'])
    # Get rows in a range.
    print('\nRows from a to d')
    print(df.loc['a':'d'])
    # Get rows by their numerical index.
    print('\nRows from indexes 1 to 4')
    print(df.iloc[1:4])
    # Selecting a single column.
    print('\nThe Rev column')
    print(df['Rev'])
    # Selecting several columns.
    print('\n Columns Rev y test')
    print(df[['Rev', 'test']])
    # Selecting an specific submatrix with row labels.
    print('\nSelecting specific submatrix with row labels')
    print(df.loc[['a', 'd', 'i'], ['Rev', 'col']])
    # Selecting an specific submatrix with row indexes.
    print('\nSelecting specific submatrix with row indexes')
    print(df.ix[[1, 5, 4], ['Rev', 'col']])

if(__name__ == '__main__'):
    # Importing specific functions.
    # Importing libraries.
    import pandas as pd

    main()