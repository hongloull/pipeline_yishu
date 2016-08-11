import os
from globalVar import *

def leadMel():
    KEY = 'MAYA_SCRIPT_PATH'
    dirs = __getSubFloders__(g.MAYA_SCRIPT_PATH, 'mel')
    print 'Lead Mel:'
    if not os.environ.has_key(KEY):
        os.environ[KEY] = ''
    for dir in dirs:
        if dir not in os.environ[KEY]:
            os.environ[KEY] = dir + ';' + os.environ[KEY]
            print dir

def __getSubFloders__(rootPath, exts=None):
    # exts: 'mel' or ['py','pyc','pyo']
    output = []
    for root, dirs, files in os.walk(rootPath):
        if exts==None:
            if len(files):
                output.append(root)
            continue
        find = 0
        for file in files:
            fe = os.path.splitext(file)[-1]
            try:
                fe = fe[1:]
            except:
                pass
            if type(exts)==type([]) or type(exts)==type(()):
                if fe in exts:
                    find=1
            elif fe==exts:
                    find=1
            if find==1:
                output.append(root)
                break
    return output
