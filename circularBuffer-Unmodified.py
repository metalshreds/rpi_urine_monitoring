import io
import random
import picamera
import datetime as dt
from time import gmtime, strftime


def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0


camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        print('waiting')
        camera.wait_recording(1)
        if motion_detected():
            print('motion detected')
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            camera.wait_recording(10)
            file_name = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".h264"
            stream.copy_to(file_name, seconds=30)
            print('done writing file')
finally:
    camera.stop_recording()