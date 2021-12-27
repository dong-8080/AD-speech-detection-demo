# AD-speech-detection-demo

AD语音识别Demo版，应老师要求写个界面以及简单的流程，用作去医院搞数据。

实现功能为：前端展示测试数据列表，选定语音数据可以播放，并绘制波形图。解析时从语音中提取IS10以及韵律特征，支持向量机进行分类，并将所有特征和结果返回前端展示。

目前仅支持使用已有的数据。数据由NCMMSC提供，已经划分好了训练集与测试集，数据集质量不高。直接训练集，长时测试集作为测试，并于前端展示。

**实现：**

Demo分为前后端，前端用Tkinter实现，参考自：

后端用bottle，转接代码写的很乱，头疼写的，勿做评价。

模型用scikit-learn实现，经过试验发现数据标准化后经PCA降维，用AVONA选择4个特征，使用rbf核的SVM分类效果好，在NCMMSC测试集上的指标如下。

| Accuracy | Precision | Recall | F1     |
| -------- | --------- | ------ | ------ |
| 0.8067   | 0.8481    | 0.8067 | 0.8095 |

![confusion matrix](https://github.com/dong-8080/AD-speech-detection-demo/blob/main/images/confusion_matrix.png)

若非菜孰愿弟，等拿到医院数据后训练更强的分类模型。

**界面：**


![gui1](https://github.com/dong-8080/AD-speech-detection-demo/blob/main/images/readme1.png)

![gui2](https://github.com/dong-8080/AD-speech-detection-demo/blob/main/images/readme2.png)
