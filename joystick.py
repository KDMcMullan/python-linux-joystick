#!/usr/bin/python3

from time import sleep
from struct import Struct

jsOK =  True
devJS = "/dev/input/js0"

try:
  js = open(devJS,"rb")
except:
  print(f"No device found: {devJS}")
  jsOK = False

#struct js_event {
#  __u32 time;     /* event timestamp in milliseconds */
#  __s16 value;    /* value */
#  __u8 type;      /* event type */
#  __u8 number;    /* axis/button number */
#};

s = Struct("I h c c")

maxButtons = 0
maxAxes = 0

buttons = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
axes = [0,0,0,0,0,0,0,0]

while True:
  jsDat = s.unpack(js.read(8))

  jsTime = jsDat[0]
  jsVal = jsDat[1]
  jsType = int.from_bytes(jsDat[2],"big")
  jsIndex = int.from_bytes(jsDat[3],"big")

  if jsType == 0x81: # button init
    maxButtons = jsIndex # I hope they appear in ascending order
    print(f"maxButtons: {maxButtons}")

  elif jsType == 0x82: # axis init
    maxAxes = jsIndex
    print(f"maxAxes: {maxAxes}")

  elif jsType == 0x01: # button event
    buttons[jsIndex] = jsVal

  elif jsType == 0x02: # axis event
    axes[jsIndex] = jsVal

  else:
    print(f"Unhandled Type: {jsType}")

#  print(jsTime, jsVal, jsType, jsIndex)
  print(axes,buttons)

  sleep(.01)