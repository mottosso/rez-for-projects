# -*- coding: utf-8 -*-

name = 'maya'

version = '2017.0.1'

requires = []

def commands():
    global env
    global system
    
    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\autodesk\maya2017\bin")
    
    elif system.platform == "linux":
        env["PATH"].prepend("/opt/maya2017/bin")

timestamp = 1555699195

format_version = 2
