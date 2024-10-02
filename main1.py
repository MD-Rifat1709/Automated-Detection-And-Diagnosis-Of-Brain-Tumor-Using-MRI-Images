import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sys
sys.path.insert(0, './System/Project_8th/System')
from segmentation import segmentation
from classification_model import classification_model
from size import size
from plotx import result

my_w = tk.Tk()
my_w.geometry("1400x1300")  # Size of the window 
my_w.title('Preliminary Report')
my_font1=('times', 18, 'bold')
my_font2 = ('times', 14, 'bold')

def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    return inp
def upload_file():
    global img
    f_types = [('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    return filename
def print1():
    x = printInput()
    y = upload_file()
    lbl.config(text = "PRELIMINARY REPORT", font=my_font1)
    tumor_type, ICD_code = classification_model(y)
    if tumor_type=='No Tumor':
        l3 = tk.Label(my_w,text="Tumor Type: "+tumor_type,font=my_font2)  
        l3.grid(row=387, column=350)
        l4 = tk.Label(my_w,text="ICD Code: "+ICD_code,font=my_font2)  
        l4.grid(row=389, column=350)
        l5 = tk.Label(my_w,text="Tumor Radiomic Characteristics",font=my_font2)  
        l5.grid(row=399, column=350)
        l6 = tk.Label(my_w,text="Tumor Size: NA",font=my_font2)  
        l6.grid(row=401, column=350)
        l7 = tk.Label(my_w,text="Tumor Area: NA",font=my_font2)  
        l7.grid(row=403, column=350)
        img = Image.open(y)
        img_resized=img.resize((171,171)) # new width & height
        img=ImageTk.PhotoImage(img_resized)
        e1 =tk.Label(my_w)
        e1.grid(row=375,column=350)
        e1.image = img
        e1['image']=img
    else:
        l8 = tk.Label(my_w,text="Tumor Type: "+tumor_type,font=my_font2)  
        l8.grid(row=387, column=350)
        l9 = tk.Label(my_w,text="ICD Code: "+ICD_code,font=my_font2)  
        l9.grid(row=389, column=350)
        image1, output1, output2, basename = segmentation(y)
        plot1 = result(image1, output1, 'output')
        A, B, plot2, plot3 = size(output2, x)
        l10 = tk.Label(my_w,text="Tumor Radiomic Characteristics",font=my_font2)  
        l10.grid(row=399, column=350)
        if x=='1':
            number_of_white_pix = np.sum(plot3 == 255)
            l11 = tk.Label(my_w,text="Lateral Diameter: "+"{:.4f}mm".format(A),font=my_font2)  
            l11.grid(row=401, column=350)
            l12 = tk.Label(my_w,text="Anterio - Posterior Diameter: "+"{:.4f}mm".format(B),font=my_font2)  
            l12.grid(row=403, column=350)
            l13 = tk.Label(my_w,text="Tumor Area: "+"{:.4f}mm".format(number_of_white_pix*0.2401),font=my_font2)  
            l13.grid(row=405, column=350)
        elif x=='2':
            number_of_white_pix = np.sum(plot3 == 255)
            l11 = tk.Label(my_w,text="Anterio - Posterior Diameter: "+"{:.4f}mm".format(A),font=my_font2)  
            l11.grid(row=401, column=350)
            l12 = tk.Label(my_w,text="Craniocaudal Diameter: "+"{:.4f}mm".format(B),font=my_font2)  
            l12.grid(row=403, column=350)
            l13 = tk.Label(my_w,text="Tumor Area: "+"{:.4f}mm".format(number_of_white_pix*0.2401),font=my_font2)  
            l13.grid(row=405, column=350)
        elif x=='3':
            number_of_white_pix = np.sum(plot3 == 255)
            l11 = tk.Label(my_w,text="Lateral Diameter: "+"{:.4f}mm".format(A),font=my_font2)  
            l11.grid(row=401, column=350)
            l12 = tk.Label(my_w,text="Craniocaudal Diameter: "+"{:.4f}mm".format(B),font=my_font2)  
            l12.grid(row=403, column=350)
            l13 = tk.Label(my_w,text="Tumor Area: "+"{:.4f}mm".format(number_of_white_pix*0.2401),font=my_font2)  
            l13.grid(row=405, column=350)
        img=Image.fromarray(plot1)
        img_resized=img.resize((171,171)) # new width & height
        img=ImageTk.PhotoImage(img_resized)
        e1 =tk.Label(my_w)
        e1.grid(row=375,column=350)
        e1.image = img
        e1['image']=img
# TextBox Creation
l2 = tk.Label(my_w,text='Press 1 for Transverse, 2 for Sagittal and 3 for Coronal: ', font=my_font1)  
l2.grid(row=350,column=347)
inputtxt = tk.Text(my_w,
                   height = 1,
                   width = 5)
  
inputtxt.grid(row = 350, column = 350)
lbl = tk.Label(my_w, text = "")
lbl.grid(row = 372, column = 350)
l1 = tk.Label(my_w,text='Click the Button to Upload The Image and Get Results: ',font=my_font1)  
l1.grid(row=359, column=347)

printButton1 = tk.Button(my_w,
                        text = "Output", 
                        command = print1)
printButton1.grid(row=359,column=350)
my_w.mainloop()
