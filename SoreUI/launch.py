import sys
import json
import hashlib
import win32api
import tkinter as tk
from tkinter import simpledialog
from pathlib import Path
import runpy
def config():
    return json.load(open(str(Path(__file__).parent.joinpath('files').joinpath('settings.json')),'r'))

def msgbox(typ,title,msg):
    return win32api.MessageBox(
    0,
    msg,
    title,typ)  

def get_input(title="Input Box", prompt="Enter text:"):
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring(title, prompt)

if config()['Security']['Enabled'] and config()['Security']["SecurityMethod"] == "Password":
    pass_ = hashlib.sha256(config()['Security']['SecurityVariables']['InsecurePassword'].encode()).hexdigest()
    user_input = get_input("Security", "Enter your password:")
    if not user_input:
        msgbox(16,"Security","Access Denied.\nPlease try again.")
        sys.exit(0)
    if hashlib.sha256(user_input.encode()).hexdigest() == pass_:
        msgbox(64,"Security","Access Granted.")
    else:
        msgbox(16,"Security","Access Denied.\nPlease try again.")
        sys.exit(0)

sys.path.append(Path(__file__).parent.joinpath('files').__str__())

import main
main.main()
