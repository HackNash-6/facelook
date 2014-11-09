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
from numpy import average, linalg, dot
import matplotlib.pyplot as plt

from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline



def compare_similarity(path):
    largest_similarity = 0.0
    matching_images = ()

    image_comparison_dict = {
        'similarity': largest_similarity,
        'images': []
    }

    for f in os.listdir('images/'):
        if path.split('/')[1] != f and f != '.DS_Store':
            similarity = image_similarity_vectors_via_numpy(path, 'images/' + f)
            if similarity > largest_similarity:
                largest_similarity = similarity
                matching_images = (f, similarity)
                image_comparison_dict = {
                    'similarity': largest_similarity,
                    'images': matching_images
                }

    return image_comparison_dict

def image_similarity_vectors_via_numpy(filepath1, filepath2):

    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)

    greatest = 0.

    images = [image1, image2]
    image_matrix = []
    norms = []
    for image in images:
        vectors = []

        for pixel_tuple in image.getdata():
            vec = []
            for val in pixel_tuple:
                vec.append(float(val))
            vectors.append(vec)
        image_matrix.append(vectors)

    return res

def get_thumbnail(image, size=(30,30), greyscale=False):
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        image = image.convert('L')
    return image


# In[210]:

images = []
for f in os.listdir('../facelook/images/'):
    if f != '.DS_Store':
        images.append((get_thumbnail(Image.open('../facelook/images/{0}'.format(f))), f))

image_matrix = []
for image, path in images:
    vectors = []

    for pixel_tuple in image.getdata():
        vec = []
        for val in pixel_tuple:
            vec.append(float(val))
        vectors.append(vec)
    image_matrix.append(vectors)


# In[211]:

X = np.asarray(image_matrix, 'float32')
Y = np.array(X.shape)
X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling


# In[212]:

rbm = BernoulliRBM(random_state=1, verbose=False)
rbm.learning_rate = 0.09
rbm.n_iter = 10
rbm.n_components = 900
rbm.batch_size = 2

y_new = np.zeros(X.shape)
for i in range(len(X)):
    x_new = rbm.fit(X[i])
    y_new[i] = x_new.components_


# In[215]:

from scipy.spatial.distance import cosine
from numpy import mean

maximum = (0, '')
for i in xrange(len(y_new)):
    sim = (1. - cosine(y_new[0].mean(0), y_new[i].mean(0)), images[i][1])
    print sim
    if sim[0] > maximum[0] and not sim[0] >= 1:
        maximum = sim

print maximum


# In[ ]:



