#!/usr/bin/python3
#encoding-utf8
"""
1st tutorial from the series:

https://pythonprogramming.net/regression-introduction-machine-learning-tutorial/

"""
def get_quandl_key():
    return(str(open('key_quandl.key','r').read().strip()))

def main():
    # Grab some data from Quandl.
    key = get_quandl_key()
    df = qd.get('WIKI/GOOGL')
    print(df.head())

if __name__ == '__main__':
    import pandas as pd
    import quandl as qd
    import os.path
    import matplotlib.pyplot as plt

    main()
