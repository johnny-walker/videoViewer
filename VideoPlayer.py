import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading

# import own modules
from ProgramBase import PgmBase
from ThreadBase import ThreadClass

program = None
def threadFunc():
    global program
    program.loadVideo()

class VideoViewer(PgmBase):
    cvImg = None
    cvImgUpdate = None
    videofile = None
    isPlaying = False
    fps = 1/30

    def __init__(self, root, width=800, height=600):
        super().__init__(root, width, height)
        self.root.title('Video Player')

        # initi thread for video playback
        self.thread = None
        self.threadEventPlayback = threading.Event()

    # overrite button handlers
    def onOpen(self):
        self.videofile =  filedialog.askopenfilename(initialdir="./", title="Select Video File")
        self.openVideo(self.videofile)

    def onReset(self):
        self.threadEventPlayback.clear()
        self.showMessage("reset effects")
        self.isPlaying = False
        self.btnPlay['text'] = 'play'

    def onPlay(self):
        self.isPlaying = not self.isPlaying
        message = 'start playing video' if self.isPlaying else 'stop video playback'
        self.showMessage(message)
        
        if self.isPlaying and self.videofile:
            self.openVideo(self.videofile)
            self.btnPlay['text'] = 'stop'
        else:
            self.threadEventPlayback.set()
            self.btnPlay['text'] = 'play'


    def onApply(self):
        self.showMessage("apply effect")

    # VideoViewer funcs
    def openVideo(self, path):
        self.videofile = path
        if self.videofile:
            self.showMessage("playback video file: {0:s}".format(self.videofile))
            self.startVideoThread()

    def startVideoThread(self):
        if self.videofile:
            self.thread = ThreadClass(1, "Video Playback Thread", self, threadFunc)
            self.threadEventPlayback.clear() 
            self.thread.start()
            self.isPlaying = True
            self.btnPlay['text'] = 'stop'
    
    def loadVideo(self):
        videoObject = cv2.VideoCapture(self.videofile)
        i=0
        if videoObject.isOpened():
            while not self.threadEventPlayback.wait(timeout=self.fps) :
                i += 1
                print("frame"+str(i))
                ret, frame = videoObject.read()
                if ret:
                    self.updateImage(frame)
                else:
                    break
            videoObject.release()
            self.threadEventPlayback.clear()
        self.isPlaying = False
        self.btnPlay['text'] = 'play'
        print("playback completed")
        self.showMessage("playback reached the end of the file")

if __name__ == '__main__':
    program = VideoViewer(tk.Tk())

    cwd = os.getcwd()
    girl = os.path.join(cwd, "data/girls.mp4")
    program.openVideo(girl)

    program.run()
