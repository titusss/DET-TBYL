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
    print(time.time())
    _, frame = webcam.read()
    gaze.refresh(frame)
    client = vision.ImageAnnotatorClient()

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    try:
        horizontalRatio = gaze.horizontal_ratio()
        verticallRatio = gaze.vertical_ratio()
    except:
        print('okay, no ratio available')
        horizontalRatio = -1
        verticallRatio = -1

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)
    print(text)

    image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    image = vision.Image(content=image_bytes)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    anger_likelihood = "N"
    joy_likelihood = "N"
    surprise_likelihood = "N"
    sorrow_likelihood = "N"
    
    detected = False
    max_key = "sleepy"

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        # print('blurred: {}'.format(likelihood_name[face.blurred_likelihood]))
        # print('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))

        anger_likelihood = likelihood_name[face.anger_likelihood]
        joy_likelihood = likelihood_name[face.joy_likelihood]
        surprise_likelihood = likelihood_name[face.surprise_likelihood]
        sorrow_likelihood = likelihood_name[face.sorrow_likelihood]
        
        detected = True

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in face.bounding_poly.vertices])

        # print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    dic = {"happy":translator(joy_likelihood),"sad":translator(sorrow_likelihood), "sleepy":translator(anger_likelihood)}

    if translator(joy_likelihood)<1 and translator(sorrow_likelihood)<1 and translator(anger_likelihood)<1 and detected==False:
        max_key = "neutral"
    elif detected == True:
        max_key = max(dic, key=dic.get)

    # print(max_key)
    detected = False
    
    if horizontalRatio == None:
        max_key = "neutral"
    
    text2 = str(horizontalRatio)+ ";"+str(verticallRatio)+ ";"+max_key
    print(text2)
    MESSAGE = text2.encode()
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    #Recording time to manage performance
    print(time.time())

    if cv2.waitKey(1) == 27:
        break
