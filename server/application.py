import os
import json
import urllib.request
import urllib.parse as urlparse
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from flask import Flask, render_template, send_file, Response, request, jsonify
import xml.etree.ElementTree as ET
import math

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join("../","client","static"))

@app.route('/', methods=['GET'])
def render_index():
    return send_file(os.path.join("../","client","index.html"))


@app.route('/getinfo', methods=['POST'])
def get_video_info():
    # url contains the url string
    # url = request.args['url']
    url = 'https://www.youtube.com/watch?v=3yLXNzDUH58'
    # Get the video id
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]

    # Create URL for transcript
    transcript_url = "http://video.google.com/timedtext?lang=en&v="+video_id
    print(transcript_url)
    #  get transcript xml sheet from transcript_url
    transcript_response = urllib.request.urlopen(transcript_url).read()
    tree = ET.fromstring(transcript_response)

    assert(tree.tag == 'transcript')
    timed_transcript = {}

    for node in tree.iter('text'):
        print(node.attrib)
        start_time = round(float(node.attrib['start']))
        timed_transcript[start_time] = node.text

    print(timed_transcript)

    #IBM Watson NLU
    # authenticator = IAMAuthenticator('{apikey}')
    # natural_language_understanding = NaturalLanguageUnderstandingV1(
    #     version='2020-08-01',
    #     authenticator=authenticator
    # )

    # natural_language_understanding.set_service_url('{url}')

    # response = natural_language_understanding.analyze(
    #     url=transcript_url,
    #     features=Features(keywords=KeywordsOptions(sentiment=False,emotion=False,limit=5))).get_result()

    # print(json.dumps(response, indent=2))

    return url

get_video_info()