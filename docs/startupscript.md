# auto start the youless live view webpage as a service on linux

## create and edit service file
`sudo touch /etc/systemd/system/youless.service` \
`sudo nano /etc/systemd/system/youless.service` \
Add the following text (change `/path/to/`):
```
[Unit]
Description=Youless Energy service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/python3 /path/to/dash_allgraphs_live.py default

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
