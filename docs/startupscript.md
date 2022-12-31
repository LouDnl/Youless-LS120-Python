# auto start the youless live view webpage as a service on linux

## create and edit startup script if you want to use environment variables
`sudo touch /usr/local/bin/youless.sh` \
`sudo nano /usr/local/bin/youless.sh` \
Change the following shell script example to your liking. \
Where there is a trailing `/` in a path it is required.
```shell
#!/bin/bash

# Youless IP
export YOULESS_IP="0.0.0.0"  # change this to the ip address of your youless

# host IP address and port for the webserver to run on
export YOULESS_HOST="0.0.0.0"  # change this to the webserver ip
export YOULESS_PORT="0"  # change this to the webserver port
export YOULESS_SCRIPTPATH="/path/to/LS120/git"  # change to where you stored the git clone
export YOULESS_LOGPATH="/path/to/logfile/folder/"  # change to where you want the log file stored

# Locale settings
export YOULESS_LANG="NL"  # or EN
export YOULESS_LOCALE="nl_NL.utf8"  # or en_US.utf8

# Database path and filename
export YOULESS_DBNAME="youless.db"  # name of the SQLite3 filename you want to create and use
export YOULESS_DBPATH="/path/to/database/"  # path where you want the db file to be stored

# start all_graphs_live
exec /usr/bin/python3 $YOULESS_SCRIPTPATH/dash_allgraphs_live.py env

```

## create and edit service file
`sudo touch /etc/systemd/system/youless.service` \
`sudo nano /etc/systemd/system/youless.service` \
Add the following text (change `/path/to/`):
```shell
[Unit]
Description=Youless Energy service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/local/bin/youless.sh

[Install]
WantedBy=multi-user.target

```

## start and enable the service
Then reload the service files: \
`sudo systemctl daemon-reload` \
Start the service: \
`sudo systemctl start youless.service` \
Enable the service on reboot: \
`sudo systemctl enable youless.service`

## optionally add daily service restart to crontab
Edit crontab: \
`sudo nano /etc/crontab` \
Add these lines at the bottom of your crontab for a daily restart at 3 am:
```
# daily restart of youless service
# every day at 3 am
0 3 * * * root systemctl restart youless.service

```
