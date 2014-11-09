__author__ = 'dgilmore'


# coding: utf-8

# In[ ]:

import os
import errno
import shutil
import itertools
import requests

from PIL import Image
import numpy as np
from numpy import average, linalg, dot, mean
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from scipy.spatial.distance import cosine
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline

model = None


def compare_similarity(path, prefix):
    return rbm_similarity(path)


def rbm_similarity(path):

    if model is None:
        images = []
        for f in os.listdir('images/'):
            if f != '.DS_Store':
                images.append((get_thumbnail(Image.open('images/{0}'.format(f))), f))

        image_matrix = []
        for image, path in images:
            vectors = []

            for pixel_tuple in image.getdata():
                vec = []
                for val in pixel_tuple:
                    vec.append(float(val))
                vectors.append(vec)
            image_matrix.append(vectors)


        train(image_matrix, images)

    scores = model['matrix']
    sim = []
    new_pred = train_new(path)
    for i in xrange(len(scores)):
        sim.append({
            'score': 1. - cosine(new_pred.mean(0), scores[i].mean(0)),
            'image': images[i][1]
        })
    print sim

    return sim


def get_thumbnail(image, size=(4, 4), greyscale=False):
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        image = image.convert('L')
    return image


def eigenfaces(images, labels):
    testing = []
    tLabels = np.asarray(labels, dtype=np.int32)
    #  for x in images:
    #     testing.append(np.asarray(cv2.imread(x, cv2.IMREAD_GRAYSCALE), dtype=np.uint8))
    model = cv2.createEigenFaceRecognizer()
    #  model.train(testing, tLabels)
    model.train(images, tLabels)
    print model
    return model


def predict_face(model, image):
    predicted_label = model.predict(image)
    print predicted_label
    return predicted_label


def detectFace(raw_image):
    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        raw_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        new_image = cv2.resize(raw_image[y:y+h,x:x+w],(100,100))
    return new_image

def train_new(path):

    thumbnail = get_thumbnail(Image.open('images/{0}'.format(path)))

    vectors = []
    for pixel_tuple in thumbnail.getdata():
        vec = []
        for val in pixel_tuple:
            vec.append(float(val))
        vectors.append(vec)

    X = np.asarray(vectors, 'float32')
    Y = np.array(X.shape)
    X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)

    rbm = BernoulliRBM(random_state=1, verbose=True)
    rbm.learning_rate = 0.09
    rbm.n_iter = 1
    rbm.n_components = 16
    rbm.batch_size = 2

    return rbm.fit(X).components_


def train(image_matrix, images):

    X = np.asarray(image_matrix, 'float32')
    Y = np.array(X.shape)
    X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)

    rbm = BernoulliRBM(random_state=1, verbose=True)
    rbm.learning_rate = 0.09
    rbm.n_iter = 1
    rbm.n_components = 16
    rbm.batch_size = 2

    y_new = np.zeros(X.shape)
    for i in range(len(X)):
        x_new = rbm.fit(X[i])
        y_new[i] = x_new.components_

    global model
    model = {
        'matrix': y_new,
        'images': images
    }

if __name__ == '__main__':
    compare_similarity('me.color.jpg', '')
