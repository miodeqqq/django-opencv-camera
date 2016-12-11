# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np
from django.conf import settings

facePath = os.path.join(settings.BASE_DIR, 'haarcascades/haarcascade_frontalface_default.xml')
eyesPath = os.path.join(settings.BASE_DIR, 'haarcascades/haarcascade_eye.xml')

faceCascade = cv2.CascadeClassifier(facePath)
eyesCascade = cv2.CascadeClassifier(eyesPath)


def detect_eyes_on_image(instance):
    """
    General method to detect eyes on image.
    """

    if instance.image:

        with open(instance.image.path, 'rb') as img_source:

            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(image)

                for (x, y, w, h) in faces:
                    roi = image[y:y + h, x:x + w]

                    eyes = eyesCascade.detectMultiScale(roi)

                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), 255, 2)

                    instance.processing_output_info = u'Eyes found: {}'.format(len(eyes)) if len(eyes) > 0 else u'No eyes found!'

                cv2.imwrite(os.path.join(instance.image.path), image)


                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))


def detect_faces_on_image(instance):
    """
    General method to detect faces in images.
    """

    if instance.image:

        with open(instance.image.path, 'rb') as img_source:

            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    image,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.imwrite(os.path.join(instance.image.path), image)

                instance.processing_output_info = u'Faces found: {}'.format(len(faces)) if len(faces) > 0 else u'No faces found!'
                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))
