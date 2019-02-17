import socket
from datetime import datetime

class message:
    def __init__(self,alias, message,time):
        self.time = time
        self.alias = alias
        self.message = message

    def constructMess(self):
        messWithoutSize = str(self.time)+ ":" + self.alias + ":" + self.message 
        size = len(messWithoutSize)
        size = str(size)
        
        if(len(size) < 3):
            size = '0' + size
        elif(len(size) > 3):
            size = size[len(size)-3] + size[len(size)-2] + size[len(size-1)]

        completeMessage = size + ":" + messWithoutSize
        return completeMessage

    def deconstructMess(self,fullmess):
        datetime = fullmess[:14]
        datetime = formatTime(datetime)
        alias = ""
        messIndex = 0
        message = ""

        for i in range(15,len(fullmess)):
            alias = alias + fullmess[i]
            if(fullmess[i+1] == ':'):
                messIndex = i + 2
                break
        message = fullmess[messIndex:]
        print(datetime + ":", alias, ":", message)
       
        
def intTime():
    timeNow = str(datetime.utcnow())
    timeNow = timeNow.replace("-", "")
    timeNow = timeNow.replace(" ", "")
    timeNow = timeNow.replace(":","")
    timeNow = timeNow.split('.', 1)[0]
    timeNow = int(timeNow)
    return timeNow

def formatTime(datetime):
    year = datetime[:4]
    month = datetime[4:6]
    day = datetime[6:8]
    hour = datetime[8:10]
    minute = datetime[10:12]
    second = datetime[12:14]
    return month + "/" + day + "/" + year + "-" + hour + ":" + minute + ":" + second

def loopRecv(csoc, size):
    data = bytearray(b" "*size)
    mv = memoryview(data)
    while size:
        rsize = csoc.recv_into(mv,size)
        mv = mv[rsize:]
        size -= rsize
    return data

def sizetoInt(size):
    size = size[:3]
    size = int(size)
    return size


def baseTCPProtocolC(csoc):
    print("Started baseTCPProtocol")
    
    mess = ""
    messageC = message("alias1",mess,intTime())  #create message object
    while(True):
        mess = input("alias1>")             #get server response
        messageC.message = mess    #modify message attribute in object
        messageC.time = intTime()   #assign send time
        messageToSend = messageC.constructMess() #construct message object
        csoc.sendall(messageToSend.encode("utf-8"))   #send message
        print("Message Sent: ",formatTime(str(intTime())),"\n")
        if(mess == "bye"):
            break
    
        size = loopRecv(csoc,4)             #get size of incoming message
        size = size.decode("utf-8")        
        size = sizetoInt(size)             #get int of size
        data = loopRecv(csoc,size)         #use to recieve rest of message
        data = data.decode("utf-8")              
        messageC.deconstructMess(data)   #print message

    print("Ended baseTCPProtocol")
    

if __name__ == "__main__":
    # create the socket
    #  defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    commsoc = socket.socket()
    
    # connect to localhost:5000
    commsoc.connect(("localhost",5000))
    
    # run the application protocol
    baseTCPProtocolC(commsoc)
    
    # close the comm socket
    commsoc.close()

    