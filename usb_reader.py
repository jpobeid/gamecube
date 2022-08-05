import usb.core
import time

VID = 0x20d6
PID = 0xa711
INTERFACE_CONTROLLER = 0
N_SLEEP = 1

def get_controller_endpoint():
    dev = None

    print('Checking for controller...')
    while dev is None:
        # Repeatedly check if controller plugged in, at N_SLEEP second intervals
        dev = usb.core.find(idVendor=VID, idProduct=PID)
        if dev is None:
            time.sleep(N_SLEEP)
        else:
            print('Detected controller...')
            break

    if dev.is_kernel_driver_active(INTERFACE_CONTROLLER):
        dev.detach_kernel_driver(INTERFACE_CONTROLLER)

    dev.reset()
    dev.set_configuration()

    conf = dev.get_active_configuration()
    endpt_in = conf.interfaces()[0].endpoints()[1]

    return endpt_in