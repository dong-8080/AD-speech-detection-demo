import requests
import os
import re


socket = "http://10.204.34.42:8080"

def get_audio_list():
    """
    发送请求获取已有的测试语音名称
    """
    url = socket+"/audio/list"
    res = requests.get(url)
    return res.text

def save_audio(data, file, root):
    """
    保存语音文件到root/file
    """
    if not os.path.exists(root):
        os.makedirs(root)
    filepath = os.path.join(root, file)
    with open(filepath, "wb") as f:
        f.write(data)

def request_audio(file):
    """
    从服务器中获取语音文件
    """
    
    url = socket + "/download/" + file
    res = requests.get(url)
    return res.content

def load_audio(file, root):
    """
    根据名称获取具体的测试语音
    root: local directory
    """
    # 语音文件不存在时，从服务器中获取并保存到本地
    filepath = os.path.join(root, file)

    if not os.path.exists(filepath):
        url = socket + "/download/"+file
        res = requests.get(url)
        data = res.content # binary
        save_audio(data, file, root)

    return os.path.join(root, file)

def test_connection():
    """
    毫无卵用，就是测试能不能连接服务器
    """
    url = socket + "/hello"
    res = requests.get(url)
    if 200==res.status_code:
        return "Connecting to the server successfully!"
    else:
        return "Failed to connect to server"

def fetch_result(filename):
    """
    发送文件给后端，获取分析结果以及某些特征。
    若服务器存在测试文件，则只上传文件名即可。
    要啥自行车，就这破数据哪有诊断数据-.-
    """
    # 正则判断一下是否是测试样例
    if re.match(r"\d{4}_(AD|HC|MCI).wav", filename):
        url = socket + "/test"
        params = {"filename": "0001_MCI.wav"}
        res = requests.get(url, params)
        return eval(res.text)['label'], eval(res.text)['feature']
    else:
        # upload first and test
        print("file not exist, upload not finish!")
        pass

if __name__ == "__main__":
    file = "0071_MCI.wav"
    root = "./"
    a =  load_audio(file, root)
    print(a)