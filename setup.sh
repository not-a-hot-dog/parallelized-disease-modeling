#!/bin/bash
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc
python3 -m pip install -U pip
pip install numpy
pip install matplotlib

