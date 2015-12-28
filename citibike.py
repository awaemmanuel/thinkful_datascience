import sqlite3 as lite
import time # datetime objects
import collections
import matplotlib.pyplot as plt
import requests as rq
import pandas as pd
import time
from pandas.io.json import json_normalize
from dateutil.parser import parse # parse string into Python datetime object
import itertools
import datetime
import sys


####### HELPER FUNCTIONS ###########

# Download bike data
def download_bike_data():
    return rq.get('http://www.citibikenyc.com/stations/json')


# As database columns cannot start with a number we normalize it by prefixing an underscore
def process_station_ids(df_ids):
    station_ids = df_ids.tolist() # df['id']
    
    #add the '_' to the station name and also add the data type for SQLite
    return ['_' + str(x) + ' INT' for x in station_ids]

'''
    Parse the execution time to update the database
'''
def process_exec_time(exec_time):
    # Parse the execution time to something the DB would be able to interprete
    return exec_time.strftime('%s')

'''
    Extraction execution time from json file
'''
def get_execution_time(req):
    return parse(req.json()['executionTime'])

# Process available bikes by station id
def create_station_to_bike_dic(stationList_json):
    # Dictionary to store available bikes by station
    id_bikes = collections.defaultdict(int) 
    
    for station in stationList_json: # req.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']
    
    return id_bikes

# Plot and save histogram of a column
def plot_and_save_hist(df, column_name, output_dir, fig_name, output_format, fig_no = 0):
    path_to_fig = str(output_dir) + '/' + str(fig_name)
    print "     ==> Saving {}_{}.{} for run: {}".format(path_to_fig, fig_no, output_format, fig_no)
    plt.figure()
    df[column_name].hist()
    plt.savefig("{}_{}.{}".format(path_to_fig, fig_no, output_format))
    plt.clf()

# Connect to DB
def connect_db():
    # Connect to the database
    return lite.connect('citi_bike.db')
    

'''
    Terminal spinning cursor simulator
'''
def spinning_cursor(time_to_wait):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    for _ in range(time_to_wait):
        sys.stdout.write(spinner.next())
        sys.stdout.flush()
        time.sleep(1)
        sys.stdout.write('\b')

######### MAIN FUNCTIONS #################

'''
    Return the Station Bean List json data object
'''
def get_stationlist_info_json(req):
    return req.json()['stationBeanList']

'''
    Return the station bean list column names
'''
def get_stationdata_keylist(req):
    return req.json()['stationBeanList'][0].keys()

'''
    Return the citibike data keys to observe data
'''
def get_citibike_data_keys(req):
    return req.json().keys() # [u'executionTime', u'stationBeanList']
    
'''
    Normalize the Station Bean List
'''
def normalized_stationbean_data(req):
    '''
        Take the semi-structured json and flatten it to a dataframe table
        would also work with straight DataFrame passing the json column as arg.
    ''' 
    return json_normalize(get_stationlist_info_json(req)) # returns a df with the station bean list

'''
    Output informational keys in the data
'''
def output_data_keys(req):
    # Set the keys of the data
    print "Citibike data keys: \n", get_citibike_data_keys(req)

    # Get the column names for our database
    print "Station Data columns: \n", get_stationdata_keylist(req)
    

'''
    Create Reference and changing tables.
'''
def create_tables(df_ids):
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    station_ids = process_station_ids(df_ids)
    
    # Create table citibike_reference
    with con:
        # Drop existing tables
        cur.execute("DROP TABLE IF EXISTS citibike_reference")
        cur.execute("DROP TABLE IF EXISTS available_bikes")
        
        # Create reference and changing tables table
        cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress1 TEXT, stAddress2 TEXT, longitude NUMERIC, latitude NUMERIC, postalCode TEXT, testStation TEXT, stationName TEXT, landMark TEXT, location TEXT )')
        
        cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")



'''
    Bulk insert into citibike reference table.
'''
def bulk_insert_citibike_ref_table():
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    #a prepared SQL statement we're going to execute over and over again
    sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress1, stAddress2, longitude, latitude, postalCode, testStation, stationName, landMark, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

    #for loop to populate values in the database
    with con:
        for station in req.json()['stationBeanList']:
            cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress1'],station['stAddress2'],station['longitude'],station['latitude'],station['postalCode'],station['testStation'],station['stationName'],station['landMark'],station['location']))
        

'''
    Bulk insert into changing available bikes table
'''
def insert_update_available_bike_table(exec_time, station_bean_list):
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    # Get stationlist dictionary of ids to available bikes
    id_bikes = create_station_to_bike_dic(station_bean_list)
    
    # Insert execution time and then iterate through the defaultdict to update the values in the database
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (process_exec_time(exec_time),))
        for key, value in id_bikes.iteritems():
            cur.execute('UPDATE available_bikes SET _' + str(key) + '=' + str(value) + ' WHERE execution_time = ' + process_exec_time(exec_time) + ';')

            
# Analysis
def get_available_bikes_from_db():
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    with con:
        df = pd.read_sql_query('SELECT * FROM available_bikes ORDER BY execution_time', con, index_col = 'execution_time')
        
    return df
# Find the key with the greatest value
def keywithmaxval(d):
    return max(d, key=lambda k: d[k])
    
if __name__ == '__main__':
    
    '''
        DATA INGESTION AND ACQUISITION
    '''
    # Create/Update database for one hour time window with 1 minute intervals.
    for idx in xrange(1, 61):

        # Download data
        req = download_bike_data()

        # Normalize Station List data
        df_stationlist = normalized_stationbean_data(req)

        # json data
        json_stationlist = get_stationlist_info_json(req)

        # Get execution time
        exec_time = get_execution_time(req)

        ''' Run inserts and updates '''
        
        # Create tables and bulk insert into reference table once.
        if idx == 1:
            output_data_keys(req) # For information purposes alone.
            create_tables(df_stationlist['id'])
            bulk_insert_citibike_ref_table()
            
        insert_update_available_bike_table(exec_time, json_stationlist)
        
        # Simple plots to observe data
        print "PLOT AND SAVE IMAGES FOR RUN: {}".format(idx)
        plot_and_save_hist(df_stationlist, 'availableBikes', 'figures/citibike', 'available_bikes', 'png', idx)
        plot_and_save_hist(df_stationlist, 'totalDocks', 'figures/citibike', 'total_docks', 'png', idx)
        plot_and_save_hist(df_stationlist, 'testStation', 'figures/citibike', 'test_station', 'png', idx)

        
        # Spinning cursor to wait for 60 seconds.
        spinning_cursor(60)
        
    '''
        ANALYSIS PART
    '''
    df = get_available_bikes_from_db()
    
    hour_change = collections.defaultdict(int)
    for col in df.columns:
        station_vals = df[col].tolist()
        station_id = col[1:] #trim the "_"
        station_change = 0
        for k,v in enumerate(station_vals):
            if k < len(station_vals) - 1:
                station_change += abs(station_vals[k] - station_vals[k+1])
        hour_change[int(station_id)] = station_change #convert the station id back to integer
        
    # assign the max key to max_station
    max_station = keywithmaxval(hour_change)

    
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    #query sqlite for reference information
    cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
    data = cur.fetchone()
    print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
    print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
))
    
    # Plot Data
    plt.bar(hour_change.keys(), hour_change.values())
    plt.savefig('hour_change.png')
    plt.clf()