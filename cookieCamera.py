import picamera
from subprocess import call
from subprocess import Popen
from datetime import datetime
from time import sleep
import threading


def takePics(picTotal):
    #our file path(need to create a cookie directory beforehand)
    filePath = "/home/pi/Desktop/cookie/"
    #picTotal = 1
    picCount = 0
    
    while picCount < picTotal:
        # grab the current time
        currentTime = datetime.now()
        # Create file name for our picture
        picTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
        picName = picTime + '.jpg'
        completeFilePath = filePath + picName
        #Setup the camera such that it closes
        #when we are done with it.
        print("About to take a picture.")
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            camera.capture(completeFilePath)
        print("Picture taken.")
    
        print("Add timestamp to pic")
        timestampMessage = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    
        timestampCommand = "/usr/bin/convert " + completeFilePath + " -pointsize 36 -fill red -annotate +700+650 '" + timestampMessage + "' " + completeFilePath
    
        #Execute our command
        call([timestampCommand], shell=True)
        print("timestamp added")
        #Advance our picture counter
        picCount += 1
        sleep(0.5)

def takevid():
    #Setup the camera
    with picamera.PiCamera() as camera:
    
        #our file path(need to create a video directory beforehand)
        filePath = "/home/pi/Desktop/cookie/Video/"
        currentTime = datetime.now()
        # Create file name for our picture
        vidTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
        vidName = vidTime + '.h264'
        completeFilePath = filePath + vidName
        camera.start_recording(completeFilePath)
        sleep(5)
        camera.stop_recording()
    
        print("convert the video..")
        #Define the command we want to execute.
        command = "MP4Box -add " + completeFilePath + " " + filePath+vidTime + ".mp4"
        #Execute our command
        call([command], shell = True)
        print("Video converted.")
        #t = threading.Thread(target = playVideo, name = 'thread1', args = (filePath, vidTime))
        #t.start()
        #t.join()
        
def playVideo(filePath, vidTime):
    playvideo = "omxplayer " + filePath + vidTime + ".mp4"
    Popen([playvideo], shell = True)
    print("Video played")
    
