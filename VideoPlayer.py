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

class VideoViewer(PgmBase):
    cvImg = None
    cvImgUpdate = None
    videofile = None
    isPlaying = False

    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Video Player')

        # initi thread for video playback
        self.thread = None
        self.threadEventPlayback = threading.Event()

    def openVideo(self, path):
        self.videofile = path
        if self.videofile:
            self.showMessage("open file {0:s}".format(self.videofile))
            self.startVideoThread()

    def startVideoThread(self):
        if self.videofile:
            self.thread = ThreadClass(1, "Video Playback Thread", self, self.loadVideo)
            self.threadEventPlayback.clear()   # reset the thread event
            self.thread.start()
            self.isPlaying = True
    
    def loadVideo(self):
        videoObject = cv2.VideoCapture(self.videofile)

        while not self.threadEventPlayback.wait(timeout=0.033) and videoObject.isOpened():
            ret, frame = videoObject.read()
            if ret:
                self.updateImage(frame)
        videoObject.release()
        self.threadEventPlayback.clear()

    # button handlers
    def onOpen(self):
        self.videofile =  filedialog.askopenfilename(initialdir="./", title="Select Video File")
        self.openVideo(self.videofile)

    def onReset(self):
        self.threadEventPlayback.set()
        self.showMessage("stop playback")
        self.isPlaying = False

    def onPlay(self):
        # todo
        self.isPlaying = not self.isPlaying
        message = 'start playing video' if self.isPlaying else 'pause video'
        self.showMessage(message)
    
    def onApply(self):
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        self.cvImgUpdate = cv2.filter2D(self.cvImgUpdate, -1, kernel)
        self.updateImage(self.cvImgUpdate)
        self.showMessage("apply flow detection")

if __name__ == '__main__':
    program = VideoViewer(tk.Tk(), width=800, height=600)

    cwd = os.getcwd()
    girl = os.path.join(cwd, "data/girls.mp4")
    program.openVideo(girl)

    program.run()
