from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/similarity', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run()