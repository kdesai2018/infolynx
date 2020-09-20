import os
import json
#import urllib.request
import urllib.parse as urlparse
from urllib.request import urlopen
from ibm_watson import NaturalLanguageUnderstandingV1, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions
from flask import Flask, render_template, send_file, Response, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from smart_data_fetcher import get_smart_data_for_keyword

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join("../","client","static"))
CORS(app)

UPLOADS_FOLDER = "../temp_files"

@app.route('/', methods=['GET'])
def render_index():
    return send_file(os.path.join("../","client","index.html"))


@app.route('/getinfo', methods=['GET'])
def get_video_info():
    # url contains the url string
    url = request.args['url']
    # url = "https://www.youtube.com/watch?v=O5nskjZ_GoI&list=PL8dPuuaLjXtNlUrzyH5r6jN9ulIgZBpdo&t=0s&ab_channel=CrashCourse"
    
    # Get the video id
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]

    print('Began getting info')

    # Create URL for transcript
    transcript_url = "http://video.google.com/timedtext?lang=en&v="+video_id
    print(transcript_url)
    #  get transcript xml sheet from transcript_url
    transcript_response = urlopen(transcript_url).read()
    tree = ET.fromstring(transcript_response)

    assert(tree.tag == 'transcript')
    timed_transcript = {}

    # print(url)
    print('Just before tree thing')

    for node in tree.iter('text'):
        start_time = round(float(node.attrib['start']))
        try:
            ibm_data = getKeywordsText(node.text, 1)
        except:
            continue
        
        if ibm_data and 'keywords' in ibm_data and len(ibm_data['keywords'])>=1 and ibm_data['keywords'][0]['relevance'] > 0.85:
            print(ibm_data['keywords'])
            keyword = ibm_data['keywords'][0]['text']
        else:
            continue

        google_knowledge = get_smart_data_for_keyword(keyword)
        # print(google_knowledge)
        if google_knowledge:
            # print('Got a word baby')
            timed_transcript[str(start_time)] = google_knowledge
        
    print('Done')
    # for key, val in timed_transcript.items():
        # print(str(key) + ':' + str(val))
    return jsonify(timed_transcript)

def getKeywordsURL(transcript_url):
    #IBM Watson NLU
    authenticator = IAMAuthenticator('TWS446L2CH4Zxnrh-nwh3T2g8stRlB08e4iyjAKyBHg0')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/816f28bc-9729-48ca-b11a-c736524e6ad6')

    response = natural_language_understanding.analyze(
        url=transcript_url,
        features=Features(keywords=KeywordsOptions(sentiment=False,emotion=False,limit=1), entities=EntitiesOptions(sentiment=False,limit=1))).get_result()
    return response



def getKeywordsText(text, numWords):
    #IBM Watson NLU
    try:
        # print(text)
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(keywords=KeywordsOptions(sentiment=False,emotion=False,limit=numWords), entities=EntitiesOptions(sentiment=True,limit=1))).get_result()
    except:
        response = None
        # print('HOLY SHIT SOMETHING WENT WRONG')
    return response

@app.route('/getuploadedinfo', methods=['POST'])
def get_uploaded_video_info():
    #request.files["video"] = f
    if "video" not in request.files:
        return None
    video_file = request.files["video"]
    #video_file = f
    save_location = os.path.join(UPLOADS_FOLDER, video_file.filename)
    video_file.save(save_location)
    # Convert the mp4 to an mp3
    mp3_filename = save_location.replace(".mp4", ".mp3")
    os.system("ffmpeg -y -i " + save_location + " " + mp3_filename)
    transcript = getTranscriptForUploadedAudio(mp3_filename)
    os.remove(save_location)
    os.remove(mp3_filename)
    return "goodbye"

# mp3File must come in BinaryIO format for easy upload to STT API
def getTranscriptForUploadedAudio(mp3File):
    authenticator = IAMAuthenticator('JNJkBoGNQKYihv3CPqXMtuKlgAVQcFrunct_mV2Yv4cx')
    STT_service = SpeechToTextV1(authenticator=authenticator)
    STT_service.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/816f28bc-9729-48ca-b11a-c736524e6ad6')
    with open(os.path.join(os.path.dirname('__file__'), mp3File),  'rb') as audio_file:
        transcript = STT_service.recognize(audio=audio_file, timestamps=True).get_result()
        return transcript

@app.route('/ansh', methods=['GET'])
def get_fake_data():
    # Fake data function for use by the man, the myth, the legend
    fake_dict = {"0":{"description":"A game is a structured form of play, usually undertaken for entertainment or fun, and sometimes used as an educational tool. Games are distinct from work, which is usually carried out for remuneration, and from art, which is more often an expression of aesthetic or ideological elements. ","image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5oLxa1DYPiVr1CuEVxpq7zDMWpJU47uky001jj4W3i0wsP8J9","proper_name":"Game","wikipedia_link":"https://en.wikipedia.org/wiki/Game"},"106":{"description":"A devil is the personification of evil as it is conceived in many and various cultures and religious traditions. It is seen as the objectification of a hostile and destructive force.\n","image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBStSjcYpxDGjzgyD_GLFNVMD9yfI0IgPKsUccVqt5fvQr06O6","proper_name":"Devil","wikipedia_link":"https://en.wikipedia.org/wiki/Devil"},"117":{"description":"An angel is a supernatural being in various Circum-Mediterranean religions. Abrahamic religions often depict them as benevolent celestial intermediaries between God and humanity. Other roles include protectors and guides for humans, and servants of God. ","image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcUp-gOnAob1JBySBdiNlzOFWh5Lwp42GxxGmZgkj2NYBFXzA9","proper_name":"Angel","wikipedia_link":"https://en.wikipedia.org/wiki/Angel"},"122":{"description":"A devil is the personification of evil as it is conceived in many and various cultures and religious traditions. It is seen as the objectification of a hostile and destructive force.\n","image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBStSjcYpxDGjzgyD_GLFNVMD9yfI0IgPKsUccVqt5fvQr06O6","proper_name":"Devil","wikipedia_link":"https://en.wikipedia.org/wiki/Devil"},"167":{"description":"In science and mathematics, an open problem or an open question is a known problem which can be accurately stated, and which is assumed to have an objective and verifiable solution, but which has not yet been solved.\n","proper_name":"Open problem","wikipedia_link":"https://en.wikipedia.org/wiki/Open_problem"},"206":{"description":"Thanksgiving Day is a national holiday celebrated on various dates in the United States, Canada, Brazil, Grenada, Saint Lucia, and Liberia, and the sub-national entities Leiden, Norfolk Island, and Puerto Rico. ","image_url":"https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRsw5mK1DrbsDyExksmgeYsIohmtKLkgbc4m2x1q0oxiO43XEv2","proper_name":"Thanksgiving","what_is_term":"Holiday","wikipedia_link":"https://en.wikipedia.org/wiki/Thanksgiving"},"22":{"description":"An angel is a supernatural being in various Circum-Mediterranean religions. Abrahamic religions often depict them as benevolent celestial intermediaries between God and humanity. Other roles include protectors and guides for humans, and servants of God. ","image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcUp-gOnAob1JBySBdiNlzOFWh5Lwp42GxxGmZgkj2NYBFXzA9","proper_name":"Angel","wikipedia_link":"https://en.wikipedia.org/wiki/Angel"},"45":{"description":"Intuition is the ability to acquire knowledge without recourse to conscious reasoning. Different fields use the word \"intuition\" in very different ways, including but not limited to: direct access to unconscious knowledge; unconscious cognition; inner sensing; inner insight to unconscious pattern-recognition; and the ability to understand something instinctively, without any need for conscious reasoning.\n","proper_name":"Intuition","wikipedia_link":"https://en.wikipedia.org/wiki/Intuition"},"65":{"description":"The Thing is a fictional superhero appearing in American comic books published by Marvel Comics. The character is a founding member of the Fantastic Four. ","proper_name":"Thing","what_is_term":"Fictional superhero","wikipedia_link":"https://en.wikipedia.org/wiki/Thing_(comics)"},"71":{"description":"Proofreading is the reading of a galley proof or an electronic copy of a publication to find and correct production errors of text or art. Proofreading is the final step in the editorial cycle before publication.","proper_name":"Proofreading","wikipedia_link":"https://en.wikipedia.org/wiki/Proofreading"},"90":{"description":"A fact is an occurrence in the real world. For example, \"This sentence contains words.\" is a linguistic fact, and \"The sun is a star.\" is an astronomical fact. ","proper_name":"Fact","wikipedia_link":"https://en.wikipedia.org/wiki/Fact"}}

    return jsonify(fake_dict)

if __name__ == "__main__":
    authenticator = IAMAuthenticator('TWS446L2CH4Zxnrh-nwh3T2g8stRlB08e4iyjAKyBHg0')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/816f28bc-9729-48ca-b11a-c736524e6ad6')
    app.run()
    # print(smart_data_fetcher.get_smart_data_for_keyword('elephant'))
