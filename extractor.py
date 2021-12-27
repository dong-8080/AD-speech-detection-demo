import pandas as pd
import numpy as np
import os

class FeatureExtractor():
    """
    封装openSMILE提取语音特征
    """
    def __init__(self,
                 tool_path = "/home/wd/tools/opensmile/bin/SMILExtract",
                 config_path = "/home/wd/tools/opensmile/config/is09-13/IS10_paraling.conf ",
                 output_path = "/home/wd/data/SystemDemo/tmp/"):
        self.tool_path = tool_path
        self.config_path = config_path
        self.output_path = output_path
        
    # 提取一条语音特征
    def extract(self, audio_file):
        """
        从音频文件中提取特征
        """
        file_output = os.path.join(self.output_path, os.path.basename(audio_file).replace(".wav", ".txt"))

        cmd = f"{self.tool_path} -C {self.config_path} -I {audio_file} -O {file_output} -noconsoleoutput 1"
        os.system(cmd)

        features = self.feature_txt2npy(file_output)

        # remove the temp file
        if os.path.exists(file_output):
            os.remove(file_output)

        return features

    # 读取一个eGeMAPS.txt文件，转化为特征名与特征的格式
    def feature_txt2npy(self, txt_file):
        """
        读取openSMILE提取的特征文件，构造成字典返回
        """
        data = pd.read_table(txt_file, header=None)

        # feature names and values  this is for eGeMAPS
#         keys = [d.split(" ")[1] for d in data[0][2:90].tolist()]
#         values = [float(i) for i in data.iloc[-1].values[0][10:-2].split(",")]

        keys = [d.split(" ")[1] for d in data[0][2:data.shape[0]-3].tolist()]
        values = [float(i) for i in data.iloc[-1].values[0][10:-2].split(",")]

        features = dict(zip(keys, values))
        return features
    
if __name__ == "__main__":
    # unit test
    audio_path = "/home/wd/data/NCMMSC/long_testdata/0002_AD.wav"
    fe = FeatureExtractor().extract(audio_path)
    feature = np.array(list(fe.values())).reshape(1,-1)
    print(feature)