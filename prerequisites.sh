#!/bin/bash

mkdir prerequisites
cd prerequisites

sudo apt install python-setuptools
sudo apt install -y i2c-tools

pip3 install smbus2

wget https://files.pythonhosted.org/packages/67/8a/443af31ff99cca1e30304dba28a60d3f07d247c8d410822411054e170c9c/PyMLX90614-0.0.3.tar.gz
tar -xf PyMLX90614-0.0.3.tar.gz
cd PyMLX90614-0.0.3/
sudo python setup.py install
cd ..

git clone https://github.com/tatobari/hx711py
cd hx711py
sudo python setup.py install
cd ..

cd ..
sudo rm -r prerequisites