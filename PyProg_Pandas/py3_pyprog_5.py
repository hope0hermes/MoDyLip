#!/usr/bin/python3
#encoding-utf8
"""
5th tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Create 3 different data frames that latter on will be concatenated or
    # appended.
    df1 = pd.DataFrame({'HPI':[80,85,88,85], 'Int_Rate':[2,3,2,2],
        'US_GDP_Thousands':[50,55,65,55]}, index = [2001,2002,2003,2004])
    df2 = pd.DataFrame({'HPI':[80,85,88,85], 'Int_Rate':[2,3,2,2],
        'US_GDP_Thousands':[50,55,65,55]}, index = [2005,2006,2007,2008])
    df3 = pd.DataFrame({'HPI':[80,85,88,85], 'Int_Rate':[2,3,2,2],
        'Low_Tier_Rate':[50,52,50,53]}, index = [2001,2002,2003,2004])
    print('\nThese are the original data frames')
    print(df1)
    print(df2)
    print(df3)
    # Concatenating data frames 1 and 2.
    cat12 = pd.concat([df1,df2])
    print('\nThis is the concatenation of df1 and df2')
    print(cat12)
    # Concatenating data frames 1, 2 and 3.
    cat123 = pd.concat([df1,df2,df3])
    print('\nThis is the concatenation of df1, df2 and df3')
    print(cat123)
    # Appending df1 and df2.
    app12 = df1.append(df2)
    print('\nAfter appending df1 and df2')
    print(app12)
    # Appending df1 and df3.
    app13 = df1.append(df3)
    print('\nAfter appending df1 and df3')
    print(app13)

if __name__ == '__main__':
    import pandas as pd

    main()