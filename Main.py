from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askopenfilename
import numpy as np 
from CannyEdgeDetector import *
import skimage
import matplotlib.image as mpimg
import os
import scipy.misc as sm
import cv2
import matplotlib.pyplot as plt 


main = tkinter.Tk()
main.title("Smart Traffic Control System Using Canny Edge Detection Algorithm")
main.geometry("1040x940")

global filename
global refrence_pixels
global sample_pixels

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def uploadTrafficImage():
    global filename
    filename = filedialog.askopenfilename(initialdir="images")
    pathlabel.config(text=filename)

def visualize(imgs, format=None, gray=False):
    j = 0
    plt.figure(figsize=(20, 40))
    for i, img in enumerate(imgs):
        if img.shape[0] == 3:
            img = img.transpose(1,2,0)
        plt_idx = i+1
        plt.subplot(2, 2, plt_idx)
        if j == 0:
            plt.title('Sample Image')
            plt.imshow(img, format)
            j = j + 1
        elif j > 0:
            plt.title('Reference Image')
            plt.imshow(img, format)
            
    plt.show()
    
def applyCanny():
    imgs = []
    img = mpimg.imread(filename)
    img = rgb2gray(img)
    imgs.append(img)
    edge = CannyEdgeDetector(imgs, sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.20, weak_pixel=100)
    imgs = edge.detect()
    for i, img in enumerate(imgs):
        if img.shape[0] == 3:
            img = img.transpose(1,2,0)
    cv2.imwrite("gray/test.png",img)
    temp = []
    img1 = mpimg.imread('gray/test.png')
    img2 = mpimg.imread('gray/refrence.png')
    temp.append(img1)
    temp.append(img2)
    visualize(temp)

def pixelcount():
    global refrence_pixels
    global sample_pixels
    img = cv2.imread('gray/test.png', cv2.IMREAD_GRAYSCALE)
    sample_pixels = np.sum(img == 255)
    
    img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
    refrence_pixels = np.sum(img == 255)
    messagebox.showinfo("Pixel Counts", "Total Sample White pixels Count : "+str(sample_pixels)+"\nTotal Reference White Pixels Count : "+str(refrence_pixels))


def timeAllocation():
    avg = (sample_pixels/refrence_pixels) *100
    if avg >= 90:
        messagebox.showinfo("Green Signal Allocation Time","Traffic is very high allocation green signal time : 120 secs")
    if avg > 85 and avg < 90:
        messagebox.showinfo("Green Signal Allocation Time","Traffic is high allocation green signal time : 60 secs")
    if avg > 75 and avg <= 85:
        messagebox.showinfo("Green Signal Allocation Time","Traffic is moderate green signal time : 40 secs")
    if avg > 50 and avg <= 75:
        messagebox.showinfo("Green Signal Allocation Time","Traffic is low allocation green signal time : 30 secs")
    if avg <= 50:
        messagebox.showinfo("Green Signal Allocation Time","Traffic is very low allocation green signal time : 20 secs")        
        

def exit():
    main.destroy()
    

    
font = ('Times',18, 'bold')
title = Label(main, text='.                                         Density Based Smart Traffic Control System Using Canny Edge Detection Algorithm      ',anchor=W, justify=CENTER)
title.config(bg='teal', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)


font1 = ('times', 14, 'bold')
upload = Button(main, text="Upload Traffic Image",command=uploadTrafficImage)
upload.place(x=260,y=180)
upload.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='silver', fg='black')  
pathlabel.config(font=font1)           
pathlabel.place(x=500,y=184)

process = Button(main, text="Image Preprocessing Using Canny Edge Detection", command=applyCanny)
process.place(x=260,y=255)
process.config(font=font1)

count = Button(main, text="White Pixel Count",command=pixelcount)
count.place(x=260,y=325)
count.config(font=font1)

count = Button(main, text="Calculate Green Signal Time Allocation",bg='green',fg='white', command=timeAllocation)
count.place(x=260,y=395)
count.config(font=font1)

exitButton = Button(main, text="Exit",bg='red',command=exit)
exitButton.place(x=1050,y=460)
exitButton.config(font=font1)


main.config(bg='silver')
main.mainloop()
