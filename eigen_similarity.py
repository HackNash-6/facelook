__author__ = 'dgilmore'

import os

import cv2
import numpy as np


def compare_similarity(path, prefix):
    pass

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


rootdir = 'images/'
images = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        images.append(rootdir + '/' +  file)
size = len(images)
labels = []
for x in range(0, size/3):
    labels.append(x)
xlabel = []

for x in labels:
    xlabel.append(x)
    xlabel.append(x)
    xlabel.append(x)
lookup_dic = {}
for x in images:
    lookup_dic[xlabel[images.index(x)]] = x

print lookup_dic


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


def gray_images(images):
    gray_scale = []
    for x in images:
        gray_scale.append(np.asarray(cv2.imread(x, cv2.IMREAD_GRAYSCALE), dtype=np.uint8))
    return gray_scale


gray_image = gray_images(images)
train_set = []
for x in gray_image:
    train_set.append(detectFace(x))

print train_set[0]

model = eigenfaces(train_set, xlabel)

prediction = predict_face(model, train_set[0])

#### Testing the model with my face ###
t = np.asarray(cv2.imread('picd_us-6.jpg', cv2.IMREAD_GRAYSCALE), dtype=np.uint8)
#my_photo = gray_images('picd_us-6.jpg')
my_face = []
my_face.append(t)
print t


# In[63]:

test_set = []
test_set.append(detectFace(my_face[0]))


# In[65]:

my_prediction = predict_face(model, test_set[0])
print my_prediction


# In[75]:

model.getMat('mean')[0][3]


# In[76]:

def fisherfaces(images, labels):
    testing = []
    tLabels = np.asarray(labels, dtype=np.int32)
    #  for x in images:
    #     testing.append(np.asarray(cv2.imread(x, cv2.IMREAD_GRAYSCALE), dtype=np.uint8))
    model = cv2.createFisherFaceRecognizer()
    #  model.train(testing, tLabels)
    model.train(images, tLabels)
    print model
    return model

fisher_model = fisherfaces(train_set, xlabel)

prediction = predict_face(fisher_model, train_set[1])

my_fisher_face = predict_face(fisher_model, test_set[0])
print my_fisher_face

lookup_dic[my_fisher_face[0]]

#### Testing someone who is already in the model.
j = np.asarray(cv2.imread('jLawrenceTest.jpg', cv2.IMREAD_GRAYSCALE), dtype=np.uint8)
test_j = detectFace(j)

print 'Eigenfaces prediction:'
eigen_prediction = predict_face(model, test_j)
print lookup_dic[eigen_prediction[0]]
print 'Fisher prediction:'
fisher_prediction = predict_face(fisher_model, test_j)
print lookup_dic[fisher_prediction[0]]

def find_top_5(image, images, labels):
    eigen_training_images = images
    eigen_training_labels = labels
    fisher_training_images = images
    fisher_training_labels = labels
    eigen_predictions = []
    fisher_predictions = []
    for x in range(0, 5):
        eigen_model = eigenfaces(eigen_training_images, eigen_training_labels)
        fisher_model = fisherfaces(fisher_training_images, fisher_training_labels)
        eigen_predictions.append(predict_face(eigen_model, image))
        fisher_predictions.append(predict_face(fisher_model, image))
        for y in range(0, 3):
            eigen_training_images.pop(eigen_training_labels.index(eigen_predictions[x][0]))
            print eigen_training_images
            eigen_training_labels.pop(eigen_predictions[x][0])
            fisher_training_images.pop(fisher_training_labels.index(fisher_predictions[x][0]))
            fisher_training_labels.pop(fisher_predictions[x][0])
    print 'Eigenfaces:'
    for x in eigen_predictions:
        print x

    print 'Fisher faces:'
    for x in fisher_predictions:
        print x
    return (eigen_predictions, fisher_predictions)

import pandas

clean_images = []
for x in images:
    lhs, rhs = x.split(rootdir)
    clean_images.append(rhs)
d = {'imagesm': train_set, 'images': clean_images, 'labels': xlabel}

df = pandas.DataFrame(data=d)
df

def eigen_find_top_5_df(image, dataframe):
    eigen_training_images = dataframe['imagesm']
    eigen_training_labels = dataframe['labels']
    #fisher_training_images = images
    #fisher_training_labels = labels
    eigen_predictions = []
    #fisher_predictions = []
    for x in range(0, 5):
        eigen_model = eigenfaces(eigen_training_images, eigen_training_labels)
        #fisher_model = fisherfaces(fisher_training_images, fisher_training_labels)
        eigen_predictions.append(predict_face(eigen_model, image))
        #fisher_predictions.append(predict_face(fisher_model, image))

        #   eigen_training_images.pop(eigen_training_labels.index(eigen_predictions[x][0]))
        dataframe = dataframe.ix[dataframe['labels'] != eigen_predictions[x][0]]
        eigen_training_images = dataframe['imagesm']
        eigen_training_labels = dataframe['labels']
        #   print eigen_training_images
        #  eigen_training_labels.pop(eigen_predictions[x][0])
        #  fisher_training_images.pop(fisher_training_labels.index(fisher_predictions[x][0]))
        # fisher_training_labels.pop(fisher_predictions[x][0])
    print 'Eigenfaces:'
    for x in eigen_predictions:
        print x

        # print 'Fisher faces:'
        #for x in fisher_predictions:
        #   print x
    return eigen_predictions

e_p = eigen_find_top_5_df(test_j, df)

for x in e_p:
    print df.ix[df['labels'] == x[0]]
