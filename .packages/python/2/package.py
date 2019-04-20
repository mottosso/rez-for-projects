# -*- coding: utf-8 -*-

name = 'python'

version = '2'

def commands():
    global env
    global system
    import os
    
    if system.platform == "windows":
        dirname = r"c:\python27"
    elif system.platform == "linux":
        dirname = r"/usr/bin"
    
    assert os.path.exists(dirname), (
        "Python could not be found on this system"
    )
    
    env.PATH.append(dirname)

timestamp = 1555700116

format_version = 2
