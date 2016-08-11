import serial
from time import gmtime, strftime
import picamera
import datetime as dt
import csv
import io

#Get Hold of Arduino and sample weight data
ser = serial.Serial('/dev/ttyACM0',9600)
weightdata = ser.readline()

#Open Save File
file = open('timedata.csv','aw')
writer = csv.writer(file)

timedata = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print(weightdata,timedata)

### SETUP METTLER TOLEDO SCALE
from mettler_toledo_device import MettlerToledoDevice
###dev = MettlerToledoDevice() # Might automatically find device if one available
# if it is not found automatically, specify port directly
###dev = MettlerToledoDevice(port='/dev/ttyACM0') # Linux specific port
#dev = MettlerToledoDevice(port='/dev/tty.usbmodem262471') # Mac OS X specific port
#dev = MettlerToledoDevice(port='COM3') # Windows specific port


#TODO
# while - key not pressed or script stopped
#       - Circular buffer
# def - weight_measurements() <-- check continuously
#       - Weight comparison - percent error
#       - Record (xlsx)- timestamps and weight in excel sheet
#***EVENT DETECTED
# def - write_video() event detected - write circular buffer
#       - capture video with timestamp percent fluctuation
#       - How many seconds previous to the event?
#
#       view camera remotely
#       start/stop script remotely


# Setup Camera
camera = picamera.PiCamera(resolution=(1280, 720), framerate=24)
camera.start_preview()
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.start_recording('timestamped.h264')
start = dt.datetime.now()

# Start Recording
while (dt.datetime.now() - start).seconds < 5:
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weightdata = ser.readline()
    camera.annotate_text = timestamp
    camera.wait_recording(0.2)

    #Write timestamp to file
    writer.writerow([timestamp, weightdata])

camera.stop_recording()


## Display End Timestamp and Weight
weightdata = ser.readline()
timedata = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print(weightdata,timedata)

#Close File
file.close()



def write_video(stream):
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    # Wipe the circular stream once we're done
    stream.seek(0)
    stream.truncate()

def detect_weight(timestamp):
    ## With Mettler Toledo
    weight, units, stability = dev.get_weight()
    ###writer.writerow([timestamp, weightdata])

    ## With Arduino
    arduinoValue = ser.readline()
    if arduinoValue == '0': #No Weight Change
        return False
    elif arduinoValue == '1024': #Weight Change
        return True





############### "MAIN" METHOD

with picamera.PiCamera(resolution=(1280, 720), framerate=24) as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_preview()
    #annotation
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #Start Recording
    camera.start_recording('timestamped.h264')
    ##
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            #Update Annotation
            timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.annotate_text = timestamp
            #
            camera.wait_recording(0.2)
            if detect_weight(timestamp):
                print('Weight Change Detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_weight(timestamp):
                    camera.wait_recording(1)
                print('Weight Change Stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()