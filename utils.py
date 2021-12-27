# import librosa
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import librosa
import librosa.display
import os

def shift_time(t):
    mins, secs = divmod(t, 60)
    mins = round(mins)
    secs = round(secs)

    return '{:02d}:{:02d}'.format(mins, secs)

def draw(frame, audio):
    figure = Figure(figsize=(5,4), dpi=100)

    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    ax = figure.add_subplot(111)
    ax.set_title(os.path.basename(audio))
    
    # shit librosa, default sr 22500
    y, sr = librosa.load(audio, sr=16000)
    x = [i/sr for i in range(len(y))]
    ax.plot(x,y)
    canvas.draw()

if __name__ == "__main__":
    pass