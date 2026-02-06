import os 
from pystyle import Colorate, Colors

def gradient(text):
    return Colorate.Horizontal(Colors.purple_to_blue, text, 1)

def success(text):
    return Colorate.Horizontal(Colors.green_to_white, text, 1)

def failure(text):
    return Colorate.Horizontal(Colors.red_to_white, text, 1)
