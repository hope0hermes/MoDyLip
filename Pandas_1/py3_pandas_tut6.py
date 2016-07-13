#!/usr/bin/python3
#encoding-utf8

def main():
    # Creating the data set.
    dat = {'one' : [1,1,1,1,1],
        'two' : [2,2,2,2,2],
        'letter' : ['a','a','b','b','c']}
    # Creating the data frame.
    df = pd.DataFrame(data = dat)
    print('\nOriginal data set')
    print(df.ix[:,:])
    print(df.index)
    # Grouping by 'letter'.
    ob1 = df.groupby(['letter']).aggregate(np.sum)
    print('\nGrouping by \'letter\' and adding individual contributions')
    print(ob1.ix[:,:])
    print(ob1.index)
    # Grouping by 'letter' and 'one'.
    ob2 = df.groupby(['letter','one']).aggregate(np.sum)
    print('\nGrouping by \'letter\' and \'one\' and adding contributions')
    print(ob2.ix[:,:])
    print(ob2.index)

if(__name__ == '__main__'):
    import pandas as pd
    import numpy as np
    main()