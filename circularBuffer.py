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


saveFile = open('timedata.csv', 'aw')
writer = csv.writer(saveFile)


def event_detected(currWeight):

    # 5mg change in weight
    # 5ml in volume

    # [-0.6800, 'g', 'S'] #if weight is stable
    weight, units, stability = dev.get_weight()

    if weight-currWeight >= 0.005:
       currWeight = weight
       return True
    currWeight = weight

    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0


# Main #
# get current weight
currWeight, units, stability = dev.get_weight()
# start picamera
camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        print('waiting')
        # # Annotate camera
        timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            # camera.wait_recording(10)
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < 10:
                # # Annotate camera
                timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.annotate_background = picamera.Color('black')
                camera.annotate_text = timestamp
                # Write File
                weight, units, stability = dev.get_weight()  # get the current weight
                writer.writerow([timestamp, weight])
            # Write video to file
            file_name = start.strftime("%Y-%m-%d %H:%M:%S") + ".h264"
            stream.copy_to(file_name, seconds=30)
            print('done writing file')
        currWeight = weight             # weight updated but no event occurring
finally:
    camera.stop_recording()
    saveFile.close()
