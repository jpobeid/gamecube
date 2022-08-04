import usb_reader as usb_gc
import controller as gc
import time
import RPi.GPIO as GPIO
import usb.core

GPIO.setmode(GPIO.BOARD)

PIN_RELAY = 37
GPIO.setup(PIN_RELAY, GPIO.OUT)

endpoint = usb_gc.get_controller_endpoint()

def toggle(pin, signal):
    if signal and GPIO.input(pin) == 0:
        print(f'Turning on pin {pin}...')
        GPIO.output(pin, True)
    elif not signal and GPIO.input(pin) == 1:
        print(f'Turning off pin {pin}...')
        GPIO.output(pin, False)

while True:
    time.sleep(0.05)
    try:
        raw_bytes = endpoint.read(8)[:-1] # Only 7 bytes are pertinent, last is always 0
    except usb.core.USBError as e:
        print(e)
        print('Cleaning up...')
        GPIO.cleanup()
        break
    controller_output = gc.interpret(raw_bytes)
    signal_A = 'A' in  controller_output.get('Main')
    signal_B = 'B' in controller_output.get('Main')
    signal_C_up = controller_output.get('C-stick')[-1] > 0
    signal_C_down = controller_output.get('C-stick')[-1] < 0
    toggle(PIN_RELAY, signal_A)
    signal_close = 'Home' in controller_output.get('Center')
    if signal_close:
        GPIO.cleanup()
        print('Shutting down...')
        break
