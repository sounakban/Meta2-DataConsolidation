# Meta2-DataConsolidation
Contains Code used to get list of all Meta-2 data from hass server, get schema and other structural information and transfer to sql Database


mounting commands:
mkdir /mnt/hassServer
sudo mount -t cifs -o username=<username> //hass11.win.rpi.edu/Research/cwl-data /mnt/hassServer


Issues with database privillages in mySQL:
login to root with : sudo mysql -u root -p
run following command to create new user and grant access: 
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL on *.* to 'newuser'@'localhost';
FLUSH PRIVILEGES;


Preparing database:
CREATE DATABASE Meta2_DB;
