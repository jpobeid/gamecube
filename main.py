import usb_reader as usb_gc
import controller as gc
import game

endpoint = usb_gc.get_controller_endpoint()

while True:
    raw_bytes = endpoint.read(8)[:-1] # Only 7 bytes are pertinent, last is always 0
    controller_output = gc.interpret(raw_bytes)
    game.play(controller_output)