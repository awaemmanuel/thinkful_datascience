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

# Spining terminal cursor
from helper_modules import spinning_cursor, utility_functions as uf


# Weather api key
api_key = '0c418987d4da9f81100361e0141d5af6'

################### UTILITY FUNCTIONS ##########################
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



# Get the daily weather data
def get_daily_temp_data(req):
    return req.json()['daily']


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
        cur.execute("CREATE TABLE IF NOT EXISTS cities_max_temperature ( date INT PRIMARY KEY, " +  ", ".join(formatted_city_names) + ");")



def insert_max_temp_to_db():
    return False

# Params ==> 'long,lat,time'
def download_weather_data(query_params, api_key='0c418987d4da9f81100361e0141d5af6'): 
    return rq.get('{}/{}/{}'.format('https://api.forecast.io/forecast', api_key, query_params))

                  
if __name__ == "__main__":
    create_tables()
                  
# https://api.forecast.io/forecast/0c418987d4da9f81100361e0141d5af6/42.331960,-71.020173,2015-12-30T09:40:02