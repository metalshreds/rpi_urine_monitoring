import io
import random
import picamera
import datetime as dt
from time import gmtime, strftime
import csv
# from mettler_toledo_device import MettlerToledoDevice


saveFile = open('timedata.csv', 'aw')
writer = csv.writer(saveFile)


def event_detected():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0


# Main #
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
        writer.writerow([timestamp, event_detected()])
        camera.wait_recording(0.2)
        # #
        # video_timestamp(camera)
        if event_detected():
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
                writer.writerow([timestamp, event_detected()])
            # Write video to file
            file_name = start.strftime("%Y-%m-%d %H:%M:%S") + ".h264"
            stream.copy_to('video.h264', seconds=30)
            print('done writing file')
finally:
    camera.stop_recording()
    saveFile.close()
