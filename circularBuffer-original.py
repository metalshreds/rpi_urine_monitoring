import io
import random
import picamera
import datetime as dt


def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0

camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        camera.wait_recording(1)
        if motion_detected():
            print('motion detected')
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            camera.wait_recording(10)
            start = dt.datetime.now()
            # file_name = start.strftime("%Y-%m-%d %H:%M:%S") + ".h264"
            stream.copy_to('video.h264', seconds=30)
            print('finished saving')
finally:
    camera.stop_recording()