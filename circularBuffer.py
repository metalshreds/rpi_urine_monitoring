import io
import random
import picamera
import datetime as dt
from time import gmtime, strftime
import csv
#from mettler_toledo_device import MettlerToledoDevice


file = open('timedata.csv','aw')
writer = csv.writer(file)

def write_now():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 100) == 0

def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        file_name = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        fileName = file_name + '.h264'
        with io.open(fileName, 'wb') as output:
            #output.write(stream.read())
            stream.copy_to(fileName, seconds = 30)
    print('Done Writing Video!')

def write_file(timestamp):
    weightData = write_now();
    writer.writerow([timestamp, weightData])

def video_timestamp(camera):
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = timestamp
    camera.wait_recording(0.2)
    write_file(timestamp)


##### MAIN #####
with picamera.PiCamera(resolution=(1280, 720), framerate=24) as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')

    try:

        while True:
            #camera.wait_recording(1)
            video_timestamp(camera)
            if write_now():
                print('Event Triggered')
                # Keep recording for 10 seconds and only then write the stream to disk
                #camera.wait_recording(10)
                start = dt.datetime.now()
                while (dt.datetime.now() - start).seconds < 10:
                    video_timestamp(camera)
                write_video(stream)

    finally:
        print('stop_recording')
        camera.stop_recording()
        file.close()