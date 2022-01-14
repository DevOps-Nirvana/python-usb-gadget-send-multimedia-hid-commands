# Send Multimedia USB HID Keys via Python
As an USB Gadget in Linux

This gives a simple script with zero dependencies that can easily run on any Linux device (eg: Raspberry Pi) that
is setup to emulate an USB Gadget, and send Multimedia Key presses such as Volume Up, Play, Next Song, etc.  The author
found this code/example didn't exist and especially not in Python.

## Purpose

This code was made for some automation and integration for automation and integration of mobile devices to an Raspberry Pi.  Specifically, was designed for an iPad a shared space to allow for various input and sensors from Raspberry Pi to trigger things on the iPad.  This especially helps you do lots if you use the "Shortcuts iOS App" paired with enabling "Full Keyboard Support" on your iPad.

This code is wonderful when paired with a tool such as [Triggerhappy](https://github.com/wertarbyte/triggerhappy) to remap keys/input to other keys and forward those keyboard presses into the Host USB Device via USB Gadget mode on Linux.  This code also acts as an simple library, so it can easily be imported in other Python scripts.

## Setup

1. Setup a fresh Linux device (eg: Raspberry Pi)
1. Follow walkthrough [here](https://mtlynch.io/key-mime-pi/) to setup your device as an USB Gadget
1. Use an editor and edit the file that the above walkthrough created at `/opt/enable-rpi-hid`, update the line 35 from...

```
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > "${FUNCTIONS_DIR}/report_desc"
```
And replace it with this line which adds the extra HID device "multimedia" profile to your USB HID Gadget.  Found this info [here](https://www.stefanjones.ca/blog/arduino-leonardo-remote-multimedia-keys/).
```
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0\\x05\\x0c\\x09\\x01\\xa1\\x01\\x85\\x02\\x05\\x0c\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x07\\x09\\xb5\\x09\\xb6\\x09\\xb7\\x09\\xcd\\x09\\xe2\\x09\\xe9\\x09\\xea\\x81\\x02\\x95\\x01\\x81\\x01\\xc0 > "${FUNCTIONS_DIR}/report_desc"
```

1. After the above manual change, reboot your device
1. Plug your Linux Device into a USB host device (eg: iPhone, iPad, Mac/PC/Linux).  Note: You may need an USB "OTG" cable.  Also note: Not ALL USB ports (especially on the Raspberry Pi) can act as USB OTG, only a specific port.
1. Download this script <instructions todo here>

## Usage (CLI / Testing)

```bash
# Run the command, asking for help
./usb_gadget_multimedia_keys.py -h
# Try sending volume up
./usb_gadget_multimedia_keys.py -k VOLUME_UP
```

## Installation

To install it on your system, a good recommended place is to put it in `/usr/local/bin`.  On most Unix-ey machines,
this is already in your PATH, so you can simply download and chmod +x it to begin using it.

```
TODO
```

## Usage (Triggerhappy)

See: https://github.com/wertarbyte/triggerhappy

Using a sample configuration such as...

```
# FORMAT: <event name>	<event value>	<command line>
# This is the + key on an extended keyboard on the number pad
KEY_KPPLUS	1		./todo -k VOLUME_UP
# This is the - key on an extended keyboard on the number pad
KEY_KPMINUS	1		./todo -k VOLUME_DOWN
```

## Manual / Manpage

```bash
root@localhost$ ./usb_gadget_multimedia_keys.py  -h
Usage: usb_gadget_multimedia_keys.py -k VOLUME_UP

Options:
  -h, --help            show this help message and exit
  -k KEYPRESS, --keypress=KEYPRESS
                        Key to send to USB Gadget Keyboard device, must be one
                        of (WAKE, SCRUB_FORWARD, SCRUB_BACKWARD, NEXT_SONG,
                        PREVIOUS_SONG, STOP, PLAY, MUTE, VOLUME_UP,
                        VOLUME_DOWN)
  -d DEVICE, --hid-device=DEVICE
                        What HID device to use (Default: /dev/hidg0)
  -v, --verbose         If we want to print some more stuff, it's fairly quiet
                        without this
  -w, --wake            If we want to send an internal/unprintable/unused
                        keypress to trigger a 'wake' on the device (eg. iPad)
                        before sending the desired key press, this can be
                        useful on devices which sleep for battery/energy
                        purposes to wake them first so they fully process the
                        keypress.  Eg: While asleep on an iPad if you press
                        'next song' it will simply wake, and not go to the
                        next song
```

## Author / Support

Authored by Farley _at_ (neonsurge) **dot** com

This is considered open source code, do whatever you want with it.  File issues if you have them, or email me if you want.

## References

Loosely inspired/based on the [Key Mime Pi](https://mtlynch.io/key-mime-pi/) project and its [accompanying repo](https://github.com/mtlynch/key-mime-pi).  Key/control/gadget/device setup code found with lots of googling and research from pages found such as...
* https://www.stefanjones.ca/blog/arduino-leonardo-remote-multimedia-keys/
* https://forum.arduino.cc/t/keyboard-library-sending-multimedia-keys/428068
* https://www.instructables.com/USB-Volume-Control-and-Caps-Lock-LED-Simple-Cheap-/
* https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
* https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/consumer_control.py
* https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/consumer_control_code.py
* https://uboopenfactory.univ-brest.fr/Les-Labs/MusicLab/Projets/Arduino-Media-Keys
