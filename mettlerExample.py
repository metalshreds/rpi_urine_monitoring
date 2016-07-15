from mettler_toledo_device import MettlerToledoDevice
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
