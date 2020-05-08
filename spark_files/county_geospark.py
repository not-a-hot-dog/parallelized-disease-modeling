from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import string, sys, re

import pandas as pd
import geopandas as gpd
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from geospark.register import upload_jars
from geospark.register import GeoSparkRegistrator

# Create Spark Session
spark = SparkSession.builder.\
    appName("SparkSessionExample").\
    getOrCreate()

# Uses findspark Python package to upload jar files to executor and nodes.
upload_jars()

# Registers all GeoSparkSQL functions
GeoSparkRegistrator.registerAll(spark)

# Load matrix of coordinates and US county data into Spark and GeoPandas
original_matrix_df = spark.read.format("csv").option("header", "true").load("geospark_matrix.csv")
original_geo_df = gpd.read_file("cb_2018_us_county_500k/cb_2018_us_county_500k.shp")

# Map Polygon in geometry field of geo_d fto WKT (well-known-text) format and rename as counties_df 
wkts = map(lambda g: str(g.to_wkt()), original_geo_df.geometry)
original_geo_df['wkt'] = pd.Series(wkts)
original_geo_df = original_geo_df.drop("geometry", axis=1)
counties_df = spark.createDataFrame(original_geo_df)

# Use Spark SQL to create new column location with each location as ST_POINT
original_matrix_df.createOrReplaceTempView("matrix")
original_matrix_df = spark.sql("SELECT *, ST_Point(CAST(matrix.lon AS Decimal(24,20)), CAST(matrix.lat AS Decimal(24,20))) AS location FROM matrix")

# Use Spark SQL to create new Spark DF with only GEOID and geometry coordiantes
counties_df.createOrReplaceTempView('counties')
counties_df = spark.sql("SELECT GEOID, st_geomFromWKT(wkt) as geometry from counties")

# Reload data into SQL names
counties_df.createOrReplaceTempView('counties')
original_matrix_df.createOrReplaceTempView("matrix")

# Find intersection between the coordinates and the geographical boundaries of the counties
mapped_county_coord = spark.sql("SELECT h.lat, h.lon, c.GEOID FROM counties AS c, matrix AS h WHERE ST_Intersects(c.geometry, h.location)")

# Merge original coordinate matrix with mapped data
coord_df = original_matrix_df.drop("location")
results = coord_df.join(mapped_county_coord, ['lat','lon'], 'left')

# Convert the DataFrame to a RDD before mapping it to a tuple
RDD = results.rdd.map(tuple)
RDD = RDD.map(lambda tup: str(float(tup[0])) + "," + str(float(tup[1])) + "," + str(int(float(tup[2]))) + "," + str(int(float(tup[3]))) + "," + str(tup[4]))
RDD.saveAsTextFile("s3://emr-example-python-ryzy1990/spark_output_geodf2")