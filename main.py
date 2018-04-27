#Threading module

import threading
import time
import socket
import cookieCamera
import P3picam

UDP_IP = "192.168.1.10"
UDP_PORT = 5005
MESSAGE = "Delay for 5 secs"

def receive():
    global delay,lock
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        data,addr = sock.recvfrom(1024)
        #print (addr[0])
        if addr[0] != UDP_IP:
            print ("received message:"+data.decode())
            lock.acquire()
            try:
                delay = True
            finally:
                lock.release()
            break


global delay, lock
lock = threading.Lock()
delay = False
print("program start from here")
#program starts
while True:
    print("threading")
    #set a thread for receive signals from the other pi
    t = threading.Thread(target = receive, name = 'thread1', args = ())
    t.start()
    #main thread keep detecting motion and recording
  
    
    while (not delay):
        #motion detecting
        motionState = False
        motionState = P3picam.motion()
        print("motionState: "+ str(motionState))
        #print(motionState)
        if motionState:
            #motion captured, send signals to the other pi to delay their recording
            sock2= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock2.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            #recording or take picture
            #cookieCamera.takePics(2)
            cookieCamera.takevid()
            
            
    #being delayed for 5 seconds by other pi
    time.sleep(5)
        
    lock.acquire()
    try:
        delay = False
    finally:
        lock.release()