__author__ = 'Geoffrey Gross'

import os
import cv2
import numpy as np
import pandas


def compare_similarity(path):
    return fisher_similarity(path)


def fisher_similarity(path):
    images = get_images()
    gray = gray_scale_images(images)
    testing_data = []
    for x in gray:
        testing_data.append(detectFace(x))
    df = to_pandas(images, testing_data, 'images/')
    #clean image
    test_image = detectFace(cv2.imread(path, cv2.IMREAD_GRAYSCALE))
    predictions = fisher_find_top_n_df(test_image, df, 5)

    biggest_weight = 0
    for x in predictions:
        if x[1] > biggest_weight:
            biggest_weight = x[1]
    sim = []
    for x in predictions:
        sim.append({
            'score': 1 - x[1]/biggest_weight,
            'image': df['images'].ix[df['labels'] == x[0]].values[0].replace('/','')
        })
    return sim



def fisherfaces(images, labels):
    tLabels = np.asarray(labels, dtype=np.int32)
    model = cv2.createFisherFaceRecognizer()
    model.train(images, tLabels)
    return model


def get_images():
    rootdir = 'images/'
    images = []

    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            path = os.path.join(subdir,f)
            match = re.search(".+1\.jpg$", path)
            if match:
                images.append(rootdir + '/' + f)
    return images


def gray_scale_images(images):
    gray_scale = []
    for x in images:
        gray_scale.append(np.asarray(cv2.imread(x, cv2.IMREAD_GRAYSCALE), dtype=np.uint8))
    return gray_scale

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


def to_pandas(image_id, image_matrix, rootdir):
    clean_images = []
    xlabel = []
    for x in image_id:
        lhs, rhs = x.split(rootdir)
        clean_images.append(rhs)
        xlabel.append(image_id.index(x))
    d = {'imagesm': image_matrix, 'images': clean_images, 'labels': xlabel}
    df = pandas.DataFrame(data=d)
    return df


def fisher_find_top_n_df(image, dataframe, num_of_celebs):
    fisher_training_images = dataframe['imagesm']
    fisher_training_labels = dataframe['labels']
    #fisher_training_images = images
    #fisher_training_labels = labels
    fisher_predictions = []
    #fisher_predictions = []
    for x in range(0, num_of_celebs):
        fisher_model = fisherfaces(fisher_training_images, fisher_training_labels)
        fisher_predictions.append(predict_face(fisher_model, image))
        dataframe = dataframe.ix[dataframe['labels'] != fisher_predictions[x][0]]
        fisher_training_images = dataframe['imagesm']
        fisher_training_labels = dataframe['labels']

    return fisher_predictions


def predict_face(model, image):
    predicted_label = model.predict(image)
    print predicted_label
    return predicted_label
