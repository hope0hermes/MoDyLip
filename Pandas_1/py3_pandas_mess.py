#!/usr/bin/python3
#encoding-utf8
"""
Small script to familiarize myself with the use of Pandas.
"""
def check_input():
    if(len(argv) != 2):
        print('Should provide a single input file with the data to analyze')
        exit(1)
    return(argv[1])

def simple_commands():
    # Initial set of baby names and birth rates.
    names = ['Bob', 'Jessica', 'Mary', 'John', 'Mel']
    births = [968, 155, 77, 578, 973]
    # Merge name and birth lists into a single list of tuples (kind of a dict).
    BabyDataSet = list(zip(names, births))
    # Export the BabyDataSet into a DataFrame (similar to a SQL table).
    df = DataFrame(data = BabyDataSet, columns = ['Name', 'Births'])
    # Export the data frame into a CSV file (without and without headers).
    file_nh = 'dat_births_1880_without_header.csv'
    file_wh = 'dat_births_1880_with_header.csv'
    df.to_csv(file_nh, index = False, header = False)
    df.to_csv(file_wh, index = True, header = True)
    # Read data from the CSV file without headers and assign new labels.
    df_nh = pd.read_csv(file_nh, header = None, names = ['Anda', 'La_osa'])
    print('\nFrom file without labels:')
    print(df_nh)
    # Read data from the CSV file with headers.
    df_wh = pd.read_csv(file_wh, header = 0, index_col = 0)
    print('\nFrom file with labels:')
    print(df_wh)
    # Check columns data types.
    print('\nChecking the column data types:')
    print(df_wh.dtypes)
    # Find the name with the highest birthrate.
    print('\nFinding the name with the highest birthrate:')
    sort = df_wh.sort_values(['Births'], ascending = False)
    print(sort.head(1))     # <- Select the 1st row of the sorted data frame.
    print(sort[1:2])
    # Find the largest value within the 'Births' column of the original array.
    print('\nThe largest value within the column \'Births\' is:')
    print(df_wh['Births'].max())

def sample_csv_10k(in_file):
    # Setting field names.
    my_header = ['Client', 'Employee', 'Employee ID', 'Client balance',
        'Current sale', 'Client avg sales', 'Region', 'Industry',
        'Client grade']
    # Getting data from file.
    df = pd.read_csv(in_file, index_col = 0, header = None, names = my_header,
        encoding = 'latin2', sep = ',', quotechar = '\"')
    # Data frame summary.
    print('\nData frame summary')
    print(df.info())
    # Fields summary.
    print('\nField description')
    for field in my_header:
        print('\n')
        print(df[field].describe())
    # Group data by fields.
    print('\nGrouping information by fields')
    clients = df.groupby('Client')
    #print(clients.first())
    for name, group in clients:
        print('\n')
        print(name)
        print(group[['Region', 'Employee']])

def tut3_CreateDataSet(dat_file):
    Output = []
    Number = 4

    for i in range(Number):
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')
        # Create random data
        data = np.random.randint(low=25,high=1000,size=len(rng))
        # Status pool
        status = [1,2,3]
        # Make a random list of statuses
        random_status = [status[np.random.randint(low=0,high=len(status))]
            for i in range(len(rng))]
        # State pool
        states = ['GA','FL','fl','NY','NJ','TX']
        # Make a random list of states
        random_states = [states[np.random.randint(low=0,high=len(states))]
            for i in range(len(rng))]
        Output.extend(zip(random_states, random_status, data, rng))
    # Create data frame and export it into an excel file.
    df = pd.DataFrame(data = Output,
        columns = ['State', 'Status', 'CustomerCount', 'StatusDate'])
    df.to_excel(dat_file, index= False)

def tutorial_3():
    # Crate data set and print it into an excel file.
    np.random.seed(111)
    dat_file = 'dat_tutorial_3.xlsx'
    tut3_CreateDataSet(dat_file)
    # Read data from file.
    df = pd.read_excel(io = dat_file, header = 0, index_col = 'StatusDate')
    print(df.info())
    print(df.head())
    print(df.index)
    # How many different states there are?
    print(df['State'].unique())
    df.State = df.State.apply(lambda x: x.upper())
    print(df['State'].unique())
    # Select records with status 1 only (boolean vector method).
    mask = df['Status'] == 1
    df = df[mask]
    print(df)
    # Merge 'NJ' register with those of 'NY'.
    df.State[df.State == 'NJ'] = 'NY'
    print(df['State'].unique())
    #df.CustomerCount.plot(figsize = (15, 5))
    #plt.show()
    # Group data by State. However, the 'groupby' operation only takes column
    # arguments and, at this point 'StatusDate' is not a column of the data
    # frame but the index 'label'. Therefore we have to reincorporate it as a
    # normal column.
    df = df.reset_index()


def main():
    # in_file = check_input()
    # simple_commands()
    # sample_csv_10k(in_file)
    tutorial_3()

if __name__ == '__main__':
    # Importing specific functions.
    from pandas import DataFrame, read_csv
    from sys import argv
    # Importing libraries.
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    main()