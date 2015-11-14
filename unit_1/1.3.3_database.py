# Import modules needed to work with SQLite, pandas
import sqlite3 as lite, pandas as pd
db_name = 'getting_started.db'


'''
    Solution to Unit 1 Lesson 3 on Databases using SQLite, pysqlite and pandas
    Will need to add dynamic inputs using sys.argv and reading input options from stdin later.
'''

def database_challenge_solution(db_name):
    # Connect to the database
    con = lite.connect(db_name)

    # Definition of data for tables to be inserted via parameterized SQL
    cities = (('New York City', 'NY'),
                  ('Boston', 'MA'),
                  ('Chicago', 'IL'),
                  ('Miami', 'FL'),
                  ('Dallas', 'TX'),
                  ('Seattle', 'WA'),
                  ('Portland', 'OR'),
                  ('San Francisco', 'CA'),
                  ('Los Angeles', 'CA'),
                  ('Las Vegas', 'NV'),
                  ('Atlanta', 'GA'))

    weather = (('New York City', '2013','July', 'January', 62),
                   ('Boston', '2013', 'July', 'January', 59),
                   ('Chicago', '2013', 'July', 'January', 59),
                   ('Miami', '2013', 'August', 'January', 84),
                   ('Dallas', '2013', 'July', 'January', 77),
                   ('Seattle', '2013', 'July', 'January', 61),
                   ('Portland', '2013', 'July', 'December', 63),
                   ('San Francisco', '2013', 'September', 'December', 64),
                   ('Los Angeles', '2013', 'September', 'December', 75),
                   ('Las Vegas', '2013', 'July', 'December', 89),
                   ('Atlanta', '2013', 'July', 'January', 75))


    # Perform databases actions using a cursor
    with con:

        cur = con.cursor()

        # Drop existing table
        cur.execute("DROP TABLE IF EXISTS cities")
        cur.execute("DROP TABLE IF EXISTS weather")

        # Create tables
        cur.execute("CREATE TABLE cities (name text, state text)")
        cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")

        # Insert data into tables
        cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
        cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

        # Join weather and cities table on city names
        cur.execute("SELECT city, state, year, warm_month AS warm, cold_month AS cold, average_high  FROM cities LEFT OUTER JOIN  weather ON name=city WHERE  warm='July' ORDER BY average_high DESC")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=cols)

    print_output(df)

'''
    Print output to stdout
'''
def print_output(df):  
    # Print output
    print "The cities that are warmest in July are: ",
    for index, row in df.iterrows():
        if index < len(df.index) - 1:
            print "{}, {},".format(row['city'], row['state']),
        else:
            print "{}, {}".format(row['city'], row['state'])

if __name__ == '__main__':
    database_challenge_solution(db_name)
