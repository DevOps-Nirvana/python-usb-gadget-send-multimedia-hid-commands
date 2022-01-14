#!/usr/bin/env python3
import os
import time
from optparse import OptionParser

# What HID device to use, defaults to hidg0 for easier/less configuration
DEFAULT_HID = '/dev/hidg0'
# Note: Multimedia devices are hardcoded to send the control code of 0x02
#       in contrast to keyboard stuff which lives on 0x00, the other thing
#       that differs for multimedia devices is using the reserved bit [1]
#       for the button code, instead of [2] which keyboards use
CONTROL_CODE = 0x02
DEBUG = False

KEYS_ALLOWED = {
  'WAKE':           {'rsvd': 0,  'ctrl': 0x00,         'kbd': 0x81, 'delay': 2,   'ctrl': 0x00},         # Basically just send a "empty/invalid" keypress, to "wake" whatever device before sending a real key below
  'SCRUB_FORWARD':  {'rsvd': 1,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 1.2, 'ctrl': CONTROL_CODE}, # Basically, a "long-press" of the next-song button, about 1.2 seconds seems to be the most reliable
  'FORWARD':        {'rsvd': 1,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 1.2, 'ctrl': CONTROL_CODE}, # Alias of above
  'SCRUB_BACKWARD': {'rsvd': 2,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 1.2, 'ctrl': CONTROL_CODE}, # Basically, a "long-press" of the previous-song button
  'BACKWARD':       {'rsvd': 2,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 1.2, 'ctrl': CONTROL_CODE}, # Alias of above
  'NEXT_SONG':      {'rsvd': 1,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE},
  'NEXT':           {'rsvd': 1,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE}, # Alias of above
  'PREVIOUS_SONG':  {'rsvd': 2,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE},
  'BACK':           {'rsvd': 2,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE}, # Alias of above
  'STOP':           {'rsvd': 4,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE}, # Not all devices respond to this, Eg: iPads do not.  Use play(pause) below
  'PLAY':           {'rsvd': 8,  'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE}, # This is play/pause, but simplified the name
  'MUTE':           {'rsvd': 16, 'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE}, # This acts as mute and unmute, simplified the name
  'VOLUME_UP':      {'rsvd': 32, 'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE},
  'VOLUME_DOWN':    {'rsvd': 64, 'ctrl': CONTROL_CODE, 'kbd': 0x00, 'delay': 0.1, 'ctrl': CONTROL_CODE},
}

# Helper script to send data directly to our HID Gadget emulation device
def send_to_gadget(hid_path, reserved_code, control_code=CONTROL_CODE, keyboard_code=0x00):
    if DEBUG:
        print("Sending {}:{}:{} to {}".format(control_code, reserved_code, keyboard_code, hid_path))

    with open(hid_path, 'wb+') as hid_handle:
        buf = [0] * 8
        buf[0] = control_code
        buf[1] = reserved_code
        buf[2] = keyboard_code
        hid_handle.write(bytearray(buf))
        hid_handle.write(bytearray([0] * 8))

# Helper script to translate KEYS_ALLOWED into the above
def send(key_name, hid_path=DEFAULT_HID):
    if DEBUG:
        print("Requested to send {} to {}".format(key_name, hid_path))
    # Sending keypress (down)
    send_to_gadget(hid_path, reserved_code=KEYS_ALLOWED[key_name]['rsvd'], control_code=KEYS_ALLOWED[key_name]['ctrl'], keyboard_code=KEYS_ALLOWED[key_name]['kbd'])
    # Wait
    if DEBUG:
        print("Waiting {} second(s)...".format(KEYS_ALLOWED[key_name]['delay']))
    time.sleep(KEYS_ALLOWED[key_name]['delay'])
    # Send end of keypress (up)
    send_to_gadget(hid_path, reserved_code=0)


# If run via the CLI
if __name__ == '__main__':
    # Setup usage arguments/switches
    usage = "usage: %prog -k VOLUME_UP"
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--keypress",
                      dest="keypress",
                      default="",
                      help="Key to send to USB Gadget Keyboard device, must be one of ({})".format(", ".join(KEYS_ALLOWED)),
                     )
    parser.add_option("-d", "--hid-device",
                      dest="device",
                      default=DEFAULT_HID,
                      help="What HID device to use (Default: {})".format(DEFAULT_HID),
                     )
    parser.add_option("-v", "--verbose",
                      dest="verbose",
                      action="store_true",
                      default=False,
                      help="If we want to print some more stuff, it's fairly quiet without this"
                     )
    parser.add_option("-w", "--wake",
                      dest="wake",
                      action="store_true",
                      default=False,
                      help="""If we want to send an internal/unprintable/unused keypress to trigger a 'wake' on the device
(eg. iPad) before sending the desired key press, this can be useful on devices which sleep for battery/energy purposes to wake them first
so they fully process the keypress.  Eg: While asleep on an iPad if you press 'next song' it will simply wake, and not go to the next song"""
                     )
    (options, args) = parser.parse_args()

    #### Startup simple checks...
    # Validate keypress is set validly
    if options.keypress == "":
        print("ERROR: You MUST specify the keypress to send to an USB Gadget HID device with -k")
        parser.print_usage()
        exit(1)
    if options.keypress not in KEYS_ALLOWED:
        print("ERROR: You MUST specify the a valid keypress from this list: ({})".format(", ".join(KEYS_ALLOWED)))
        parser.print_usage()
        exit(1)
    # Validate device is set, this is set by default though, but just incase
    if options.device == "":
        print("ERROR: There somehow isn't an valid device specified.  Please specify one with -d")
        parser.print_usage()
        exit(1)
    # If we want to print out what we're doing as we're doing it
    if options.verbose:
        DEBUG=True
    # If we want to send an unprintable escape sequence ahead of time to "wake" the device (Eg: iPad energy saving mode)
    if options.wake:
        send('WAKE', options.device)

    # Finally, send our desired command
    send(options.keypress, options.device)
