import picamera
from picamera import Color
from subprocess import call
from subprocess import Popen
from datetime import datetime
from time import sleep
import threading


def takePics(picTotal):
    #our file path
    filePath = "/home/pi/Desktop/cookie/Image/"
    #picTotal = 1
    picCount = 0
    
    while picCount < picTotal:
        # grab the current time
        currentTime = datetime.now()
        
        #Setup the camera such that it closes
        #when we are done with it.
        print("About to take a picture.")
        print("Add timestamp to pic")
        timestampMessage = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    
        
    

        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            camera.start_preview()
            
            camera.annotate_foreground = Color('black')
            camera.annotate_background = Color('white')
            camera.annotate_text = timestampMessage
            
          
            while(datetime.now()-currentTime).seconds <= 5:
                camera.annotate_text = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
                sleep(0.2)
            
            # Create file name for our picture
            picTime = datetime.now().strftime("%Y.%m.%d-%H%M%S")
            picName = picTime + '.jpg'
            completeFilePath = filePath + picName
            camera.capture(completeFilePath)
            camera.stop_preview()
        print("Picture taken.")
        
        timestampCommand = "/usr/bin/convert " + completeFilePath + " -pointsize 36 -fill red -annotate +700+650 '" + timestampMessage + "' " + completeFilePath
        #Execute our command
        #call([timestampCommand], shell=True)
        print("timestamp added")
        #Advance our picture counter
        picCount += 1
        sleep(0.5)

def takevid():
    # grab the current time
    currentTime = datetime.now()
    timestampMessage = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    #our file path
    filePath = "/home/pi/Desktop/cookie/Video/"
    
    # Create file name for our picture
    vidTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
    vidName = vidTime + '.h264'
    completeFilePath = filePath + vidName
   
    #Setup the camera
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.start_preview()
            
        camera.annotate_foreground = Color('black')
        camera.annotate_background = Color('white')
        camera.annotate_text = timestampMessage
        camera.start_recording(completeFilePath)    
          
        while(datetime.now()-currentTime).seconds <= 10:
            camera.annotate_text = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
            camera.wait_recording(0.2)
        
        
      
        camera.stop_recording()
        camera.stop_preview()
        
        print("convert the video..")
        #Define the command we want to execute.
        command = "MP4Box -add " + completeFilePath + " " + filePath + vidTime + ".mp4"
        #Execute our command
        call([command], shell = True)
        print("Video converted.")
        