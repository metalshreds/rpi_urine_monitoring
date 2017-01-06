import io
import random
import picamera
import datetime as dt
from time import gmtime, strftime
import csv
from mettler_toledo_device import MettlerToledoDevice
dev = MettlerToledoDevice() # Might automatically find device if one available
# if it is not found automatically, specify port directly
dev = MettlerToledoDevice(port='/dev/ttyACM0') # Linux specific port


filename = dt.datetime.now().strftime('%Y-%m-%d hr%H_min%M_s%S')
filename += '.csv'
saveFile = open(filename, 'w')
#saveFile = open('timedata.csv', 'aw')
writer = csv.writer(saveFile)

# Main #
# get current weight
print('program started')
weight, units, stability = dev.get_weight()
currWeight = weight
# start picamera
camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=10)
camera.start_recording(stream, format='h264')
try:
    while True:
        print('waiting')
        # # Annotate camera
        timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = timestamp
        # Write File
        writer.writerow([timestamp, weight])
        camera.wait_recording(0.2)
        # #
        # video_timestamp(camera)
        weight, units, stability = dev.get_weight() # get the current weight

        if weight-currWeight >= 0.005:
            print('event detected')
            print(weight)
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            # camera.wait_recording(10)
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < 10:
                # # Annotate camera
                timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                camera.annotate_background = picamera.Color('black')
                camera.annotate_text = timestamp
                # Write File
                weight, units, stability = dev.get_weight()  # get the current weight
                writer.writerow([timestamp, weight])
            # Write video to file
            file_name = start.strftime("%Y-%m-%d %H:%M:%S.%f") + ".h264"
            #stream.copy_to(file_name, seconds=30)
            stream.copy_to('motion.h264')
            print('done writing file')
        currWeight = weight             # weight updated but no event occurring
finally:
    camera.stop_recording()
    saveFile.close()
