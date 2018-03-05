import os
import syslogclient
class PortMonitor:
    def __init__(self,log_address,swapfile,ip="0",port=514):
        self.ip=ip
        self.port=port
        self.log_address=log_address
        self.swapfile=swapfile
        self.Port_dict={}
        self.Portdict_last={}
        #print ("{},{},{},{}".format(self.Port_dict,self.Portdict_last,self.log_address,self.swapfile))


#Port List Section
    def Port_list_now(self):
        lines=[]
        cmd="netstat -nutlp | sed 1,2d | awk '{print $1\"|\"$4\"|\"$7}'"
        ports_list = os.popen(cmd).read()
        with open(self.swapfile,'w') as ports_file:
            ports_file.writelines(ports_list)
        ports_list=ports_list.split('\n')
        Port_dict={}
        for iter_dict in ports_list:
            if len(iter_dict)>1:
                lines=iter_dict.split('|')
                if (lines[2] != ''):
                    pid=lines[2].split('/')[0]
                    cmd=lines[2].split('/')[1]
                if(len(lines)>1 and lines[1].split(':')[0] != '127.0.0.1' and lines[1].split(':')[0] != '' ):
                    Port_dict.update({lines[1].split(':')[1]:{'proto':lines[0],'CMD':cmd,'listen':lines[1].split(':')[0],'pid':pid}})
        self.Port_dict=Port_dict

        #Process List For Last Check
    def Port_list_last(self):
        lines=[]
        if os.path.isfile(self.swapfile): 
            with open(self.swapfile,'r') as ports_file:
                result=ports_file.read().splitlines()
        else:
            cmd="netstat -nutlp | sed 1,2d | awk '{print $1\"|\"$4\"|\"$7}'"
            result = os.popen(cmd).read()
            with open(self.swapfile,'w') as ports_file:
                ports_file.writelines(result)
            result=result.split('\n')
        Portdict_last={}
        for iter_dict in result:
            if len(iter_dict)>1:
                lines=iter_dict.split('|')
                #print ("Started \n {} \n Ended".format(lines))
            cmd=''
            pid=''
            port=''
            if (len(lines[1].split(':'))>1):
                port=lines[1].split(':')[1]
            if (len(lines[2].split('/'))> 1):
                    pid=lines[2].split('/')[0]
                    cmd=lines[2].split('/')[1]
            if(len(lines)>1 and lines[1].split(':')[0] != '127.0.0.1' and lines[1].split(':')[0] != '' ):
                    Portdict_last.update({port:{'proto':lines[0],'CMD':cmd,'listen':lines[1].split(':')[0],'pid':pid}})
                    #print ("Portdict_last = {}".format(Portdict_last))         
        self.Portdict_last=Portdict_last
    def check_Port(self):
        logger=syslogclient.LoggingClass(self.ip,self.port)
        set_now=set(self.Port_dict.keys())
        set_last=set(self.Portdict_last.keys())
        items_created=[x for x in self.Port_dict.keys() if x not in set_last]
        exepted_Ports=['0']
        for i in items_created:
            if (i not in exepted_Ports):
                experssion="{}|PortListened|{}|{}|{}|{}".format(self.Port_dict[i]['CMD'],self.Port_dict[i]['listen'],self.Port_dict[i]['pid'],self.Port_dict[i]['proto'],i)
                logger.Send(experssion)
                f=open(self.log_address,"a+")
                f.write("\n" + experssion)
                f.close()
        items_closed=[x for x in self.Portdict_last.keys() if x not in set_now]
        for i in items_closed:
            if (i not in exepted_Ports):
                experssion="{}|PortClosed|{}|{}|{}".format(self.Portdict_last[i]['CMD'],self.Portdict_last[i]['pid'],self.Portdict_last[i]['listen'],self.Portdict_last[i]['proto'],i)
                logger.Send(experssion)
