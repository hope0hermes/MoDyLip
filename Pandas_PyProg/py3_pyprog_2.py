#!/usr/bin/python3
#encoding-utf8
"""
2nd tutorial from the series:

https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/

"""

def main():
    # Set plotting style to emulate R's ggplo2.
    style.use('ggplot')
    # Set the initial data set.
    web_stats = {'Day':[1,2,3,4,5,6],
                 'Visitors':[43,34,65,56,29,76],
                 'Bouncers':[65,67,78,65,45,52]}
    # Set the data frame.
    df = pd.DataFrame(web_stats)
    print('\nOriginal data frame')
    print(df.head())
    # Set a new index.
    df.set_index('Day',inplace=True)
    print('\nData frame with a new index')
    print(df.head())
    # Set a new plotting style and plot a single column.
    style.use('fivethirtyeight')
    df['Visitors'].plot()
    plt.show()
    # Now plot both columns.
    df.plot()
    plt.show()

if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import style

    main()