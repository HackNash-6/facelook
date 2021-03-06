import os
import tempfile
import base64
import eigen_similarity
import fisher_similarity
from PIL import Image
from io import BytesIO

from flask import Flask
from flask import request
import flask

import rbm_similarity


try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
    from flask.ext.cors import cross_origin
except ImportError:
    # Path hack allows examples to be run without installation.
    import os

    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)
    from flask.ext.cors import CORS

app = Flask(__name__)
# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
CORS(app, resources=r'/api/*', headers='Content-Type')

@app.route('/api/similarity', methods=['POST'])
def rbm_find_similar_images():
    algorithm = request.args.get('algorithm', 'rbm')
    topn = request.args.get('topn', 5)
    prefix = request.url_root + 'api/images/'
    f = tempfile.NamedTemporaryFile(delete=False)
    im = Image.open(BytesIO(base64.b64decode(request.data)))
    im.save(os.path.abspath(f.name), 'JPEG')
    f.close()
    matches = []

    path = os.path.abspath(f.name)
    if algorithm == 'rbm':
        matches = rbm_similarity.compare_similarity(path)
    elif algorithm == 'eigen':
        matches = eigen_similarity.compare_similarity(path)
    elif algorithm == 'fisher':
        matches = fisher_similarity.compare_similarity(path)
    matches.sort(key=lambda match: match['score'], reverse=True)
    for match in matches:
        name = match['image']
        match['image'] = prefix + match['image']
        match['name'] = name.replace('.jpg','').replace('_',' ')
    return flask.jsonify(results=matches[:topn])


@app.route('/api/images/<image_name>')
def lookup_image(image_name=None):
    return flask.send_file('images/' + image_name, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run()
