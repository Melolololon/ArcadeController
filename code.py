#  SPDX-FileCopyrightText: 2021 Jeff Epler for Adafruit Industries
# 
#  SPDX-License-Identifier: MIT

import keypad
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.keycode import Keycode

key_pins = [
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
    board.GP26,
]

keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)

class BitmapKeyboard(Keyboard):
    def __init__(self, devices):
        device = find_device(devices, usage_page=0x1, usage=0x6)

        try:
            device.send_report(b'\0' * 16)
        except ValueError:
            print("found keyboard, but it did not accept a 16-byte report. check that boot.py is installed properly")

        self._keyboard_device = device

        #  report[0] modifiers
        #  report[1:16] regular key presses bitmask
        self.report = bytearray(16)

        self.report_modifier = memoryview(self.report)[0:1]
        self.report_bitmap = memoryview(self.report)[1:]

    def _add_keycode_to_report(self, keycode):
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            #  Set bit for this modifier.
            self.report_modifier[0] |= modifier
        else:
            self.report_bitmap[keycode >> 3] |= 1 << (keycode & 0x7)

    def _remove_keycode_from_report(self, keycode):
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            #  Set bit for this modifier.
            self.report_modifier[0] &= ~modifier
        else:
            self.report_bitmap[keycode >> 3] &= ~(1 << (keycode & 0x7))
        
    def release_all(self):
        for i in range(len(self.report)):
            self.report[i] = 0
        self._keyboard_device.send_report(self.report)

 
from board import *
import rotaryio
import usb_hid
import digitalio
import board
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode

# キーコード https://docs.circuitpython.org/projects/hid/en/4.1.6/api.html

#                                             Start    Select
#
#            Up1      Up2      Up3      Up4
#   Stick    Down1    Down2    Down3    Down4
#

# 3ボタン                                                                               Down1     Up1           Up2       Up3       Up4       Down4     Down2     Down3     Start          Select
keyCodes = [Keycode.UP_ARROW,Keycode.DOWN_ARROW,Keycode.LEFT_ARROW,Keycode.RIGHT_ARROW,Keycode.P,Keycode.SHIFT,Keycode.X,Keycode.Z,Keycode.B,Keycode.N,Keycode.M,Keycode.A,Keycode.ESCAPE,Keycode.S]
# 4ボタン                                                                                Down1     Up1           Up2       Up3       Up4       Down4     Down2     Down3     Start          Select
keyCodes2 = [Keycode.UP_ARROW,Keycode.DOWN_ARROW,Keycode.LEFT_ARROW,Keycode.RIGHT_ARROW,Keycode.Z,Keycode.SHIFT,Keycode.X,Keycode.C,Keycode.B,Keycode.N,Keycode.M,Keycode.A,Keycode.ESCAPE,Keycode.S]

kbd = BitmapKeyboard(usb_hid.devices)

# 除数
DIVISOR = 1
encoder = rotaryio.IncrementalEncoder(GP0,GP1,DIVISOR)
# 前フレームの位置(変化確認用)
prePos = 0

# モード
# 0 3ボタンモード
# 1 4ボタンモード
mode = 0

def checkButton():
    global mode
    
    ev = keys.events.get()
    if ev is not None:
        if mode == 0:
            key = keyCodes[ev.key_number]
        else:
            key = keyCodes2[ev.key_number]
        if ev.pressed:
            if key == Keycode.B:
                mode = 0
            elif key == Keycode.N:
                mode = 1
            else:
                kbd.press(key)
        else:
            kbd.release(key)

# パドルコントローラー用
def checkEncoder():
        
while True:
    # ボタン処理
     checkButton()
    


