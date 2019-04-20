# -*- coding: utf-8 -*-

name = 'nuke'

version = '11.3.2'

requires = []

def commands():
    global env
    global system
    
    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\nuke11.3v2\bin")
    
    elif system.platform == "linux":
        env["PATH"].prepend("/opt/nuke11.3v2/bin")

timestamp = 1555699229

format_version = 2
