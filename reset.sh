python ./setup.py build
sudo python ./setup.py install
sudo supervisorctl stop satnogs
killall -9 oggenc
killall -9 rtl_fm
sudo supervisorctl reread
sudo supervisorctl start satnogs
