# -*- coding: utf-8 -*-

name = 'lotr'

version = '1.13.2'

requires = [
    'base-1',
    '~maya-2011',
    '~nuke-9',
    '~houdinifx-11',
    '~mari-0.2'
]

def commands():
    global env
    global this
    global expandvars
    
    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1555748983

format_version = 2

environ = \
    {'PRODUCTION_TRACKER_ID': 'lotr-124',
     'PROJECT_NAME': 'Lord of the Rings',
     'PROJECT_PATH': '{env.PROJECTS_PATH}/lotr'}
