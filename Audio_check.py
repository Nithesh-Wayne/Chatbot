from gtts import gTTS
from time import sleep
import os
import pyglet

tts = gTTS(text='Hello World', lang='en')
filename = "check.mp3"
tts.save(filename)

music = pyglet.media.load(filename, streaming=False)
music.play()

sleep(music.duration) #prevent from killing
os.remove(filename) #remove temperory file
