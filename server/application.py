from flask import Flask, render_template, send_file, Response, request, jsonify
import os

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join("../","client","static"))

@app.route('/', methods=['GET'])
def render_index():
    return send_file(os.path.join("../","client","index.html"))


@app.route('/getinfo', methods=['POST'])
def get_video_info():
    url = request.args['url']
    # url contains the url string
    # Do whatever you gotta do with it here
    return url