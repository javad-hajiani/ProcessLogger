# ProcessLogger

## Getting Started

This script help us for logging created or killed process.Its my experience for our servers

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

##### Run Script on startup
- RC.Local
 - > sudo echo "python3 /path/to/main.py" >> /etc/rc.local
- crontab -e
 - > @reboot /usr/bin/python3 /path/to/main.py 
