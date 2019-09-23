# create_gis_tables.py

import psycopg2
from config import config
from sql_gis_queries import create_tbl_queries, drop_tbl_queries


def create_database():
    """
    Create GIS database
 
    Returns:
        (DB cursor) cur - cursor of open DB connection where tables exist
        (DB connection) conn - open database where the tables exist
    """
    
    print("Reading database connection parameters")
    db_logon = config('gis_app.ini', 'postgredb')
    gis_db_logon = config('gis_app.ini', 'gisdbload')
    
    gis_db = gis_db_logon['database']
    
    print("Creating database: {}".format(gis_db))
    try:
        conn = psycopg2.connect(**db_logon)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
    
        # create GIS database with UTF8 encoding
        
        query = 'DROP DATABASE IF EXISTS ' + gis_db
        cur.execute(query)
        
        query = 'CREATE DATABASE ' + gis_db + " WITH ENCODING 'utf8' TEMPLATE template0"
        cur.execute(query)
    
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return('None', 'None')
    
    print("Adding GIS database extensions: postgis and postgis_topology")
    try:
        conn = psycopg2.connect(**gis_db_logon)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        
        cur.execute("CREATE EXTENSION postgis;")
        cur.execute("CREATE EXTENSION postgis_topology;")
        
        # close connection to default database
        # conn.close()    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return('None', 'None')
    
    return cur, conn


def create_tables(cur, conn, tgt_tbl_nm):
    """
    Create the tables and indexes.
    
    Args:
        (DB cursor) cur - cursor of open DB connection where tables exist
        (DB connection) conn - open database where the tables exist

    Returns:
        N/A
    """
    
    print("Creating target table: ", tgt_tbl_nm)
    for query in create_tbl_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as error: 
            print("Error: creating table: ",  query)
            print (error)
            return(1)
            
    return(0)

def main():
    """
    Manage the application flow
    
    Returns:
        (int) exit_cd exit status code
    """
    
    cur, conn = create_database()
    if cur != 'None':
        sts_cd = create_tables(cur, conn, 'us_state')
       
    conn.close()
    if sts_cd != 0:
        exit(1)

    exit(0)
    
if __name__ == "__main__":
    main()