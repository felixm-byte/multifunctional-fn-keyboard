import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode, LEDCode
from machine import Pin,SPI
import time
import pickle
from st7735 import TFT
from st7735 import sysfont
import math
import _thread
import gc

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None) #mosi is the same as SDA
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


KEYS = (
    (Pin.CPU.GPIO0, "Y"),
    (Pin.CPU.GPIO1, "X"),
    (Pin.CPU.GPIO2, "B"),
    (Pin.CPU.GPIO3, "A"),
    (Pin.CPU.GPIO4, "UP"),
    (Pin.CPU.GPIO5, "LEFT"),
    (Pin.CPU.GPIO6, "RIGHT"),
    (Pin.CPU.GPIO7, "DOWN"),
    (Pin.CPU.GPIO12, "1"),
    (Pin.CPU.GPIO13, "2"),
    (Pin.CPU.GPIO14, "3"),
    (Pin.CPU.GPIO15, "4"),
    (Pin.CPU.GPIO21, "5")
) # verify with hardware

#in this design the only LED is power, power is not connected to a GPIO pin

#the device has 2 modes - gamepad and function keyboard
#in function keyboard mode, people will not want signals to be sent multiple times even if they hold down the button - simplistic debouncing by giving a 1000ms wait until button is sent again
#in gamepad, people will want to hold down a button or mash repeatedly so a very short debouncing time should be used (20ms)
#the shortcut to switch to/from gamepad is holding down 1,2,3,4,5 simultaneously, which is almost impossible to fat finger but easy and memorable to do
REFRESH_TIME = 5
#bouncing times must be a multiple
GAMEPAD_BOUNCING_TIME = 20
KEYBOARD_BOUNCING_TIME = 1000

help_button = Pin.CPU.GPIO22
help_button.init(Pin.IN, Pin.PULL_UP)

for pin, _ in KEYS:
    pin.init(Pin.IN, Pin.PULL_UP)

class Keyboard(KeyboardInterface):
    pass #there is no custom keyboard functionality needed right now, change if needed in future

gamepad_mode = False 
keyboard = Keyboard()
mappings = {}; gamepad_mappings = {}

def display_help(keyname, keymapping):
    tft.fill(TFT.BLACK)
    v = 30
    tft.text((0, v), f"The key {keyname}", TFT.RED, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0,v), f"maps to {keymapping}", TFT.BLUe, sysfont, 2, nowrap=True)
    gc.collect()

def display_change_notice(is_in_gamepad_mode):
    tft.fill(TFT.BLACK)
    v = 30
    tft.text((0, v), f"Gamepad mode:", TFT.RED, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), f"Turned {"on" if is_in_gamepad_mode else "off"}.", TFT.RED, sysfont, 1, nowrap=True)
    gc.collect()

def load_mappings():
    global mappings
    global gamepad_mappings
    f = open("mappings.kb", 'rb')
    mappings = pickle.load(f)
    f = open("gamepad_mappings.kb", 'rb')
    gamepad_mappings = pickle.load(f)

def output_keys(ids):
    global gamepad_mode; global mappings
    keys = []
    if gamepad_mode:
        for id in ids:
            keys.append(mappings[id])
    keyboard.send_keys(keys)

usb.device.get().init(keyboard, builtin_driver=True)

previous_keys = [["none", 0], ["none, 0"]]
while True:
    if keyboard.is_open():
        keys = []
        active_keys = []
        for pin, id in KEYS:
            if not pin(): #pin must be 0 for keys to be active
                keys.append(id)
        #this may cause lag, better to cause output lag than missing keypresses
        if not help_button():
            new_thread = _thread.start_new_thread(display_help, (str(keys[0]), (gamepad_mappings if gamepad_mode else mappings)[keys[0]] ) )

        if keys == ["1", "2", "3", "4", "5"]:
            gamepad_mode = not gamepad_mode

        
        for k in range(len(previous_keys)):
            if previous_keys[k][1] + REFRESH_TIME >= (GAMEPAD_BOUNCING_TIME if gamepad_mode else KEYBOARD_BOUNCING_TIME):
                previous_keys.pop(k)
            else:
                previous_keys[k][1] += REFRESH_TIME
            
        for key_pressed in keys:
            for p in previous_keys:
                if not key_pressed == p[0]: #key has been previously pressed
                    previous_keys.append([key_pressed, 0])
                    active_keys.append(key_pressed)

        output_keys(keys)
    time.sleep_ms(REFRESH_TIME)
    


                