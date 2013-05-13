import serial
import sys
import time
import math
import os
# import subprocess
import platform


# appscript import for key events
# from appscript import app, k
# os = ""
# if "Darwin" in platform.platform():
#     os = "osx"
# else:
#     os = "windows"

def next_slide():
    # cmd = """osascript<<END
    # tell application "Microsoft PowerPoint" to go to next slide (slide show view of slide show window 1)

    # END"""
    cmd = """osascript -e 'tell application "Microsoft PowerPoint" to go to next slide (slide show view of slide show window 1)'"""
    
    os.system(cmd)

def previous_slide():
    # cmd = """osascript<<END
    # tell application "Microsoft PowerPoint"
    #     go to previous slide (slide show view of slide show window 1)
    # end tell
    # END"""

    cmd = """osascript -e 'tell application "Microsoft PowerPoint" to go to previous slide (slide show view of slide show window 1)'"""
    os.system(cmd)
    # print p
    # p.terminate()

ports = ["/dev/cu.usbmodem411", 
	"/dev/tty.usbmodem411", 
	"/dev/tty.usbmodem641", 
	"/dev/cu.usbmodem641"]



ser = None
for port in ports:
	try:
		ser = serial.Serial(port, 9600)
		break
	except Exception:
		print "no Arduino in %s" % (port)

if ser is None:
	sys.exit(1)

C = ["X", "Y", "Z"]
# Movement tags:
# F=Forwards, B=Backwards
# L=Left, R=Right
# U=Up, D=Down
M = [ ("F", "B"), ("L", "R"), ("U", "D") ]
# Direction vector
D = ["", "", ""]
# Force vector
F = [0.0, 0.0, 0.0]
# The average value of each value
mean = [0.00,0.0,0.00]

# To be registered by the system as a direction movement
# the movement vector has to be larger than its 
# delta vector
delta =[0.07, 0.07, 0.0]
# noise_delta = 40

# ON / OFF status
normal = 0
inactive = 1

# continuous scroll
L = 2
R = 3

# repeat delta
tick = 1
stateTIME = 0.0
lastSTATE = normal

def stateSwitch(direction, lastSTATE, stateTIME):
    x, y, z = direction
    if y != "-":
        if y == "L":
            return left(lastSTATE, stateTIME)
        if y == "R":
            return right(lastSTATE, stateTIME)
    return normal, stateTIME

def left(LastSTATE, stateTIME):
    # if this not a repeat state
    if LastSTATE != L:
        # print LastSTATE
        stateTIME = time.time()
        # previous_slide()
        return L, stateTIME

    t1 = time.time()
    delta = t1 - stateTIME
    if delta >= tick:
        print "Repeat: %s: t=%.2f" % (lastSTATE, delta)
        previous_slide()
        # reset time
        stateTIME = t1
        return L, stateTIME
    # no action, but state unchanged
    return L, stateTIME

def right(lastSTATE, stateTIME):
    # if this not a repeat state
    if lastSTATE != R:
        # print lastSTATE
        stateTIME = time.time()
        # next_slide()
        return R, stateTIME

    t1 = time.time()
    delta = t1 - stateTIME
    if delta >= tick:
        print "Repeat: %s: t=%.2f" % (lastSTATE, delta)
        next_slide()
        # reset time
        stateTIME = t1
        return R, stateTIME
    # no action, but state unchanged
    return R, stateTIME

if __name__ == "__main__":
    while True:
        line = ser.readline().split("\t")
        if len(line) < 3:
            while len(ser.readline().split("\t")) < 3:
                time.sleep(1)

        # normalize the values to be [+511;-512]
        try:
            V = ((int(line[0])-512)/-512.0,  
                 (int(line[2])-512)/-512.0,
                 (int(line[1])-512)/-512.0,
                 )
        except Exception:
            continue

        for i in xrange(len(V)):
            if abs(V[i]) > delta[i]:
                D[i] = M[i][0] if V[i] > 0 else M[i][1]
            else:
                D[i] = "-"

        lastSTATE, stateTIME = stateSwitch(D, lastSTATE, stateTIME)

        print "(%1s,%1s,%1s) - STATE: %s, stateTIME: %.2f" % (D[0],D[1],D[2], lastSTATE, stateTIME)

