# Software Installation

To install the software you need, run the following commands in a terminal window:

```bash
sudo atp-get update
sudo apt-get install python3-requests python3-matplotlib
wget https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz
tar -xvf v1.0.7rel.tar.gz 
cd basemap-1.0.7rel/
cd geos-3.3.3/
export GEOS_DIR=/usr/local
./configure --prefix=$GEOS_DIR
make
sudo make install
cd ..
sudo python3 setup.py install
```
