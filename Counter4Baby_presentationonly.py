import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/gcp.json"
from google.cloud import vision

import cv2
from gaze_tracking import GazeTracking
import io
import time
import socket
import subprocess
import sys

os.system('cls||clear')

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Setting up UPD communication
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

p = subprocess.Popen([sys.executable, 'websocket.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT)

os.system('pkill -f chromium-browser')
p = subprocess.Popen([sys.executable, 'chrome.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT)

def translator(str):
    if str == 'VERY_UNLIKELY':
        str = 0
    elif str == 'UNLIKELY':
        str = 1
    elif str == 'POSSIBLE':
        str = 2
    elif str == 'LIKELY':
        str = 3
    elif str == 'VERY_LIKELY':
        str = 4
    elif str == 'N':
        str = -2
    else:
        str = -1
    return str

while True: 
    time.sleep(2)
    
    text2 = str(0.5)+ ";"+str(0.5)+ ";"+"sleepy"
    print(text2)
    MESSAGE = text2.encode()
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(2)

    text2 = str(0.5)+ ";"+str(0.5)+ ";"+"happy"
    print(text2)
    MESSAGE = text2.encode()
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(2)

    text2 = str(0.5)+ ";"+str(0.5)+ ";"+"sad"
    print(text2)
    MESSAGE = text2.encode()
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(2)

