# -*- coding: utf-8 -*-

# Copyright 2021  Authors: Kevin.MH.Yang
# Requirements:
#   - python > 3.4
#   - flask (pip install flask)
#   #- jiwer (pip install jiwer)
#   - srt (pip install srt)

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
#import jiwer
import srt
import uuid
import time
import logging
from io import StringIO

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

#logging.basicConfig(filename='error.log', level=logging.DEBUG)

#transformation = jiwer.Compose([
#    jiwer.ToLowerCase(),
#    jiwer.RemoveWhiteSpace(replace_by_space=True),
#    jiwer.RemoveMultipleSpaces(),
#    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
#]) 

datefmt = "%Y-%m-%d %H:%M:%S"
log_stream = StringIO()    
logging.basicConfig(format="%(asctime)s [%(levelname)-1s] %(message)s", stream=log_stream, level=logging.DEBUG, datefmt=datefmt)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)-1s]: %(message)s", datefmt)
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-1s]: %(message)s", datefmt))
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
file_handler = logging.FileHandler("error.log", "w")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler) 



@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/test_post", methods=['POST', 'GET'])
def test_post():
    print("///////////////")
    print(request.json)
    print("///////////////")
    return jsonify(status="Hello")

@app.route("/block_merge_wav", methods=['POST', 'GET'])
def block_merge_wav():
    print("///////////////")
    logger.debug(request.json)
    current = time.strftime("%Y%m%d-%H%M", time.localtime())
    folder = "{TIME}-{UID}".format(TIME=current, UID=str(uuid.uuid4()))
    logger.debug(folder)
    print("///////////////")
    return jsonify(url="http://10.137.0.6/block-mergewav/uploads/" + folder)

@app.route("/srt_norm", methods=['POST'])
def srt_norm():
    print("--"*50)
    srtfile = request.files["srt"]
    print("  - {}".format(str(srtfile)))

    content = srtfile.read().decode('utf-8').replace('\ufeff', '')
    list_srt = list(srt.parse(content))
    print("  - length", len(list_srt))

    normed_srt = srt.compose(list_srt)
    return jsonify(srt_norm=normed_srt)

# '''
# @app.route("/calculate", methods=['POST','PUT'])
# def calc():
#     ref = request.files['ref']
#     hyp = request.files['hyp']
#     is_kaldi = request.files['kaldi']
#     
#     ref_filename = secure_filename(ref.filename)
#     hyp_filename = secure_filename(hyp.filename)
#     
#     ground_truth = str(ref.read())
#     hypothesis = str(hyp.read())
# 
#     if is_kaldi:
#         ground_truth = ground_truth.split("")
# 
# 
#     print(type(ground_truth))
#     print(ref_filename, len(ground_truth))
#     print(hyp_filename, len(hypothesis))   
#     print(ground_truth.split()[0], ground_truth.split()[1]) 
# 
#     error = jiwer.cer(ground_truth, hypothesis, 
#                       truth_transform=transformation, 
#                       hypothesis_transform=transformation
#                       )
#     
#     return "{}\n".format(round(error, 2))
# '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7733, debug=False) 
    #app.run(host='0.0.0.0', port=7733, debug=True) 

