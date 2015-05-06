import cv2
import sys
import os
import subprocess


def del_bad_faces():
    """Searches a directory for photos with non-faces (ie profile shots, no face in photo.
       deletes bad photos via subprocess.call.  Usage: 'remove_badfaces.py image_directory'
    """
    def is_bad_face(filename):
        """:param filename: (string) file name ending in .jpg or .png
           :returns: (boolean) True if photo does not have an acceptable view of at least one face
        """
        print('evaluating {}'.format(filename))
        # Ignore hidden files
        if os.path.basename(os.path.abspath(filename)).startswith('.'):
            return False

        assert(filename[-3:] in ['jpg', 'png'])
        imagePath = '{}/{}'.format(sys.argv[1], filename) 
        cascPath = 'haarcascade_frontalface_default.xml'

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)

        # Read the image

        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

             
        if len(faces) < 1:
            return True
        return False        


    pics = os.listdir(sys.argv[1])
    bad_faces = [pic for pic in pics if is_bad_face(pic)]

    for bad in bad_faces:
        del_path = '/'.join([sys.argv[1], bad])
        subprocess.call(['rm', del_path])
   
  
del_bad_faces()







