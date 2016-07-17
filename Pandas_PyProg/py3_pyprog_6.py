#!/usr/bin/python3
#encoding-utf8
"""
6th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Create 3 different data frames that latter on will be concatenated or
    # appended.
    df1 = pd.DataFrame({'Year':[2001,2002,2003,2004], 'Int_Rate':[2,3,2,2],
        'US_GDP_Thousands':[50,55,65,55]})
    df2 = pd.DataFrame({'Year':[2002,2003,2004,2005], 'Unemployment':[7,8,9,6],
        'Low_Tier_Rate':[50,52,50,53]})
    print('\nThese are the original data frames')
    print(df1)
    print(df2)
    # Merging left.
    m_l = pd.merge(df1,df2, on = ['Year'], how = 'left')
    print('\nMerging left on year')
    print(m_l)
    # Merging right.
    m_r = pd.merge(df1,df2, on = ['Year'], how = 'right')
    print('\nMerging right on year')
    print(m_r)
    # Merging outer.
    m_o = pd.merge(df1,df2, on = ['Year'], how = 'outer')
    print('\nMerging outer on year')
    print(m_o)
    # Merging inner.
    m_i = pd.merge(df1,df2, on = ['Year'], how = 'inner')
    print('\nMerging inner on year')
    print(m_i)

if __name__ == '__main__':
    import pandas as pd

    main()
