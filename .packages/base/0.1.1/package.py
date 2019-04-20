# -*- coding: utf-8 -*-

name = 'base'

version = '0.1.1'

requires = []

def commands():
    global env
    global this
    global expandvars
    
    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1555698593

format_version = 2

environ = \
    {'GITLAB_URI': 'https://gitlab.mycompany.co.jp',
     'PYTHONDONTWRITEBYTECODE': '1'}
