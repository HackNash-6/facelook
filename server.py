from flask import Flask
from flask import request
import flask
from naive_similarity import compare_similarity
import os
import tempfile

app = Flask(__name__)


@app.route('/similarity', methods=['POST'])
def find_similar_images():
    prefix = request.url_root + 'images/'
    if request.headers['Content-Type'] == 'application/octet-stream':
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(request.data)
        f.close()
        similarity = compare_similarity(os.path.abspath(f.name), prefix)
        return flask.jsonify(similarity)

    else:
        return "415 Unsupported Media Type ;)"


@app.route('/images/<image_name>')
def lookup_image(image_name=None):
    return flask.send_file('images/' + image_name, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run()