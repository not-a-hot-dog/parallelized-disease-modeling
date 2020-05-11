To implement the GeoSpark code on an AWS cluster, you will require the following steps:

1) Bootstrap the AWS EMR cluster using bashscript_aws.sh contained in this folder. 

The Bash script does the following:
- Downloads Miniconda
- Installs required packages (Geospark, Pandas, Geopandas, Haversine) across all nodes in the cluster
- Downloads Java ARchive (JAR) files required for GeoSpark onto EMR cluster

2) When setting up the EMR cluster, include the geospark.json file in this folder as part of the cluster configuration

3)When launching the EMR cluster, specify the SPARK_HOME environment variable as `/usr/lib/spark` by using the following command or adding it to .bashrc: 
`export SPARK_HOME=/usr/lib/spark`

4) The following two lines are also added to /usr/lib/spark/conf/spark-env.sh:
`export PYSPARK_PYTHON=/home/hadoop/conda/bin/python`
`export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/python`

