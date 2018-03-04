import socket
import syslog
#Logging Library
class Facility:
  "Syslog facilities"
  KERN, USER, MAIL, DAEMON, AUTH, SYSLOG, \
  LPR, NEWS, UUCP, CRON, AUTHPRIV, FTP = range(12)

  LOCAL0, LOCAL1, LOCAL2, LOCAL3, \
  LOCAL4, LOCAL5, LOCAL6, LOCAL7 = range(16, 24)

class Syslog:
    def __init__(self,host="localhost",port=514,facility=Facility.DAEMON):
        self.host = host
        self.port = port
        self.facility = facility
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Send Function for sending logs to Host
    def send(self, message, level=1):
        data = "<{}>{}".format(level + self.facility*8, message)
        self.socket.sendto(data.encode(), (self.host, self.port))
#Logging Class:
class LoggingClass:
    def __init__(self,server_address="0",port=514,server_facility=Facility.DAEMON,file_address=''):
        self.server_address=server_address
        self.file_address=file_address
        self.port=port
        self.server_facility=server_facility
        if(self.server_address !="0"):
            self.local=1
        elif(self.file_address != ''):
            self.local=2
        else:
            self.local=0
    def Logging_local(self,message):
        syslog.syslog(message)
    
    def Logging_file (self,message):
        f=open(self.file_address,"a+")
        f.write("\n" + message)
        f.close()
    def Logging_remote (self,message):
        log=Syslog(self.server_address,self.port,self.server_facility)
        log.send(message)
    def Send(self,message):
        if(self.local == 0):
            self.Logging_local(message)
        elif(self.local == 2):
            self.Logging_file(message)
            #print("test")
        else:
            self.Logging_remote(message)
