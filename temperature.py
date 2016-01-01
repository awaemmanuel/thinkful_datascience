import sqlite3 as lite
import time # datetime objects
import collections
import matplotlib.pyplot as plt
import requests as rq
import pandas as pd
from scipy import stats
import time
from pandas.io.json import json_normalize
from dateutil.parser import parse # parse string into Python datetime object
import itertools
import datetime
import pytz
import sys

# Spining terminal cursor
from helper_modules import spinning_cursor, utility_functions as uf


# Weather api key
api_key = '0c418987d4da9f81100361e0141d5af6'
url = 'https://api.forecast.io/forecast'

################### UTILITY FUNCTIONS ##########################
# Params ==> 'long,lat,time'
def download_weather_data(url, query_params, api_key='0c418987d4da9f81100361e0141d5af6'): 
    return rq.get('{}/{}/{}'.format(url, api_key, query_params))

# Connect to DB
def connect_db():
    # Connect to the database
    return lite.connect('weather.db')


class _Const(object):
    @uf.constant
    def CITIES_AND_LOCATION():
        return { 
            "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435' }

'''
    Parse the execution time to update the database
    Because of dst and timezone issues, we need to synchronize
    the times to utc before updating database for the cities on 
    the same day.
'''
def sync_daily_time_to_utc(req): 
    timezone_str = get_timezone(req)
    time_stamp = get_daily_time(req)
    local_time = pytz.timezone (timezone_str)
    time_obj = datetime.datetime.fromtimestamp(int(time_stamp))
    local_dt = local_time.localize(time_obj, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return datetime.datetime.strptime(utc_dt.strftime('%Y-%m-%d'), "%Y-%m-%d").strftime('%s')


# Get the daily weather data
def get_daily_temp_data(req):
    return req.json()['daily']

# Get the max daily weather data
def get_daily_time_and_maxtemp(req):
    return (sync_daily_time_to_utc(req), get_daily_maxtemp(req)) # time and max temp

# Get the time of daily data response before utc sync
def get_daily_time(req):
    daily_data = get_daily_temp_data(req)
    return daily_data['data'][0]['time']

# Get the daily max temperature
def get_daily_maxtemp(req):
    daily_data = get_daily_temp_data(req)
    return daily_data['data'][0]['temperatureMax']

# Get data timezone
def get_timezone(req):
    return req.json()['timezone']


# Format cities names to be used for db column creation
def db_format_city_names():
    CONST = _Const()
    locations = CONST.CITIES_AND_LOCATION
    return [str(city) + " NUMERIC" for city in locations.keys()]

'''
    Take the semi-structured json and flatten it to a dataframe table
    would also work with straight DataFrame passing the json column as arg.
''' 
def normalized_daily_weather_data(req):
    return json_normalize(get_daily_temp_data(req)) # returns a df with the daily weather data

def create_tables():
    con = connect_db()
    cur = con.cursor()
    formatted_city_names = db_format_city_names()
    
    with con:
        # Create city to maximum temperature by dates
        cur.execute("DROP TABLE IF EXISTS cities_max_temperature")
        cur.execute("CREATE TABLE IF NOT EXISTS cities_max_temperature ( date INT PRIMARY KEY, " +  ", ".join(formatted_city_names) + ");")
        
'''
    Update table with exec_time and max temperature for city.
'''


def insert_max_temp_to_db():
    con = connect_db()
    cur = con.cursor()
    global url
    
    CONST = _Const()
    cityname_and_location = CONST.CITIES_AND_LOCATION
    
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days = 30)
    
    # Update table with daily max temperatures
    for idx in xrange(31): # 30 Days starting from day 0
        for city_idx, key in enumerate(cityname_and_location):
            # Get longitude and latitude ==> key is the city name
            long_lat = cityname_and_location[key]
            query_params = long_lat + ',' + (start_date + datetime.timedelta(days = idx)).strftime('%Y-%m-%dT%H:%M:%S')

            # Download data
            req = download_weather_data(url, query_params)

            # Process data
            exec_time, temp = get_daily_time_and_maxtemp(req)

            print "Day: {}  PROCESSING ==> {}. Max temperature {}".format(idx, key, temp)

            with con:
                # Insert exec_time for the run only, for each row.
                if city_idx == 0:
                    cur.execute('INSERT INTO cities_max_temperature (date) VALUES (?)', (exec_time,) )
                    
                # Update DB
                cur.execute('UPDATE cities_max_temperature SET {} = {} WHERE date = {} ;'.format(key, temp, exec_time))
        
        # Demarcation.
        print "=" * 80

# Plot and save histogram of a column
def plot_and_save_hist(df, column_name, output_dir, fig_name, output_format, fig_no = 0):
    path_to_fig = str(output_dir) + '/' + str(fig_name)
    print "     ==> Saving {}_{}.{} for run: {}".format(path_to_fig, fig_no, output_format, fig_no)
    plt.figure()
    df[column_name].hist()
    plt.savefig("{}_{}.{}".format(path_to_fig, fig_no, output_format))
    plt.clf()
    

# Analysis
def get_maxtemps_from_db():
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    with con:
        df = pd.read_sql_query('SELECT * FROM cities_max_temperature ORDER BY date', con, index_col = 'date')   
    return df


# DATA ANALYSIS
def data_analysis():
    df = get_maxtemps_from_db()
    daily_change = collections.defaultdict(str)
    
    # Connect to the database
    con = connect_db()
    cur = con.cursor()
    
    for col in df.columns:    
        city_vals = df[col].tolist()
        city_name = col
        temp_change = 0
        for k,v in enumerate(city_vals):
            if k < len(city_vals) - 1:
                temp_change += abs(city_vals[k] - city_vals[k+1])
        daily_change[city_name] = temp_change 
        
        print "MEAN: ", df[col].mean()
        print "MODE: ", stats.mode(df[col]).mode[0]
        print "VARIANCE: ", df[col].var()
        print "RANGE: ", max(df[col]) - min(df[col])
        plot_and_save_hist(df, col, 'figures/weather', '{}_histplot'.format(col), 'png')
        
    # city with max change in temperature
    city_max_temp = uf.keywithmaxval(daily_change)
    
    print "City with max temp", city_max_temp
    
    print("The city with the most changes in temperature is: {} with max temperature of {}".format(city_max_temp, df[city_max_temp].max()))


# DATA INGESTION
def data_ingestion():
    try:
        create_tables()
        insert_max_temp_to_db()
    except Exception:
        raise Exception('Something went wrong with Database connection.')
        
    
                  
if __name__ == "__main__":
    data_ingestion()
    
    data_analysis()
   
# Sample api call
# https://api.forecast.io/forecast/0c418987d4da9f81100361e0141d5af6/42.331960,-71.020173,2015-12-30T09:40:02