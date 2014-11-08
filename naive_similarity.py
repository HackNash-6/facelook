import os
import requests
from PIL import Image
from numpy import average, linalg, dot


# In[ ]:
#
# def download_file(url, filepath):
# _USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
#     headers = { 'user-agent': _USER_AGENT }
#     r = requests.get(url, headers=headers, timeout=60, stream=True)
#     with open(filepath, 'wb') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
#                 f.flush()
#     return filepath
#
#
# # In[66]:
#
# image_urls = [
#     'http://celebritydb.net/images/1407162060_59511.jpg',
#     'http://celebritydb.net/images/1407162123_18383.jpg',
#     'http://images.agoramedia.com/everydayhealth/gcms/celebrity-sleep-disorders-Jennifer-Aniston-pg-full.jpg'
# ]
#
# for line in image_urls:
#     download_file(line, 'images/' + line.split('/')[-1])


# In[67]:

image_count = 1


# In[68]:

# def similarity(url):
#
#     global image_count
#     path = 'tmp/{0}_.jpg'.format(image_count)
#     download_file(url, path)
#     image_count += 1
#
#     return compare_similarity(path)

def compare_similarity(path, prefix):
    largest_similarity = 0.0
    matching_images = ()

    image_comparison_dict = {
        'similarity': largest_similarity,
        'images': []
    }

    for f in os.listdir('images/'):
        similarity = image_similarity_vectors_via_numpy(path, 'images/' + f)
        if similarity > largest_similarity:
            largest_similarity = similarity
            matching_images = (prefix + f, similarity)
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

    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # If we did not resize the images to be equal, we would get an error here
    # ValueError: matrices are not aligned
    res = dot(a / a_norm, b / b_norm)
    return res


def get_thumbnail(image, size=(128, 128), greyscale=False):
    #get a smaller version of the image - makes comparison much faster/easier
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        #convert image to greyscale
        image = image.convert('L')
    return image


# # In[69]:
#
# print similarity('http://www.eonline.com/resize/300/300/www.eonline.com/eol_images/Entire_Site/201488/rs_300x300-140908133055-600-megan-fox-turtles-sydney.ls.98114.jpg')
#
