# Lab Mice monitoring system
# Using raspberry pi camera module and mettler toledo scale
#
# Python Circular Buffer
# http://picamera.readthedocs.io/en/release-1.10/recipes2.html#splitting-to-from-a-circular-stream
#
#Mettler Toledo Scale -- Mettler Toledo New Classic MF, model MS 303S
#https://pypi.python.org/pypi/mettler_toledo_device/1.3.3

import io
import random
import picamera
from PIL import Image
#Setup Mettler Toledo Scale
from mettler_toledo_device import MettlerToledoDevice

prior_image = None

def setup_scale():
    dev = MettlerToledoDevice() # Might automatically find device if one available
    # if it is not found automatically, specify port directly
    dev = MettlerToledoDevice(port='/dev/ttyUSB0') # Linux specific port
        #dev = MettlerToledoDevice(port='/dev/tty.usbmodem262471') # Mac OS X specific port
        #dev = MettlerToledoDevice(port='COM3') # Windows specific port
    dev.get_serial_number()
        #1126493049
    dev.get_balance_data()
        #['XS204', 'Excellence', '220.0090', 'g']
    dev.get_weight_stable()
        #[-0.0082, 'g'] #if weight is stable
        #None  #if weight is dynamic
    dev.get_weight()
        #[-0.6800, 'g', 'S'] #if weight is stable
        #[-0.6800, 'g', 'D'] #if weight is dynamic
    dev.zero_stable()
        #True  #zeros if weight is stable
        #False  #does not zero if weight is not stable
    dev.zero()
        #'S'   #zeros if weight is stable
        #'D'   #zeros if weight is dynamic



def detect_motion(camera):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!
        result = random.randint(0, 10) == 0
        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        return result

#def detect_weight_change():


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

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera):
                print('Motion detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()