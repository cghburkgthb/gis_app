# Geography Application

## Content
- Summary
- PostgreSQL/PostGIS Database Setup
- Python 3.x Application Environment Setup
- Obtaining Google Map API Key
- Downloading Source Data File 
- Application Execution Instructions
- Adding Additional Street Addresses

## Summary

This application accept an US street address, lookup it's longitude and latitude using Google Map API. It then uses the above location information to lookup the state name for the address using a PostgreSQL/PostGIS database.

This application will run in debug mode and should not be executed in a production environment.

Below are the instructions to setup and execute the application on a PC, assuming a developer will be running the code.

## PostgreSQL/PostGIS Database Setup
    
Setup and test your PostgreSQL/PostGIS database. I found the following sites useful:
- https://www.postgresql.org/download/
- https://www.gpsfiledepot.com/tutorials/installing-and-setting-up-postgresql-with-postgis/
- https://www.bostongis.com/PrinterFriendly.aspx?content_name=postgis_tut01

You will need to store the postgres user password in the gis_add.ini configuration file mentioned below.
  
## Python 3.x Application Virtual Environment Setup

You can setup Anaconda Python on your PC. Below is the site you can use to setup version 3.7 environment: https://www.anaconda.com/distribution/

Then create a virtual application environment called "gis_app" using Anaconda Navigator. Your can find Navigator within the Anaconda program folder in the Start Menu, assuming you are using Windows 7, 8 or 10.

Select Environments then click the create button located at the bottom of the center panel. 

From Navigator, add the psycopg2 package to you environment. On the 3rd panel change Installed to Not Installed. Then scroll down to find and click the selection box next to psycopg2. To install this package, click the "Apply" button in the lower, right hand corner.

Below are some of the additional packages you need to add to the environment:
- https://anaconda.org/conda-forge/googlemaps
- conda install -c conda-forge googlemaps
    
- https://anaconda.org/conda-forge/flask-restful
- conda install -c conda-forge flask-restful

## Obtaining Google Map API Key

Obtain your Google Map API key by following the instructions at the site below: 

- https://developers.google.com/maps/documentation/javascript/get-api-key. 

You will need to store your key in the gis_app.ini file mentioned below.

## Creating Application Root Directory

Create the application root directory "gis_app" within your development folder.

## Downloading Source Data File

Download the 2019 census state geography shapefile & related files from the location below:

- https://www2.census.gov/geo/tiger/TIGER2019/STATE/
    
Extract and store the files within the "data" folder in the application directory: ../gis_app/data.

## Application Execution Instructions

Activate the Python environment that you created from Anaconda Prompt terminal by entering the following command:
conda activate <python_env_nm>  (e.g., conda activate gis_app)

Next, navigate to the application root directory (i.e., ../gis_app)

### Configuring the Application

Edit the file below replacing the place holders (e.g., <password>)
with your own PostgreSQL database and Google Map credentials using a code text editor:

- gis_app.ini

### Creating the Database and Tables

Execute this command below in order to create the target database: gis and table: us_state and related index:

- python create_gis_tables.py

### Loading the Database Tables

Run this script to load the staging table: us_state_stg and target table: us_state:

- python load_gis_data.py

### Starting the Local Web Server

Execute this command to start a local Flask Web server:

- python lookup_state.py

### Looking the State Name of Addresses

Open another Anaconda Prompt terminal window, activate your Python environment and run this script to display the state name associated with a few addresses:

- python test_gis_addr.py 

## Adding Additional Street Addresses

You might use the Web site below to generate random addresses and add them to the script: test_gis_addr.py

- https://www.bestrandoms.com/random-address

Once you have edited the aforementioned file, execution the Python command under the section "Looking the State Name of Addresses" above.
