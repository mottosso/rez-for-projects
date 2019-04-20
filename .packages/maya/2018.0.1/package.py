# -*- coding: utf-8 -*-

name = 'maya'

version = '2018.0.1'

requires = []

def commands():
    import os
    global env
    global system
    
    if system.platform == "windows":
        path = r"c:\program files\autodesk\maya2018\bin"
    
    elif system.platform == "linux":
        path = "/opt/maya2018/bin"
    
    assert os.path.exists(path), "Missing files: %s" % path
    env["PATH"].prepend(path)

timestamp = 1555699198

format_version = 2
