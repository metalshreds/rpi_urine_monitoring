# Raspberry Pi Urine Monitoring System
Logging and reviewing mice data and videos can be time consuming and tedious. The purpose of this project was to create a device that would constantly log the weight from a Mettler Toledo ML-303 while only capturing 20 seconds prior and 10 seconds after the event. The trigger mechanism was change in scale weight of 5mg from one recording to the next. 

## Materials
  * Raspberry Pi 3
  * Camera Module V2
  * Mettler Toledo Scale with USB communication
  * Mice cage suspended above mettler toledo scale with mesh floor
  * Plastic enclosure surrounding system to prevent air flow from triggering recording event.
  
## Installation for Raspberry Pi or macOS
From link below do the following:
[Setup Python](https://github.com/janelia-pypi/python_setup)
```shell
Dont install homebrew OR python -- macOS 10.11 already has python in it
sudo easy_install pip
sudo pip install virtualenv
sudo pip install ipython
sudo pip install pyserial
```

### Linux and Mac OS X

```shell
mkdir -p ~/virtualenvs/mettler_toledo_device
virtualenv ~/virtualenvs/mettler_toledo_device
source ~/virtualenvs/mettler_toledo_device/bin/activate
pip install mettler_toledo_device  ## Be sure this installs successfully
```

/Library/Python/2.7/site-packages/serial-device2

## To run simply execute the script
$ python circularBuffer_latest.py 

## Troubleshooting

  * Script ends abruptly
    * Problem: Mettler Toledo Scale is in standby mode
    * Solution: Tap the scale to take it out of standby mode 

    * Problem: Mettler Toledo Cable is not connected properly
    * Typically error says “No Mettler Toledo Device Found”
    * Solution: Check that the USB cable is securely attached to the raspberry pi and scale

  * Plugging HDMI while raspberry pi is already booted. Note: raspberry pi is not hot pluggable 
    * Plugin HDMI monitor
    * Restart Raspberry pi

  * Run script while connected to raspberry pi
    * Open terminal
    * Execute command $ python circularBuffer_latest.py
    
  * Distorted video feed
    *  If the camera module cable is wrapped too tightly onto itself, the video feel will be distorted due to interference. 
