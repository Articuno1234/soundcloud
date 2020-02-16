version = "0.2.1"

# Discord RPC doesn't work for this version at the moment!

from tkinter import *
import tkinter as tk
import youtube_dl
import os
import sys
import pygame as pg
from PIL import Image
import requests
from io import BytesIO
import urllib.request
from urllib.request import urlopen
import io
import base64
try:
    import rpc
    client_id = '676288890331463700' #Soundcloud Client ID (Don't Change Unless you want to change the name)
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    print("RPC connection successful.")
    discordsupport = True
except:
    discordsupport = False
import time

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'mp3',
    'outtmpl': '%(extractor)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def download_images(url, title=""):
    # In order to fetch the image online
    # WIP
    try:
        import urllib.request as uril
    except ImportError:
        import urllib as uril
    uril.urlretrieve(url, "{}.jpg".format(title))

def discordup(track, url, aurl, artist=None):
    start_time = time.time()
    if artist == None:
        lt = aurl
    else:
        lt = "{}/{}".format(artist, aurl)
    activity = {
        "state": "Playing a Track... {}".format(lt),
        "details": "BETA v{}".format(version),
        "timestamps": {
            "start": start_time
        },
        "assets": {
            "small_text": lt,
            "small_image": "playb",
            "large_text": "Playing a Track.",
            "large_image": "sc"
        }
    }
    rpc_obj.set_activity(activity)

def offlineplayy(file, *, loop=None, stream=False):
    volume=0.8
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    pg.mixer.music.load("soundcloud-" + file + ".mp3")
    print("Now Playing {}...".format(file))
    pg.mixer.music.play()

def from_url(url, *, loop=None, stream=False):
    volume=0.8
    scurl = "https://soundcloud.com/{}".format(url)
    data = ytdl.extract_info(scurl)
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    
    if 'entries' in data:
        data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    pg.mixer.music.load(filename)
    print("Now Playing {}...".format(url))
    pg.mixer.music.play()
    start_time = time.time()
    if discordsupport == True:
        discordup(filename, scurl, url)
        print("[Discord] Set Rich Presence!")
    else:
        print("[Discord] Discord not Found!")

def search(query, *, loop=None, stream=False):
    volume=0.8
    data = ytdl.extract_info(query)
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    
    if 'entries' in data:
        data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    pg.mixer.music.load(filename)
    print("Now Playing {}...".format(data['title']))
    nowplaying = Tk()
    nowplaying.title('{} - Soundcloud Client v{}'.format(data['title'], version))
    sec = 0
    minu = 0
    hur = 0
    for f in range(int(data['duration'])):
        sec += 1
        if sec == 60:
            minu += 1
            sec = 0
            if minu == 60:
                hur +=1
                minu = 0
    np = Label(nowplaying, text="Now Playing: {} by {}\n\nViews: {} | Likes: {} | Reposts: {}\nDuration: {}:{}:{}".format(data['title'], data['uploader'], data['view_count'], data['like_count'], data['repost_count'], hur, minu, sec))
    np.pack()
    #image_byt = urlopen(data['thumbnail']).read()
    #image_b64 = base64.encodestring(image_byt)
    #photo = PhotoImage(data=image_b64)
    #canvas = Canvas(nowplaying, width = 512, height = 512)      
    #canvas.pack()  
    #canvas.create_image(20,20, anchor=NW, image=photo)
    pg.mixer.music.play()
    start_time = time.time()
    if discordsupport == True:
        discordup(filename, data['url'], data['title'], data['uploader'])
        print("[Discord] Set Rich Presence!")
    else:
        print("[Discord] Discord client not Found!")

master = Tk()
master.title('Soundcloud Client v{}'.format(version))
txr = Label(master, text="Soundcloud Client Made by Artucuno#1898")
txr.pack()
e = Entry(master)
e.pack()

e.focus_set()

def srch():
    search(e.get())

def offlineplay():
    offlineplayy(e.get())

def callback():
    from_url(e.get())

def stop():
    pg.mixer.music.stop()

def pause():
    pg.mixer.music.pause()

def resume():
    pg.mixer.music.unpause()

def loop():
    try:
        pg.mixer.music.play(-1)
    except:
        print("Make sure you press play first!")

src = Button(master, text="Search", width=10, command=srch)
src.pack()
b = Button(master, text="Play", width=10, command=callback)
b.pack()
off = Button(master, text="Offline Play", width=10, command=offlineplay)
off.pack()
stop = Button(master, text="Stop", width=10, command=stop)
stop.pack()
pause = Button(master, text="Pause", width=10, command=pause)
pause.pack()
resu = Button(master, text="Resume", width=10, command=resume)
resu.pack()

lop = Button(master, text="Loop", width=10, command=loop)
lop.pack()

e.pack()
canvas = Canvas(master, width = 512, height = 512)      
canvas.pack()      
img = PhotoImage(file="data/assets/sc.png")      
canvas.create_image(20,20, anchor=NW, image=img) 

text = e.get()
mainloop()

text = content.get()
content.set(text)
