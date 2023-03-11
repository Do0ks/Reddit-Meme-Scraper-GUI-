import asyncio
import random
import praw
import requests
import os
import webbrowser
import urllib.request
import threading
import tkinter
from tkinter.ttk import Progressbar
from tkinter import ttk, filedialog, CENTER, HORIZONTAL, StringVar, END
from urllib.parse import urlparse



SubReddits = ["funnymeme", "DirtyMemes", "thensfwmemes", "BabyYodaMemes", "lol", "memes", "dankmemes", "ComedyCemetery", "PrequelMemes", "terriblefacebookmemes", "PewdiepieSubmissions", "funny", "AdviceAnimals", "MemeEconomy", "meme", "surrealmemes"]
url = "https://paypal.me/automationz?country.x=US&locale.x=en_US"

root = tkinter.Tk()
root.geometry("400x195")
root.title("RMD")
root.resizable(0,0)
root.config(background='#505050')
root.iconbitmap('reddit.ico')


Ltitle = tkinter.Label(root, text="Reddit Meme Downloader", font=('Cambria', 13, 'bold','underline'), bg='#505050', fg='#ff2121', cursor="hand2")
Ltitle.pack(padx=(3), pady=(1), anchor='w')
Ltitle.bind("<Button-1>", lambda e:open_url(url))

PFrame = tkinter.LabelFrame(root, text="Properties", borderwidth=3, background='#505050')


Ldir = tkinter.Label(PFrame, text="Save Directory:", font=('Cambria', 9), bg='#505050', fg='#000000')
Ldir.pack(padx=(1), pady=(1), anchor='w')

SDEntry = tkinter.Entry(PFrame, width=57, bd=5,bg="#cacaca")
SDEntry.insert(0, str('C:/Users\conta\Desktop'))
SDEntry.pack(pady=(1),padx=(1), anchor="w")

Ltype = tkinter.Label(PFrame, text="/r/:", font=('Cambria', 9), bg='#505050', fg='#000000')
Ltype.pack(pady=(5),padx=(0), anchor="w")

SREntry = tkinter.Entry(PFrame, width=35, bd=2, bg="#cacaca")
SREntry.insert(0,str(random.choice(SubReddits)))
SREntry.place(x=27, y=56)

LQTY = tkinter.Label(PFrame, text="Qty:", font=('Cambria', 9), bg='#505050', fg='#000000')
LQTY.place(x=245,y=56)

QTEntry = tkinter.Entry(PFrame, width=4, bd=2, justify=CENTER, bg="#cacaca")
QTEntry.insert(0,str('10'))
QTEntry.place(x=271, y=55)

StatusLable = tkinter.Label(root, text="Reddit Meme Downloader!", bd=1, relief=tkinter.SUNKEN, anchor=CENTER, background='#ababab', font=('Cambria', 10, 'bold'))
StatusLable.pack(fill=tkinter.X, side=tkinter.BOTTOM, ipady=2)

PFrame.pack(pady=1, padx=2, fill="both")

running = False

def open_url(url):
   webbrowser.open_new_tab(url)

x = 0
nd = 0
def go():
    threading.Thread(target=scrape())


def scrape():
    if SDEntry.get() == "":
        StatusLable.config(text="You Must Choose A Directory To Save Memes In!")
        return
    if SREntry.get() == "":
        StatusLable.config(text="You Must Choose A Sub Reddit To Get Memes From!")
        return
    global x
    global nd
    x = 0
    nd = 0
    root.geometry("400x223")
    progress = Progressbar(root, orient=HORIZONTAL, length=385, mode='determinate', maximum=int(QTEntry.get()))
    progress.place(x=8, y=171)

    global running
    running = True
    reddit = praw.Reddit(client_id = 'YOUR_ID',
                         client_secret = 'YOUR_TOKEN',
                         user_agent = 'YOUR_AGENT')

    qty = int(QTEntry.get())
    name = ["A-", "B-", "C-", "D-", "E-", "F-", "G-", "H-", "I-", "J-", "K-", "L-", "M-", "N-", "O-", "P-", "Q-", "R-", "S-", "T-", "U-", "V-", "W-", "X-", "Y-", "Z-", ]
    idenifier = ["!", "@", "#", "$", "%", "^", "&", "(", ")"]
    Rname = random.choice(name)
    Ridenifier = random.choice(idenifier)
#   reddit.subreddit(SREntry.get()).new(limit=qty)
    for submission in reddit.subreddit(SREntry.get()).new(limit=qty): #can use hot,top,new,rising
        if running == True:
            try:
                x += 1
                urls= submission.url
                link = requests.get(urls).url
                path = urlparse(link).path
                ext = os.path.splitext(path)[1]
                if ext == "":
                    progress['value'] = x
                    sus = x - nd
                    if x == qty:
                        progress.destroy()
                        root.geometry("400x195")
                        StatusLable.config(text=f"Download Complete! {sus} Successful, {nd} Failed")
                    else:
                        StatusLable.config(text=f"Couldn't Download Meme. {sus} Successful, {nd} Failed.")
                        nd += 1

                else:
                    urllib.request.urlretrieve(link, f"{SDEntry.get()}\!{Ridenifier}{Rname}{SREntry.get()}-{x}{ext}")
                    root.update()
                    progress['value'] = x
                    StatusLable.config(text=f"Downloading {x} of {qty} Memes")
                    print(nd)
                    if x == qty:
                        sus = x - nd
                        progress.destroy()
                        root.geometry("400x195")
                        StatusLable.config(text=f"Download Complete! {sus} Successful, {nd} Failed")
                    if running == False:
                        sus = x - nd
                        progress.destroy()
                        root.geometry("400x195")
                        StatusLable.config(text=f"Download Stopped At {x} Memes. {sus} Successful, {nd} Failed")
            except:
                pass
        else:
            return

def stop():
    global running
    global x
    global nd
    if running:
        running = False
    else:
        sus = x - nd
        StatusLable.config(text=f"Nothing Downloading, Last Download Was {sus} Memes, {nd} Failed.")


def folder():
    SDEntry.delete(0, END)
    dirname = filedialog.askdirectory(initialdir="/", title="Select Folder")
    SDEntry.insert(0,dirname)

def startfolder():
    os.startfile(SDEntry.get())

def DIR_ON_HOVER(e):
    StatusLable.config(text="Pick The Directory To Save Memes In!")

def DIR_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")

def SRENTRY_DOUBLE_CLICK(e):
    SREntry.delete(0, END)
    SREntry.insert(0,str(random.choice(SubReddits)))

def SRE_ON_HOVER(e):
    StatusLable.config(text="Double Click to Generate Random SubReddit.")

def SRE_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")

def SDE_ON_HOVER(e):
    StatusLable.config(text=f"Memes Will Save To {SDEntry.get()}")

def SDE_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")

def QTE_ON_HOVER(e):
    StatusLable.config(text="How Many Memes Do You Want To Download?")

def QTE_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")

def DL_ON_HOVER(e):
    StatusLable.config(text="Open The Current Save Directories Folder.")

def DL_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")

def LT_ON_HOVER(e):
    StatusLable.config(text="Made By: Do0ks aka NOP.                        Consider Donating! :D")

def LT_OFF_HOVER(e):
    StatusLable.config(text="Reddit Meme Downloader!")


style = ttk.Style()
style.configure("BW.TButton", foreground="black", background="#c00000",)

startButton = ttk.Button(root, text="Start!", style="BW.TButton", width=30, command=go)
startButton.place(x=7, y=139)

stopButton = ttk.Button(root, text="Stop!", style="BW.TButton", width=30, command=stop)
stopButton.place(x=204, y=139)

DIRButton = ttk.Button(PFrame, text="🔍", style="BW.TButton", width=3, command=folder)
DIRButton.place(x=359, y=24)
DIRButton.bind("<Enter>", DIR_ON_HOVER)
DIRButton.bind("<Leave>", DIR_OFF_HOVER)

DLButton = ttk.Button(PFrame, text="Downloads", style="BW.TButton", width=11, command=startfolder, )
DLButton.place(x=312, y=53.6)

SREntry.bind("<Double-Button-1>", SRENTRY_DOUBLE_CLICK)
SREntry.bind("<Enter>", SRE_ON_HOVER)
SREntry.bind("<Leave>", SRE_OFF_HOVER)

SDEntry.bind("<Enter>", SDE_ON_HOVER)
SDEntry.bind("<Leave>", SDE_OFF_HOVER)

QTEntry.bind("<Enter>", QTE_ON_HOVER)
QTEntry.bind("<Leave>", QTE_OFF_HOVER)

Ltitle.bind("<Enter>", LT_ON_HOVER)
Ltitle.bind("<Leave>", LT_OFF_HOVER)

DLButton.bind("<Enter>", DL_ON_HOVER)
DLButton.bind("<Leave>", DL_OFF_HOVER)



root.mainloop()
