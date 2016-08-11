import os
from globalVar import *

def setEnv():
    ENV = g.ENV
    print 'Set Env:'
    for key in ENV:
        dir = ENV[key]
        if not os.environ.has_key(key):
            os.environ[key] = ''
        if dir not in os.environ[key]:
            print key,dir
            os.environ[key] = dir + os.environ[key]
