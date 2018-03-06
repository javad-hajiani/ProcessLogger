##### Import Libraries
import time
import os
import os.path
import syslogclient
import PortMonitor
import ProcessMonitor

log_file='/var/log/prc_br.log'
swapfile="/root/text.txt"
swapfileport=swapfile+'port'
monitorobj=ProcessMonitor.ProcessMonitor(log_file,swapfile)
monitorport=PortMonitor.PortMonitor(log_file,swapfileport)
while True:    
    monitorobj.process_list_last()
    monitorobj.process_list_now()
    monitorobj.check_pid()
    monitorport.Port_list_last()
    monitorport.Port_list_now()
    monitorport.check_Port()
    #log rotation run once per hour,but you can set with maximum log file size
    time.sleep(5)
    #print("Logging!!!")

