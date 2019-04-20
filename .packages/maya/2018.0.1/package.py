# -*- coding: utf-8 -*-

name = 'maya'

version = '2018.0.1'

requires = []

def commands():
    global env
    global system
    
    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\autodesk\maya2018\bin")
    
    elif system.platform == "linux":
        env["PATH"].prepend("/opt/maya2018/bin")

timestamp = 1555699198

format_version = 2
