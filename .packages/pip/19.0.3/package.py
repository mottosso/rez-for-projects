# -*- coding: utf-8 -*-

name = 'pip'

version = '19.0.3'

requires = ['rezutils-1']

def commands():
    global env
    global this
    global system
    global expandvars
    
    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].prepend(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1555749563

format_version = 2

environ = {'PYTHONPATH': ['{root}/python']}
