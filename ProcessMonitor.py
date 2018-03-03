
# coding: utf-8

## Process Monitor Script

##### Import Libraries
import time
import os
import os.path
class ProcessMonitor:
    def __init__(self,log_address,swapfile):
        self.log_address=log_address
        self.swapfile=swapfile
        self.process_dict={}
        self.processdict_last={}
        #print ("{},{},{},{}".format(self.process_dict,self.processdict_last,self.log_address,self.swapfile))


#Log Rotation Method
    def log_rotation(self,log_maxsize=9999999999):
        log_size= os.stat(self.log_address).st_size
        now = time.strftime("%M%S")
        if ( 300 <= int(now) and int(now) < 305 or log_size > log_maxsize):
            with open(log_address,'w') as log_file:
                log_file.write("")


#Process List Section
    def process_list_now(self):
        lines=[]
        cmd="ps aux | awk '{print $1\"|\"$2\"|\"$11}'"
        proc_list = os.popen(cmd).read()
        with open(self.swapfile,'w') as proc_file:
            proc_file.writelines(proc_list)
        proc_list=proc_list.split('\n')
        process_dict={}
        for iter_dict in proc_list:
            if len(iter_dict)>1:
                lines=iter_dict.split('|')
                if(len(lines)>2):
                    process_dict.update({lines[1]:{'USER':lines[0],'CMD':lines[2]}})
        self.process_dict=process_dict


#Process List For Last Check
    def process_list_last(self):
        lines=[]
        if os.path.isfile(self.swapfile): 
            with open(self.swapfile,'r') as proc_file:
                result=proc_file.read().splitlines()
        else:
            cmd="ps aux | awk '{print $1\"|\"$2\"|\"$11}'"
            result = os.popen(cmd).read()
            with open(self.swapfile,'w') as proc_file:
                proc_file.writelines(result)
            result=result.split('\n')
        processdict_last={}
        for iter_dict in result:
            if len(iter_dict)>1:
                lines=iter_dict.split('|')
                if(len(lines)>2):
                    processdict_last.update({lines[1]:{'USER':lines[0],'CMD':lines[2]}})
                    #print ("processdict_last = {}".format(processdict_last))         
        self.processdict_last=processdict_last

#Check PIDs For New Ones or Deletes
    def check_pid(self):
        set_now=set(self.process_dict.keys())
        set_last=set(self.processdict_last.keys())
        items_created=[x for x in self.process_dict.keys() if x not in set_last]
        exepted_cmd=['/bin/sh','sleep','bash','awk','ps','python3.6','-bash']
        local_time= time.asctime(time.localtime(time.time()))
        for i in items_created:
            new_cmd = self.process_dict[i]['CMD']
            if (new_cmd not in exepted_cmd):
                experssion="{}|BR_ProcAnalyzer|Created|{}|{}|{}".format(local_time,self.process_dict[i]['USER'],self.process_dict[i]['CMD'],i)
                f=open(self.log_address,"a+")
                f.write("\n" + experssion)
                f.close()
        items_closed=[x for x in self.processdict_last.keys() if x not in set_now]
        for i in items_closed:
            new_cmd = self.processdict_last[i]['CMD']
            if (new_cmd not in exepted_cmd):
                experssion="{}|BR_ProcAnalyzer|Closed|{}|{}|{}".format(local_time,self.processdict_last[i]['USER'],self.processdict_last[i]['CMD'],i)
                f=open(self.log_address,"a+")
                f.write("\n" + experssion)
                f.close()


log_file='/var/log/prc_br.log'
swapfile="/root/text.txt"
monitorobj=ProcessMonitor(log_file,swapfile)
while True:
    monitorobj.process_list_last()
    monitorobj.process_list_now()
    monitorobj.check_pid()
    #log rotation run once per hour,but you can set with maximum log file size
    monitorobj.log_rotation()
    time.sleep(5)
    #print("Logging!!!")


