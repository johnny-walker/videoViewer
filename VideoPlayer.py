import os
import tkinter as tk
from tkinter import filedialog
import cv2
import threading

# import own modules
from ProgramBase import PgmBase
from ThreadBase import ThreadClass

class VideoViewer(PgmBase):
    cvImg = None
    cvImgUpdate = None
    videofile = None
    isPlaying = False
    fps = 29.97

    def __init__(self, root, width=800, height=600):
        super().__init__(root, width, height)
        self.root.title('Video Player')

        # initi thread for video playback
        self.thread = None
        self.threadEventPlayback = threading.Event()

    # overrite button handlers
    def onOpen(self):
        self.threadEventPlayback.set() 
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
            self.thread = ThreadClass(1, "Video Playback Thread", self, self.loadVideo)
            self.threadEventPlayback.clear() 
            self.thread.start()
            self.isPlaying = True
            self.btnPlay['text'] = 'stop'
    
    def loadVideo(self):
        videoObject = cv2.VideoCapture(self.videofile)
        if videoObject.isOpened():
            index=0
            while not self.threadEventPlayback.wait(timeout = 1/self.fps) :
                index += 1
                print("frame_{0:04d}".format(index))
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
