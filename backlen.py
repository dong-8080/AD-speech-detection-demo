from bottle import template, Bottle, request, static_file

import numpy as np
import pandas as pd
import os

import joblib

from extractor import FeatureExtractor

root = Bottle()
base_path = "/home/wd/data/NCMMSC/long_testdata/"

def get_test_audio():
    wav_list = []
    
    for i, f in enumerate(os.listdir(base_path)):
        wav_list.append(f)
    wav_list.sort()
    return wav_list

@root.route("/hello", method="GET")
def index():
    return 'hello get!'

@root.route("/hello", method="POST")
def index():
    email = request.forms.get("email")
    address = request.forms.get("address")
    return email+" "+address

@root.route("/audio/list", method="GET")
def get_testset():
    """
    获取测试语音列表
    """
    wavlist = get_test_audio()
    return str(wavlist)

@root.route("/download/<filepath>")
def download(filepath):
    """
    根据文件名，提供语音文件
    """
    return static_file(filepath, root=base_path)

def get_prosody(audio):
    """
    直接查表得到韵律特征，调用那个包太麻烦了，需要有新数据再说
    """
    prosody = pd.read_csv("/home/wd/data/NCMMSC/prosody/prosody_test.csv")
    prosody = prosody[prosody["AudioFile"]==audio].drop("AudioFile", axis=1)
    return dict(zip(prosody.columns.values, prosody.values[0])), prosody.values[0]

@root.route("/test")
def test():
    filename = request.query.filename
    
#    just local file
    audio_path = os.path.join(base_path, filename)
    clf = joblib.load("./svm.model")
    # 提取IS10特征
    fe = FeatureExtractor().extract(audio_path)
    feature = np.array(list(fe.values())).reshape(1,-1)
    
    # 提取韵律特征
    prosody_dict, prosody_list = get_prosody(filename)
    
    fe = {**fe,  **prosody_dict}
    feature = feature.tolist()[0]
    feature.extend(prosody_list)

    # 不能回传数字，转成字符串传输
    pred = clf.predict([feature])
    # TODO: return it
    return {"label": pred[0], "feature": fe}
root.run(host="10.204.34.42", port=8080)