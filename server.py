from flask import Flask
from flask import request
import flask
from naive_similarity import compare_similarity
import os
import tempfile
import base64
from PIL import Image
from io import BytesIO

try:
    from flask.ext.cors import CORS # The typical way to import flask-cors
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
def find_similar_images():
    prefix = request.url_root + 'api/images/'
    f = tempfile.NamedTemporaryFile(delete=False)
    im = Image.open(BytesIO(base64.b64decode(request.data)))
    im.save(os.path.abspath(f.name), 'JPEG')
    f.close()
    similarity = compare_similarity(os.path.abspath(f.name), prefix)
    return flask.jsonify(similarity)


@app.route('/api/images/<image_name>')
def lookup_image(image_name=None):
    return flask.send_file('images/' + image_name, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run()