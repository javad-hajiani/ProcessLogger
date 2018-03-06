# pmonitor ProcessLogger

## Getting Started

This script help us for logging created or killed process and ports.Its my experience for our servers

You Can Logging Process Into File or Local Syslog or Directly Send to Syslog Server.

### Requirements

- Python3
 - Debian Based
  - > sudo apt install python3
 - Redhat Based
  - > sudo yum -y install python3
 - Arch Based
  - > sudo pacman -Sy python3

### Configuration

##### Run Script to install Python package
- Service Base
 - Run With root Permission > sudo /path/to/run.sh
- crontab -e
 - Run With root Permission > @reboot /usr/bin/python3 /path/to/main 

##### Start pmonitor Service
- Service Command
 - > sudo service pmonitor start
- INIT File
 - > sudo /etc/init.d/pmonitor start

##### Run as Startup
- update-rc.d
 - > sudo update-rc.d pmonitor enable
- chkconfig
 - > sudo chkconfig pmonitor on
