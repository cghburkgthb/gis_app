# load_data.py

import psycopg2
from config import config
import shlex
import subprocess
import os
from sql_gis_queries import load_tbl_queries, us_state_stg_tbl_drop

def load_stg_tbl(data_path, src_srid, tgt_srid, db_nm, stg_tbl):
    """
    load shapefile file data into staging table

    Args:
        (str) data_path  - directory and name of state shapefile and releated files
        (str) db_nm - name of GIS database
        (numeric) src_srid - shapefile srid
        (numeric) tgt_srid - SRID of the GIS tables geography columns
        (str) stg_tbl - stage table name where to load shapefile data
    
    Returns:
        (int) sts_cd - state code 1 (error) or 0 (success)
    """
    print("Loading data file: {0} into table {1}.{2}".format(data_path, db_nm, stg_tbl))
    try:
        
        psql_script_path = os.path.dirname(data_path)
        psql_script_path += '/' + stg_tbl + '.sql'
      
        print('Creating SQL file: ', psql_script_path)
        
        fstream = open(psql_script_path, "w")
        cmd = 'shp2pgsql -g geog -s ' + src_srid + ':' + tgt_srid + ' ' 
        cmd +=  data_path + ' ' + stg_tbl + ' -T'
        print('cmd: ', cmd)
        
        results = subprocess.run(shlex.split(cmd), stdout=fstream)
        fstream.close()     
    except subprocess.CalledProcessError as error:
        print(error)
        return(1)

    try:
        print("Loading staging table: {} using SQL file: {}".format(stg_tbl, psql_script_path))
        
        # localhost is trusted; thus psql is running w/o specifying password
        cmd = 'psql -h localhost -d ' + db_nm + ' -U postgres -f '
        cmd += psql_script_path
        #print('cmd: ', cmd)
        
        results = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as error:
        print(error)
        return(1)
 
    return(0)
    
    
def load_tgt_tbl(cur, conn, tgt_tbl_nm):
    """
    Load target table, after deleting the records from it.
    
    Args:
        (DB cursor) cur - cursor of open DB connection where tables exist
        (DB connection) conn - open database where the tables exist

    Returns:
        N/A
    """
    print('Loading target table: ', tgt_tbl_nm)
    for query in load_tbl_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as error: 
            print("Error: loading table: ",  query)
            print (error)
            return(1)
            
    return(0)

            
def main():
    """
    Load target table, after loading staging table. Drop staging table before
    loading it and delete records from target before loading it.
    
    Returns:
        (int) exit_cd exit status code
    """
    
    gis_db_logon = config('gis_app.ini', 'gisdbload')
    try:
        conn = psycopg2.connect(**gis_db_logon)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    # Drop stage table, before loading it. The data file  will contains an SQL
    # statement at the beginning of it that will create the table.
    try:
        cur.execute(us_state_stg_tbl_drop)
        conn.commit()
    except psycopg2.Error as error: 
        print("Error: dropping staging table: ",  us_state_stg_tbl_drop)
        print (error)
        exit(1)
    
    gis_db_nm = gis_db_logon['database']
    stg_tbl_nm = 'us_state_stg'
    
    data_file_info = config('gis_app.ini', 'datainfo')
    
    data_file_nm_prfx = data_file_info['datafnmprfx']
    data_path = 'data/' + data_file_nm_prfx
    
    src_srid, tgt_srid = data_file_info['src_srid'], data_file_info['tgt_srid']
    
    sts_cd = load_stg_tbl(data_path, src_srid, tgt_srid, gis_db_nm, stg_tbl_nm)
    
    if sts_cd != 0:
        exit(1)
    
    sts_cd = load_tgt_tbl(cur, conn, 'us_state')
    exit(sts_cd)
    
if __name__ == '__main__':
    main()
    
