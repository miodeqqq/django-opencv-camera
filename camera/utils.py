# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np
from django.conf import settings
from django.core.files.base import ContentFile


def prepare_classifiers():
    """
    General method to prepare classifiers.
    """

    classifiers_dict = {
        'frontal_face_default': os.path.join(
            settings.BASE_DIR, 'haarcascades/haarcascade_frontalface_default.xml'
        ),
        'eyes': os.path.join(
            settings.BASE_DIR, 'haarcascades/haarcascade_eye.xml'
        ),
        'frontal_cat_face': os.path.join(
            settings.BASE_DIR, 'haarcascades/haarcascade_frontalcatface.xml'
        ),
        'frontal_cat_face_extended': os.path.join(
            settings.BASE_DIR, 'haarcascades/haarcascade_frontalcatface_extended.xml'
        ),
    }

    return classifiers_dict


def detect_barcode_on_image(instance):
    """
    General method to detect barcodes on image.
    """

    if instance.input_image:

        with open(instance.input_image.path, 'rb') as img_source:
            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                grad_x = cv2.Sobel(
                    image,
                    ddepth=cv2.cv.CV_32F,
                    dx=1,
                    dy=0,
                    ksize=-1
                )

                grad_y = cv2.Sobel(
                    image,
                    ddepth=cv2.cv.CV_32F,
                    dx=0,
                    dy=1, ksize=-1
                )

                gradient = cv2.subtract(grad_x, grad_y)
                gradient = cv2.convertScaleAbs(gradient)

                blurred = cv2.blur(gradient, (9, 9))
                (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
                closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                closed = cv2.erode(closed, None, iterations=4)
                closed = cv2.dilate(closed, None, iterations=4)

                (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(cnts) == 0:
                    return None

                c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

                rect = cv2.minAreaRect(c)

                box = np.int0(cv2.cv.BoxPoints(rect))

                cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

                image_file_name = instance.input_image.path.split('/')[-1]
                output_image_file = ContentFile(image)

                instance.output_image.save(
                    image_file_name,
                    output_image_file,
                    save=True
                )

                cv2.imwrite(os.path.join(instance.output_image.path), image)

                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))


def detect_eyes_on_image(instance):
    """
    General method to detect eyes on image.
    """

    if instance.input_image:

        classifiers = prepare_classifiers()

        with open(instance.input_image.path, 'rb') as img_source:
            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            face_cascade = cv2.CascadeClassifier(classifiers.get('frontal_face_default', None))
            eyes_cascade = cv2.CascadeClassifier(classifiers.get('eyes', None))

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(image)

                for (x, y, w, h) in faces:
                    roi = image[y:y + h, x:x + w]

                    eyes = eyes_cascade.detectMultiScale(roi)

                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), 255, 2)

                    number_of_eyes = len(eyes) if len(eyes) > 0 else u'No eyes found!'

                    instance.processing_output_info = u'Eyes found: {number_of_eyes}'.format(
                        number_of_eyes=number_of_eyes,
                    )

                image_file_name = instance.input_image.path.split('/')[-1]
                output_image_file = ContentFile(image)

                instance.output_image.save(
                    image_file_name,
                    output_image_file,
                    save=True
                )

                cv2.imwrite(os.path.join(instance.output_image.path), image)

                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))


def detect_faces_on_image(instance):
    """
    General method to detect faces in images.
    """

    if instance.input_image:

        classifiers = prepare_classifiers()

        with open(instance.input_image.path, 'rb') as img_source:
            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            face_cascade = cv2.CascadeClassifier(classifiers.get('frontal_face_default', None))

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(
                    image,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                number_of_faces = len(faces) if len(faces) > 0 else u'No faces found!'

                instance.processing_output_info = u'Faces found: {number_of_faces}'.format(
                    number_of_faces=number_of_faces,
                )

                image_file_name = instance.input_image.path.split('/')[-1]
                output_image_file = ContentFile(image)

                instance.output_image.save(
                    image_file_name,
                    output_image_file,
                    save=True
                )

                cv2.imwrite(os.path.join(instance.output_image.path), image)

                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))


def detect_cats_on_image(instance):
    """
    General method to detect cats in images.
    """

    if instance.input_image:

        classifiers = prepare_classifiers()

        with open(instance.input_image.path, 'rb') as img_source:
            img = cv2.imdecode(np.frombuffer(img_source.read(), np.uint8), -1)

            cat_face_cascade = cv2.CascadeClassifier(classifiers.get('frontal_cat_face_extended', None))

            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                cat_faces = cat_face_cascade.detectMultiScale(
                    image,
                    scaleFactor=1.3,
                    minNeighbors=10,
                    minSize=(75, 75),
                )

                for (i, (x, y, w, h)) in enumerate(cat_faces):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    cv2.putText(
                        image,
                        u'Cat #{index}'.format(
                            index=i + 1
                        ),
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 255),
                        2
                    )

                number_of_cats = len(cat_faces) if len(cat_faces) > 0 else u'No cats found!'

                instance.processing_output_info = u'Cats found: {number_of_cats}'.format(
                    number_of_cats=number_of_cats,
                )

                image_file_name = instance.input_image.path.split('/')[-1]
                output_image_file = ContentFile(image)

                instance.output_image.save(
                    image_file_name,
                    output_image_file,
                    save=True
                )

                cv2.imwrite(os.path.join(instance.output_image.path), image)

                instance.save()

            except IOError as io:
                print('Error --> {}'.format(io))
