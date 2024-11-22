# Import libraries
import windowsapps
import pyautogui as pyg
import winapps
import win32ui
import win32api
import win32con
import cython
import webbrowser
import subprocess
from pathlib import Path
import pyttsx3
from threading import Thread
from gtts import gTTS, lang as glang
from playsound import playsound
import os
import time
import random
from pydub import AudioSegment
from pydub.playback import play
from importlib import import_module
from deep_translator import GoogleTranslator

# -------------------------------------------------
# Initials
_TTSengine = pyttsx3.init()
_TTSengine.setProperty('voice', _TTSengine.getProperty('voices')[1].id)
_IS_SPEAKING = False
# ------------------------------------------------
# GLOBAL VARIABLES
MESSAGEBOX_STYLE_ASK_YES_NO=4
MESSAGEBOX_STYLE_ASK_OK_CANCEL=1
MESSAGEBOX_STYLE_ERROR=16
MESSAGEBOX_STYLE_QUESTION=32
MESSAGEBOX_STYLE_INFO=64
# -----------------------------------------------
# METHODS

def convert_path(path:str): # Converts linux path to windows path
    return str(Path(path).absolute())

def MessageBox(message:str,title:str,style:int=0)->str:
    _= win32ui.MessageBox(message,title,style) # Shows MessageBox with arguements
    # checks for codes for answers and returns simpler answers
    if _ == 1:
        return "ok"
    elif _ == 2:
        return "cancel"
    elif _ == 6:
        return "yes"
    elif _ == 7:
        return "no"
    else:
        return _
def OpenApp(appname:str)->bool:
    try:
        windowsapps.open_app(appname) # Uses a library to search and open application
        return True # returns true if the application is found and launched 
    except:
        return False # returns false if the application is not found

def ListInstalledAppsName()->list:
    output=[] # the return variable
    for app in list(winapps.list_installed()): # loops through installed applications using "winapps" library
       output.append(app.name) # appends only the name of the applications installed
    return output # returns the names of the applications installed

def UninstallApp(appname:str)->bool:
    if winapps.search_installed(appname)==[]:return False # Returns false if installed application is not found
    ask=MessageBox(f"Do you really want to uninstall {appname}?","AI Assistant",MESSAGEBOX_STYLE_ASK_YES_NO) # makes sure if user wants their application to be deleted
    if ask == "yes":
        winapps.uninstall(appname) # uninstalls the application
    return True

def OpenUrl(url:str): 
    return webbrowser.open(url) # simply opens a url in browser

def SearchOnGoogle(keywords:str):
    keywords=keywords.replace(" ","+") # replace spaces with "+" so it can be used for search
    url = "https://www.google.com/search?q="+keywords # adds the keywords to search url
    return webbrowser.open(url) # simply searches on google

def OpenPath(path:str):
    # simply opens a path in windows explorer
    return subprocess.Popen(["explorer.exe",convert_path(path)])

def translate(text:str,from_:str,to:str):
    t=GoogleTranslator()
    return t.translate(text)
def _TextToSpeech(text:str,lang:str):
    global _IS_SPEAKING
    if lang not in list(glang.tts_langs().keys()): 
        text = translate(text,"auto","en")
    # if _TTSengine._inLoop == True:
    #     _TTSengine.endLoop()
    #     _TTSengine.stop()
    # _TTSengine.say(text)
    # _TTSengine.runAndWait()
    if _IS_SPEAKING:
        while _IS_SPEAKING:
            time.sleep(0.1)
        
    tts=gTTS(text,lang=lang)
    f=f"audio/audio{random.randint(99999,199999)}.mp3"
    tts.save(f)
    # playsound(f)
    # time.sleep(1)
    # os.remove(f)
    _IS_SPEAKING = True
    try:
        sound= AudioSegment.from_mp3(f)
        play(sound)
    except:
        playsound(f)
    _IS_SPEAKING = False
    os.remove(f)

# TextToSpeech function do not support persian/farsi language instead you can use Finglish typing like TextToSpeech("Salam",lang="en") 
def TextToSpeech(text:str,lang:str='en'): # Recommended to use English as text and if needed to speak in another language just use the lang parameter
    # t=Thread(target=_TextToSpeech,args=(text,))
    # t.start()
    _TextToSpeech(text,lang)

def import_lib(libname:str):
    return import_module