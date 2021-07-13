import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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
        geometry = '{0:d}x{1:d}+{2:d}+{3:d}'.format(root.width+5, root.height+5, x, y) 
        root.geometry(geometry)    # ex. root.geometry('600x400+250+150')
        root.title("window")

        # bind events
        root.bind_all('<Key>', self.onKey)
        self.root.title('Video Viewer')
        self.loadLayout()
        self.bindBtnEvents()

    def bindBtnEvents(self):
        self.btnOpen['command'] = lambda : self.onOpen()
        self.btnReset['command'] = lambda : self.onReset()   
        self.btnPlay['command'] = lambda : self.onPlay()
        self.btnApply['command'] = lambda : self.onApply()


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
        self.imgHeight = self.root.height - btnHeight - msgHeight

        divImg = tk.Frame(self.root,  width=self.imgWidth , height=self.imgHeight , bg='blue')
        divBtnArea = tk.Frame(self.root,  width=self.imgWidth , height=btnHeight , bg='white')
        divMsg = tk.Frame(self.root,  width=self.imgWidth , height=msgHeight , bg='black')

        self.root.update()

        divImg.grid(row=0, column=0, padx=padding, pady=padding, sticky=align_mode)
        divBtnArea.grid(row=1, column=0, padx=padding, pady=padding, sticky=align_mode)
        divMsg.grid(row=2, column=0, padx=padding, pady=padding, sticky=align_mode)

        self.defineLayout(self.root)
        self.defineLayout(divImg)
        self.defineLayout(divBtnArea)
        self.defineLayout(divMsg)

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
        self.showMessage("reset")

    def onPlay(self):
        self.showMessage("play")

    def onApply(self):
        self.showMessage("apply")

    def loadImage(self, path):
        im = Image.open(path)
        im.thumbnail((self.imgWidth, self.imgHeight))
        tkimage = ImageTk.PhotoImage(im)

        if self.lblImg:
            self.lblImg.destroy()

        # create label
        self.lblImg = tk.Label(self.divImg, image=tkimage)
        self.lblImg.image = tkimage    
        self.lblImg.grid(row=0, column=0)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight

        align_mode = 'nswe'
        self.lblImg.grid(row=0, column=0, sticky=align_mode)

        self.showMessage("file {0:s} loaded".format(path))

    # img : cv image
    def updateImage(self, img):
        im = Image.fromarray(img)
        im.thumbnail((self.imgWidth, self.imgHeight))
        tkimage = ImageTk.PhotoImage(im)

        if self.lblImg:
            self.lblImg.destroy()

        # create label
        self.lblImg = tk.Label(self.divImg, image=tkimage)
        self.lblImg.image = tkimage    
        self.lblImg.grid(row=0, column=0)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight

        align_mode = 'nswe'
        self.lblImg.grid(row=0, column=0, sticky=align_mode)

if __name__ == '__main__':
    program = PgmBase(tk.Tk(), width=800, height=600)
    program.loadLayout()
    program.bindBtnEvents()

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)
    program.run()
