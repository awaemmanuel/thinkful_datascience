#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Work done for Unit 2 Lesson 1 on Statistics.

import pandas as pd, sys
from scipy import stats

''' 
    Clean data
'''
def clean_data(text):
    text = text.splitlines()
    return [i.strip().split(',') for i in text]


'''
    Build DataFrame from clean data
'''
def build_dataframe(data):
    column_names = data[0] # First line based on data definition above
    rows = data[1::]
    return pd.DataFrame(rows, columns=column_names)

'''
    Change Data Frame data type definition.
    Float's needed for stats calculation.
'''
def change_column_datatype(data_frame, column_name, new_type = float):
    data_frame[column_name] = data_frame[column_name].astype(new_type)
    
'''
    Calculate Mean 
'''   
def calc_mean(data_frame, column_name):
    return data_frame[column_name].mean()

    
'''
    Calculate Median 
''' 
def calc_median(data_frame, column_name):
    return data_frame[column_name].median()

    
'''
    Calculate Mode 
''' 
def calc_mode(data_frame, column_name):
    return stats.mode(data_frame[column_name]).mode[0]

    
'''
    Calculate Range 
''' 
def calc_range(data_frame, column_name):
    return max(data_frame[column_name]) - min(data_frame[column_name])

'''
    Calculate Variance
'''
def calc_variance(data_frame, column_name):
    return data_frame[column_name].var()


'''
    Calculate Standard Deviation
'''
def calc_std(data_frame, column_name):
    return data_frame[column_name].std()


'''
    Output to screen and flush buffer
'''
def print_out(str):
    print str
    sys.stdout.flush()

'''
    Solution
'''
def process_stats():
    
    # Data Entry definition
    data = '''Region,Alcohol,Tobacco
    North,6.47,4.03
    Yorkshire,6.13,3.76
    Northeast,6.19,3.77
    East Midlands,4.89,3.34
    West Midlands,5.63,3.47
    East Anglia,4.52,2.92
    Southeast,5.89,3.20
    Southwest,4.79,2.71
    Wales,5.27,3.53
    Scotland,6.08,4.51
    Northern Ireland,4.02,4.56'''
    
    cleaned_data = clean_data(data)
    df = build_dataframe(cleaned_data)
    
    print_out('=' * 50)
    print_out('Data Frame built!\n {}'.format(df))
    
    cols = list(df.columns[1:3])
    for col in cols:
        
        print_out("=" * 50)
        change_column_datatype(df, col) # Change from str to float
        print_out("The range for the {} dataset is: \t{}".format(col, calc_range(df, col)))
        print_out("The mean for the {} dataset is: \t{}".format(col, calc_mean(df, col)))
        print_out("The median for the {} dataset is: \t{}".format(col, calc_median(df, col)))
        print_out("The mode for the {} dataset is: \t{}".format(col,calc_mode(df, col)))
        print_out("The variance for the {} dataset is: {}".format(col,calc_variance(df, col)))
        print_out("The standard deviation for the {} dataset is: {}".format(col,calc_std(df, col)))
        
    
    
    
if __name__ == '__main__':
    process_stats()
    
    
    
    
    