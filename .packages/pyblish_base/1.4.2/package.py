# -*- coding: utf-8 -*-

name = 'pyblish_base'

version = '1.4.2'

requires = ['base-1']

def commands():
    global env
    global this
    global system
    global expandvars
    
    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1555748306

format_version = 2

environ = {'PYTHONPATH': ['{root}/python']}
