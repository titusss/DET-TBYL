import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/Users/xiaobaiji/Desktop/gcp.json"
from google.cloud import vision

import cv2
from gaze_tracking import GazeTracking
import io
import time

os.system('cls||clear')

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # print(time.time())
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

    # cv2.putText(new_frame, str(time.time()), (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)
    print(text)

    image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    image = vision.Image(content=image_bytes)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        print('blurred: {}'.format(likelihood_name[face.blurred_likelihood]))
        print('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    print(time.time())

    if cv2.waitKey(1) == 27:
        break
