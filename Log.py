"""
simple log class to log all files which the download url doesnot exits for them
"""
class Log:
    def __init__(self):
        print("opening log file...")
        self.log_file = open("./log.txt","w") #opening the file
    
    def __del__(self):
        print("closing log file...")
        self.log_file.close() #closing the file

    def log(self,msg):
        self.log_file.write(msg+"\n") #writing to the file

    