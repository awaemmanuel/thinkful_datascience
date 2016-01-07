'''
    Analysis of Educational Attainment with GDP
'''
import csv
import matplotlib.pyplot as plt
import requests as rq
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


from helper_modules import utility_functions as uf, spinning_cursor as sc

# Create table for education data
def create_table_education():
    con = uf.connect_db('scrappd_education_data.db')
    cur = con.cursor()
    with con:
        cur.execute("DROP TABLE IF EXISTS education_life_info")
        cur.execute("CREATE TABLE education_life_info (Country TEXT PRIMARY KEY, \
        Year INT, Total_School_Time INT,  Male_Expectancy INT, Female_Expectancy INT);")
        
# Create table gdp
def create_table_gdp():
    con = uf.connect_db('scrappd_education_data.db')
    cur = con.cursor() 
    with con:
        cur.execute("DROP TABLE IF EXISTS worldbank_gdp_data")
        cur.execute('CREATE TABLE worldbank_gdp_data (Country REAL,\
        GDP_1999 NUMERIC, GDP_2000 NUMERIC, GDP_2001 NUMERIC, GDP_2002 \
        NUMERIC, GDP_2003 NUMERIC, GDP_2004 NUMERIC, GDP_2005 NUMERIC, \
        GDP_2006 NUMERIC, GDP_2007 NUMERIC, GDP_2008 NUMERIC, GDP_2009 \
        NUMERIC, GDP_2010 NUMERIC);')
        
# Download data
def download_data_education():
    # Data URL
    return rq.get('http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm')

# Get Soup of data
def get_beautiful_soup_data(req):
    req = download_data_education()
    return BeautifulSoup(req.content, "html.parser")

# Get relevant tabled data
def get_cleaned_data_from_table(soup):
    all_data = soup('table')[6].findAll('tr', 'tcont')
    clean_data = [d for d in all_data if len(d) == 25] # len of empty field is 7 and filled 25
    return clean_data

# Build DataFrame education
def build_dataframe_education(clean_data_list):
    result = []
    for row in clean_data_list:
        column = row.find_all('td')
        country = column[0].string
        year = column[1].string
        total = column[4].string
        men = column[7].string
        women = column[10].string
        result.append([country, year, total, men, women]) # A record/row in the dataframe
    
    # Create and clean DF
    cols = ['Country', 'Year', 'Total_School_Time', 'Men_School_Time', 'Women_School_Time']
    df = pd.DataFrame(result, columns=cols)
    df = df.dropna(axis=1, how="all")
    return df

# Insert data into database
def bulk_insert_into_db_education(df):
    con = uf.connect_db('scrappd_education_data.db')
    cur = con.cursor()
    
    # Prepared SQL
    sql = "INSERT INTO education_life_info (Country, Year, \
    Total_School_Time, Male_Expectancy, Female_Expectancy) VALUES (?,?,?,?,?)" 
    with con:
        for row in df.values:
            cur.execute(sql, (row[0], row[1], row[2], row[3], row[4]))

# Get relevant csv columns indexes
def get_csv_column_idx(csv_headers, min_year, max_year):
    str_min_year = uf.stringify_text(min_year)
    str_max_year = uf.stringify_text(max_year)
    country_field = uf.stringify_text('Country Name')
    header_list = csv_headers.split(',')
    col_indexes = {}
    for idx, val in enumerate(header_list):
        if val == country_field or val == str_min_year or val == str_max_year:
            col_indexes[val] = idx      
    return col_indexes

# Insert data into gdp database
def bulk_insert_into_db_gdb(min_year, max_year):
    con = uf.connect_db('scrappd_education_data.db')
    cur = con.cursor()  
    with open('world_bank_gdp_data/9612cab5-6177-41d5-a04f-55d22c4169b7_v2.csv') as input_file:
        # skip the first four irrelevant lines
        next(input_file) 
        next(input_file)
        next(input_file)
        next(input_file)
        
        # Get csv header and parse information to return relevant column names to the db
        header = next(input_file)
        col_indexes = get_csv_column_idx(header, min_year, max_year)
        country_idx = col_indexes['"Country Name"']
        min_year_idx = col_indexes[uf.stringify_text(min_year)]
        max_year_idx = col_indexes[uf.stringify_text(max_year)]
        
        # Get a csv reader to parse csv text properly
        input_reader = csv.reader(input_file)
        for line in input_reader:
            if line:
                with con:
                    cur.execute('INSERT INTO worldbank_gdp_data \
                    (Country, GDP_1999, GDP_2000, GDP_2001, \
                    GDP_2002, GDP_2003, GDP_2004, GDP_2005, \
                    GDP_2006, GDP_2007, GDP_2008, GDP_2009, GDP_2010) \
                    VALUES ("' + line[country_idx] + '","' + \
                                '","'.join(line[min_year_idx : (max_year_idx + 1)]) + '");')

                    
# Ingest the UN Data and produce a DataFrame, after inserting into database.
def data_ingestion_education_info():
    print "[Ingesting Education data] ==> Begin"
    
    create_table_education()
    req = download_data_education()
    soup = get_beautiful_soup_data(req)
    clean_data = get_cleaned_data_from_table(soup)
    df = build_dataframe_education(clean_data)
    bulk_insert_into_db_education(df)
    
    print "[Ingesting Education data] ==> End"
    
    # Tuple of data needed to correlate with gdp information
    return (df, df.Year.min(), df.Year.max())
    

# Ingest the world bank GDP information, specifying what year range to analyze
def data_ingestion_worldbank_gdp_info(min_year, max_year):
    print "[Ingesting World bank GDP data] ==> Begin"
    
    create_table_gdp()
    bulk_insert_into_db_gdb(min_year, max_year)
    
    print "[Ingesting World bank GDP data] ==> End"
    
    
# Build DataFrame - world bankd gdp
def build_dataframe_gdp():
    # Connect to database
    con = uf.connect_db('scrappd_education_data.db')
    with con:
        # Get data out from the database
        df_gdb = pd.read_sql_query("SELECT * FROM worldbank_gdp_data", con)
    # Clean up null rows - drop features with no values i.e all rows where all columns are empty
    df_gdb = df_gdb.dropna(axis=1, how="all")
    return df_gdb
        
# Analysis and Correlation education data with gdp
def data_analysis_and_correlation(df_education, df_gdp):
    print "[Data Analysis and Correlation of Education to GDP data] ==> Begin"
    
    # Find set of common countries
    set_edu = set(df_education['Country'].tolist())
    set_gdp = set(df_gdp['Country'].tolist())
    list_common_countries = list(set_edu & set_gdp)
    

    gdp = []
    Total_School_Time = []
    Men_School_Time = []
    Women_School_Time = []
    for cntry in list_common_countries:
        df1 = df_education[df_education['Country'] == cntry]
        df2 = df_gdp[df_gdp['Country'] == cntry]
        
        if df2['GDP_'+ df1['Year'].iloc[0]].iloc[0] != '':
            Total_School_Time.append(int(df1['Total_School_Time'].iloc[0]))
            Men_School_Time.append(int(df1['Men_School_Time'].iloc[0]))
            Women_School_Time.append(int(df1['Women_School_Time'].iloc[0]))
            gdp.append(np.log(df2['GDP_'+ df1['Year'].iloc[0]].iloc[0]))

    df_edu_to_gdp = pd.DataFrame({'Total': Total_School_Time, 'Men': Men_School_Time, \
                                  'Women': Women_School_Time, 'GDP': gdp})    

    # Print Correlation Matrix
    print df_edu_to_gdp.corr()
    
    # Scatter matrix plot with histogram of data plots in the diagonal
    pd.scatter_matrix(df_edu_to_gdp, alpha=0.05, figsize=(10, 10), diagonal='hist')
    plt.savefig('figures/education_to_gdp/data_education_gdp_analysis.png')
    plt.clf()

    
    '''
         ==> Conclusion / Summary
                    GDP       Men     Total     Women
        GDP    1.000000  0.495794  0.479050  0.497923
        Men    0.495794  1.000000  0.971663  0.942572
        Total  0.479050  0.971663  1.000000  0.977217
        Women  0.497923  0.942572  0.977217  1.000000
    '''
    
    print """
    FINAL ANALYSIS: 
    We observe a weak correlation between education attainment and GDP.
    The correlation coefficients are closer to 0 than 1.
    This shows there is a greater scatter of the data points from the fitted line.
    At this point we cannot not conclude any direct relationship.  
    """
    
    print "[Data Analysis and Correlation of Education to GDP data] ==> End"

############# RUN MAIN ##########################
if __name__ == '__main__':
    df_education, min_year, max_year = data_ingestion_education_info()
    sc.spinning_cursor(3)
    
    data_ingestion_worldbank_gdp_info(min_year, max_year)
    sc.spinning_cursor(3)
    
    df_gdp = build_dataframe_gdp()
    sc.spinning_cursor(3)
    
    data_analysis_and_correlation(df_education, df_gdp)
    sc.spinning_cursor(3)
    



