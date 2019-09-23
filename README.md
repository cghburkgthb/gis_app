# gis_app
Geography Application
Below are the instructions to setup and execute the application on a PC, assuming a developer will be running the code.

PostgreSQL/PostGIS Database Setup
    Setup and test your PostgreSQL/PostGIS database. I found the following sites useful:
        https://www.postgresql.org/download/
        https://www.gpsfiledepot.com/tutorials/installing-and-setting-up-postgresql-with-postgis/
        https://www.bostongis.com/PrinterFriendly.aspx?content_name=postgis_tut01

    You will need to store the postgres user password in the gis_add.ini configuration file mentioned below.
  
Python 3.x Application Environment Setup
    Setup your Python application environment. You can setup Anaconda Python on your PC. Below
    is the site you can use to setup version 3.7 environment:
    https://www.anaconda.com/distribution/
    
    Add the psycopg2 package to you environment. You can use Anaconda Navigator to do the above.

    Below are some of the additional packages you need to add to the environment:
    https://anaconda.org/conda-forge/googlemaps
    conda install -c conda-forge googlemaps
    
    https://anaconda.org/conda-forge/flask-restful
    conda install -c conda-forge flask-restful

Obtaining Google Map API Key 
    Obtain your Google Map key by following the instructions at: https://developers.google.com/maps/documentation/javascript/get-api-key. 

    You will need to store your key in the gis_app.ini file mentioned below.

Data File Download
    Download the 2019 census state geography shapefile & related files from the location below: https://www2.census.gov/geo/tiger/TIGER2019/STATE/
    
    Unzip and store the files within the "data" folder in your application root directory: <app_root>/data.

Application Execution Instructions
    Activate the Python environment that you created from Anaconda Prompt terminal by entering the following command:
    conda activate <python_env_nm>  (e.g., conda activate gis_app)
    
gis_app.ini -- replace the place holders (e.g., <password>) with your own PostgreSQL database and Google Map credentials.

create_gis_tables.py -- execute this script in order to create the target database: gis and table: us_state and related index.

load_gis_data.py -- run this script to load the staging table: us_state_stg and target table: us_state.
lookup_state.py -- execute this script to start Flask Web server.

test_gis_addr.py -- from a different Anaconda Prompt terminal window, activate your Python environment and run this script to display the state name associated with a few addresses.

Additional Street Addresses
    You might use the Web site below to generate random addresses and use them in the script: test_gis_addr.py
    https://www.bestrandoms.com/random-address
