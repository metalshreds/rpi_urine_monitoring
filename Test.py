import serial
from time import gmtime, strftime
import picamera
import datetime as dt

ser = serial.Serial('/dev/ttyACM0',9600)
weightdata = ser.readline()
timedata = strftime("%Y-%m-%d %H:%M:%S", gmtime())

file = open('timedata.csv','a')
writer = csv.writer(file)


# with picamera.PiCamera() as camera:
#   camera.resolution = (640, 480)

weightdata = ser.readline()
timedata = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print(weightdata,timedata)

camera = picamera.PiCamera(resolution=(1280, 720), framerate=24)
camera.start_preview()
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.start_recording('timestamped.h264')
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 30:
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_text = timestamp
    camera.wait_recording(0.2)
    writer.writerow(timestamp)
camera.stop_recording()

# camera.start_recording('my_video.h264')
# camera.wait_recording(60)
# camera.stop_recording()

weightdata = ser.readline()
timedata = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print(weightdata,timedata)

file.close()

