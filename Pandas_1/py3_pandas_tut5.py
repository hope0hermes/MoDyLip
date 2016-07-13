#!/usr/bin/python3
#encoding-utf8

def main():
    # Original data set.
    dat = {'one' : [1,1], 'two' : [2,2]}
    idx = ['a','b']
    df = pd.DataFrame(data = dat, index = idx)
    # Print the original data frame.
    print('\nOriginal data frame')
    print(df.ix[:,:])
    print(df.index)
    # Bring the columns and place them in the index.
    print('\nEmbedding column labels into the index')
    df = df.stack()
    print(df.ix[:,:])
    print(df.index)
    # Unstacking column labels from the index.
    print('\nUnembedding column labels from the index')
    df = df.unstack()
    print(df.ix[:,:])
    print(df.index)
    # Transposing the data frame.
    df = df.transpose()
    print('\nTransposing the data frame')
    print(df.ix[:,:])
    print(df.index)

if(__name__ == '__main__'):
    import pandas as pd
    main()