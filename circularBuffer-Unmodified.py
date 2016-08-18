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


def write_file(timestamp):
    #weightData = event_detected()
    writer.writerow([timestamp, event_detected()])


def video_timestamp(camera):
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = timestamp
    camera.wait_recording(0.2)
    write_file(timestamp)


def write_video(stream):
    file_name = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".h264"
    stream.copy_to(file_name, seconds=30)
    print('done writing file')


# Main #
camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        print('waiting')
        camera.wait_recording(1)
        video_timestamp(camera)
        if event_detected():
            print('event detected')
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            #camera.wait_recording(10)
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < 10:
                video_timestamp(camera)
            write_video(stream)
finally:
    camera.stop_recording()
    saveFile.close()