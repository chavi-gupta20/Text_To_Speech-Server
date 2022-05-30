from flask import Flask,render_template, jsonify,request,send_from_directory
from gtts import gTTS
from gtts.tokenizer import pre_processors
from IPython.display import Audio
from playsound import playsound
from flask_cors import CORS,cross_origin
import gtts.tokenizer.symbols
import os
import re
import inflect

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
DOWNLOAD_DIRECTORY = "/home/fa059053/Desktop/tts-server"


def convert_word(match_obj):
    if match_obj.group() is not None:
        return inflect.engine().number_to_words(match_obj.group())

def substitutor(test_text):
    
    
    sentence = test_text
    final_sentence=re.sub(r"2[0-9][0-9][0-9]",convert_word, sentence)
    replaced = re.sub('Dec-', 'December', final_sentence)
    return replaced


@app.route('/get-files/<path:path>',methods = ['GET'])
def get_files(path):

    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route("/speak",methods=['POST'])
def say():
    if os.path.exists("/home/fa059053/Desktop/tts-server/1.wav"):
       os.remove("/home/fa059053/Desktop/tts-server/1.wav")
       print("File deleted")
    speak_text=request.json['text']
    final_text=substitutor(speak_text)
    ##gtts.tokenizer.symbols.SUB_PAIRS.append([('Dec-', 'December')])
    ##final_text=pre_processors.word_sub(test_text)
    print(final_text)
    tts = gTTS(final_text,lang='en',tld='co.in')
    tts.save('1.wav')
    sound_file = '1.wav'
    Audio(sound_file,autoplay=True)
    # path="http://127.0.0.1:8887/{file_name}".format(file_name=sound_file) 
    # to use the above endpoint, an extension needs to be downloaded - web server for chrome                   
    path="http://localhost:5000/get-files/1.wav"    #get files locally using get-files endpoint
    print("path is"+path)
    return jsonify({"path":path})



if __name__ =="__main__":
    app.run(debug = True)

