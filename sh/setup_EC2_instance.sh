#!/bin/bash
# 
# This script will setup anaconda, jupyter notebook,
# Java, Scala, and Spark on a Amazon EC2 ubuntu instance
#
# Reference: Jose Portilla https://bit.ly/2uDx7Ck


# Download and setup anaconda
wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
bash Anaconda3-5.1.0-Linux-x86_64.sh
source ~/.bashrc


# Create certifications 
mkdir certs
cd certs
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem

# Configure Jupyter Notebook
jupyter notebook --generate-config
cd ~./jupyter/
mv jupyter_notebook_config.py temp_config.py

echo '
c = get_config()

Notebook config this is where you saved your pem cert
c.NotebookApp.certfile = u"/home/ubuntu/certs/mycert.pem"

# Run on all IP addresses of your instance
c.NotebookApp.ip = "*"

# Dont open browser by default
c.NotebookApp.open_browser = False  

# Fix port to 8888
c.NotebookApp.port = 8888
' > jupyter_notebook_config.py

echo temp_config.py >> jupyter_notebook_config.py
rm -f temp_config.py


# Install Java
sudo apt-get update
sudo apt-get install default-jre

# Install Scala
sudo apt-get install scala

# Install py4j
export PATH=$PATH:$HOME/anaconda3/bin
conda install pip
pip install py4j

# Install Spark and Hadoop
wget archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
mv spark-2.3.0-bin-hadoop2.7.tgz $HOME/
cd $HONE/
sudo tar -zxvf spark-2.3.0-bin-hadoop2.7.tgz


# Tell Python where to find Spark
SPARK_HOME='/home/ubuntu/spark-2.3.0-bin-hadoop2.7'
PATH=$SPARK_HOME:$PATH
PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH

exit $?












