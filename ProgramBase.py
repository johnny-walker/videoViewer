import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class PgmBase(tk.Frame):
    divImg = None
    lblImg = None
    lblMsg = None

    btnOpen = None
    btnReset = None
    btnPlay = None
    btnApply = None

    def __init__(self, root, width=640, height=480):
        super().__init__(root)
        self.root = root
        self.frame = self

        # configure window
        x = 450
        y = 150
        root.width = width
        root.height = height
        geometry = '{0:d}x{1:d}+{2:d}+{3:d}'.format(root.width, root.height, x, y) 
        root.geometry(geometry)    # ex. root.geometry('600x400+250+150')
        self.root.title('Image Viewer')

        # bind events
        root.bind_all('<Key>', self.onKey)
        self.loadLayout()
        self.bindBtnEvents()

    def bindBtnEvents(self):
        self.btnOpen['command'] = lambda : self.onOpen()
        self.btnReset['command'] = lambda : self.onReset()   
        self.btnPlay['command'] = lambda : self.onPlay()
        self.btnApply['command'] = lambda : self.onApply()
        self.root.bind("<Configure>", self.onResize)

    def onResize(self, event):
        if event.widget == self.lblImg:
            self.imgWidth = event.width
            self.imgHeight = event.height

    def run(self):
        self.root.mainloop()

    def onKey(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == 'Right':
                print("key Right") 
            elif event.keysym == 'Left':
                 print("key Left") 
            elif event.keysym == 'Space':
                 print("key Space") 
            elif event.keysym == 'Escape':
                print("key Escape") 
                self.root.destroy()

    def defineLayout(self, widget, cols=1, rows=1):
        for c in range(cols):    
            widget.columnconfigure(c, weight=1)
        for r in range(rows):
            widget.rowconfigure(r, weight=1)
    
    def loadLayout(self):
        align_mode = 'nswe'
        padding= 2
        btnHeight = 40
        msgHeight = 40

        self.imgWidth = self.root.width
        self.imgHeight = self.root.height - btnHeight 
        divImg = tk.Frame(self.root,  width=self.imgWidth , height=self.imgHeight , bg='white')
        divBtnArea = tk.Frame(self.root,  width=self.imgWidth , height=btnHeight , bg='white')
        divMsg = tk.Frame(self.root,  width=self.imgWidth , height=msgHeight , bg='black')

        divImg.grid(row=0, column=0, padx=padding, pady=padding, sticky=align_mode)
        divBtnArea.grid(row=1, column=0, padx=padding, pady=padding, sticky=align_mode)
        divMsg.grid(row=2, column=0, padx=padding, pady=padding, sticky=align_mode)

        self.defineLayout(self.root)
        self.defineLayout(divImg)
        self.defineLayout(divMsg)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # label as container of image
        self.divImg = divImg

        self.btnOpen = tk.Button(divBtnArea, text='open')
        self.btnOpen.pack(side='left')

        self.btnReset = tk.Button(divBtnArea, text='reset')
        self.btnReset.pack(side='left')

        self.btnPlay = tk.Button(divBtnArea, text='play')
        self.btnPlay.pack(side='left')

        self.btnApply = tk.Button(divBtnArea,text='apply')
        self.btnApply.pack(side='left')


        # label as message
        self.lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showMessage(self, msg):
        self.lblMsg['text'] = msg
        
    def onOpen(self):
        self.videofile =  filedialog.askopenfilename(initialdir="./", title="Select a file")
        if self.videofile:
            self.showMessage("open file {0:s}".format(self.videofile))
            self.loadImage(self.videofile)

    def onReset(self):
        # override to implement this
        self.showMessage("reset")

    def onPlay(self):
        # override to implement this
        self.showMessage("play")

    def onApply(self):
        # override to implement this
        self.showMessage("apply")

    def loadImage(self, path):
        im = cv2.imread(path)
        self.updateImage(im)
        self.showMessage("file {0:s} loaded".format(path))

    def dimResize(self, im):
        tar_ratio = self.imgHeight / self.imgWidth
        im_ratio = im.shape[0] / im.shape[1]
        if tar_ratio > im_ratio:
            # scale by width
            width = self.imgWidth
            height = round(width * im_ratio)
        else:
            # scale by height
            height = self.imgHeight
            width = round(height / im_ratio)
        return (width, height)

    # img : cv image
    def updateImage(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        dim = self.dimResize(img)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        im = Image.fromarray(img)
        tkimage = ImageTk.PhotoImage(im)

        if self.lblImg:
            self.lblImg.configure(image=tkimage)
            self.lblImg.image = tkimage
        else:
            # create label
            self.lblImg = tk.Label(self.divImg, image=tkimage)
            self.lblImg.image = tkimage    
            self.lblImg['width'] = dim[0]
            self.lblImg['height'] = dim[1]
            self.lblImg.grid(row=0, column=0, sticky='nswe')

if __name__ == '__main__':
    program = PgmBase(tk.Tk(), width=800, height=600)
    program.loadLayout()
    program.bindBtnEvents()

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)
    program.run()
