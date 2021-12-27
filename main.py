from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.scrolledtext as scrolledtext
from ttkthemes import themed_tk as tk
import tkinter.font as tkFont

import time
import threading
from pygame import mixer
import shutil

import request
import utils

import requests
import os


# 保存语音文件的位置
root_dir = "./download"

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")


# 底部状态栏，用来显示状态信息，还挺有意思的
statusbar = ttk.Label(root, text="welcome", relief=SUNKEN,\
    anchor=W, font="Times 10 italic")
statusbar.pack(side=BOTTOM, fill=X)

# 菜单栏
menubar = Menu(root)
root.config(menu=menubar)

root.title("AD Detection Demo")
# root.iconbitmap(r'images/melody.ico')

def deleteDownload():
    if os.path.exists("./download"):
        shutil.rmtree("./download")
    tkinter.messagebox.showinfo('Delete', "The cache file was successfully deleted.")

def exit():
    if os.path.exists("./download"):
        shutil.rmtree("./download")
    root.destroy()
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Delete", command=deleteDownload)
subMenu.add_command(label="Exit", command=exit)

# 作者相关信息
def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music\
    player build using Python Tkinter by @attreyabhatt')

def test_connection():
    msg = request.test_connection()
    tkinter.messagebox.showinfo('Help', msg)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)
subMenu.add_command(label="Test", command=test_connection)

# 顶部左侧布局
topparentframe = Frame(root)
topparentframe.pack(side=TOP)


leftframe = Frame(topparentframe)
leftframe.pack(side=LEFT, padx=30, pady=30)

ft = tkFont.Font(family="Arial", size=12, weight=tkFont.BOLD)
listLabel = Label(leftframe, text="Test audio list", font=ft)
listLabel.pack()
def get_audios():
    audio_list = request.get_audio_list()
    for i in eval(audio_list):
        playlistbox.insert("end", i)

playlistbox = Listbox(leftframe)
playlistbox.pack()

def select_audio():
    try:
        filename = playlistbox.get(playlistbox.curselection())

        # 改变src的信息
        m = f"Select {filename}, Ready to Play.\n"
        informations.insert(END, m)

        # 预下载语音
        audio = request.load_audio(filename, root_dir)

        audio_length = mixer.Sound(os.path.join(root_dir, filename)).get_length()
        timeformat = utils.shift_time(audio_length)
        lengthlabel['text'] = "Total Length" + ' : ' + timeformat

        utils.draw(mfccLabel, audio)

    except tkinter._tkinter.TclError:
        # 肯定是没选择测试语音，弹框提示一下
        tkinter.messagebox.showinfo('Warning', 'please select audio from list')
    
def cancel_audio():
    informations.delete(0.0, END)
    currenttimelabel['text'] = "Current Time" + ' - ' + "--:--"

addBtn = ttk.Button(leftframe, text="Select", command=select_audio)
addBtn.pack(side=LEFT)

delBtn = ttk.Button(leftframe, text="Cancel", command=cancel_audio)
delBtn.pack(side=LEFT)


# 顶部右侧布局
rightframe = Frame(topparentframe)
rightframe.pack(pady=50)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

# 右侧布局中间按钮部分
middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

mixer.init()
isPause = False

def show_details(audio):
    # 调用进程，展示正在播放语音的时间
    audio_length = mixer.Sound(audio).get_length()
    t1 = threading.Thread(target=start_count, args=(audio_length,))
    t1.start()

def start_count(t):
    global isPause
    current_time = 0
    while current_time<=t and mixer.music.get_busy():
        if isPause:
            continue
        else:
            time.sleep(1)
            current_time += 1
            timeformat = utils.shift_time(current_time)
            currenttimelabel['text'] = "Current Time" + ' : ' + timeformat

def play_audio():
    global isPause
    if isPause:
        mixer.music.unpause()
        isPause = False
    else:
        stop_audio()
        time.sleep(0.5)
        
        filename = filename = playlistbox.get(playlistbox.curselection())
        audio = request.load_audio(filename, root_dir)

        mixer.music.load(audio)
        mixer.music.play()
        show_details(audio)
        

def pause_audio():
    global isPause
    isPause = True
    mixer.music.pause()

def stop_audio():
    mixer.music.stop()
    currenttimelabel["text"] = "Current Time : --:--"

playPhoto = PhotoImage(file='images/play.png').subsample(3, 3)
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_audio)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png').subsample(3, 3)
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_audio)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png').subsample(3, 3)
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_audio)
pauseBtn.grid(row=0, column=2, padx=10)

def parse():
    ifo = "start parsing... ...\n"
    informations.insert(END, ifo)

    filename = playlistbox.get(playlistbox.curselection())
    predict, features = request.fetch_result(filename)

    m = f"\nThe result of predicting {filename} is {predict}\n\n"
    informations.insert(END, m)

    m = "Detailed feature information is as follows:\n"
    informations.insert(END, m)

    for k,v in features.items():
        informations.insert(END, f"{k} : {v}\n")

parseBtn = ttk.Button(rightframe, text="Parse", command=parse)
parseBtn.pack()

# 信息输出框
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM, fill=X)

notebook = ttk.Notebook(bottomFrame, width=550 ,height=400)


notebook.pack(pady=5)
informations = scrolledtext.ScrolledText(bottomFrame, height=20)
mfccLabel = ttk.Label(bottomFrame)
# mfccLabel["image"] = mfccphoto
informations2 = scrolledtext.ScrolledText(bottomFrame, height=20)

notebook.add(informations, text="Log")
notebook.add(mfccLabel, text="Waveform")
# informations.pack(pady=5)

# 等界面全部加载完成后，获取语音列表，若出错则弹窗表示后端未运行
try:
    get_audios()
except Exception as e:
    time.sleep(1)
    tkinter.messagebox.showerror('Error', 'Failed to connect to the server.\nPlease Contact your system administrator!')
    statusbar['text'] = "Error. Please contact the system administrator!"

# 主循环
root.mainloop()