# lookup_state.py

import googlemaps
import psycopg2
from config import config
from sql_gis_queries import *
from flask import Flask, request #import main Flask class and request object
import datetime as dt

app = Flask(__name__) #create the Flask app

@app.route('/addr', methods=['POST'])
def find_state():
    """
    find the name of the state for the street address sent to this service
    
    Returns:
        (str) state_nm - name of the state
    """
    
    print("{} Retrieving street address".format(dt.datetime.now()))
    
    request_data=request.get_json()
    street_address = request_data['addr']
    
    print("{} street_address: {}".format(dt.datetime.now(), street_address))
    
    print("{} Reading application configuration".format(dt.datetime.now()))
    
    # read database connection parameters
    db_logon = config('gis_app.ini', 'gisdbread')
    
    # read Google Map key
    google_map = config('gis_app.ini', 'googlemap')
    addr_loc_lkp = googlemaps.Client(key=google_map['key'])
        
    print("{} Retrieving long/lat from GoogleMap Service".format(dt.datetime.now()))
        
    geocode_result = addr_loc_lkp.geocode(street_address)
    location = geocode_result[0]['geometry']['location']
    addr_geo_loc = ','.join([str(location['lng']), str(location['lat'])])
    
    print("{} Retrieving state name from GIS database".format(dt.datetime.now()))
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**db_logon)
        cur = conn.cursor()
        
        # retrieving state
        sel_st_nm_qry = state_nm_tmplt_sel.replace('LOCATION_TKN', addr_geo_loc)
        cur.execute(sel_st_nm_qry)
        
        state_nm = {}
        state_nm = cur.fetchone()
 
       # close the communication with the PostgreSQL
        cur.close()
    except psycopg2.Error as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    print("{} Returning state name".format(dt.datetime.now()))
    return(state_nm[0])
    
   
if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000