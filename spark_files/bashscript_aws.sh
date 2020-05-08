#!/bin/bash

wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p $HOME/conda
echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

pip install geospark
pip install pandas
pip install geopandas
pip install haversine

sudo mkdir /jars
cd /jars
sudo wget https://github.com/DataSystemsLab/GeoSpark/blob/master/python/geospark/jars/2_4/geo_wrapper_2.11-0.3.0.jar 
sudo wget https://github.com/DataSystemsLab/GeoSpark/blob/master/python/geospark/jars/2_4/geospark-1.3.0.jar
sudo wget https://github.com/DataSystemsLab/GeoSpark/blob/master/python/geospark/jars/2_4/geospark-sql_2.3-1.3.0.jar
sudo wget https://github.com/DataSystemsLab/GeoSpark/releases/download/1.2.0-spark-2.3/geospark-viz_2.3-1.2.0.jar