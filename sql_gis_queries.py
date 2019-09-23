###########################################################
# Drop Tables
us_state_tbl_drop = "DROP TABLE IF EXISTS us_state;"
us_state_stg_tbl_drop = "DROP TABLE IF EXISTS us_state_stg;"

###########################################################
# Create Tables
us_state_tbl_create = ("""
    CREATE TABLE IF NOT EXISTS us_state
    (
        gid SERIAL PRIMARY KEY,
        geoid SMALLINT NOT NULL, 
        stusps TEXT NOT NULL,
        name TEXT NOT NULL,
        intptlat TEXT,
        intptlon TEXT,
        geog GEOMETRY
    );
""")

us_state_idx_create = ("""
    CREATE INDEX us_state_geom_idx ON us_state USING GIST (geog);
""")

###########################################################
# Insert Records
us_state_tbl_insrt = ("""
    INSERT INTO us_state(geoid, stusps, name, intptlat, intptlon, geog)
        SELECT CAST(geoid AS SMALLINT), stusps, name, intptlat, intptlon
            , ST_Transform((ST_Dump(geog)).geom, 4326) AS geog
        FROM us_state_stg
        ;
""")

###########################################################
# Insert Records
us_state_tbl_del = ("""
    DELETE FROM us_state;
""")


###########################################################
# Find State associated with long, latitude
state_nm_tmplt_sel = ("""
    SELECT us_state.name
    FROM us_state, 
    (
        SELECT ST_SetSRID(ST_MakePoint(LOCATION_TKN), 4326) point
        --select  ST_PointFromText('POINT(LONGITUDE_TKN LATITUDE_TKN)', 4326) point
    ) addr
    WHERE ST_INTERSECTS(us_state.geog, addr.point)
""")


create_tbl_queries = [us_state_tbl_create, us_state_idx_create]
load_tbl_queries = [us_state_tbl_del, us_state_tbl_insrt] 
drop_tbl_queries = [us_state_tbl_drop, us_state_stg_tbl_drop]
