import os, shutil
import sys
import ctypes
from ctypes.wintypes import MAX_PATH

class core:
    ENV = 'Maya.env'
    MAYA_VER = ('2016')
    source_env = ''
    maya_list = []
    
    def __init__(self):
        self.getCurrentPath()
        self.getMayaVerList()
        
    def run(self):
        for item in self.maya_list:
            target_env = os.path.join(item, self.ENV)
            print target_env
            self.backup(target_env)
            # self.copy(target_env)
            self.appendMayaEnv(target_env)
    
    def backup(self, file):
        new = file
        num = 1
        while(os.path.isfile(new)):
            new = '%s.%03d.bak' % (file, num)
            num +=1
        if not new==file:
            try:
                shutil.copy2(file, new)
                print 'backup %s to %s' % (self.ENV, new)
            except:
                print 'Failed backeup %s to %s' % (self.ENV, new)
        
    def copy(self, file):
        try:
            shutil.copy2(self.source_env, file)
            print 'Copy %s to %s' % (self.source_env, file)
        except:
            print 'Failed copy %s to %s' % (self.source_env, file)
            
    def appendMayaEnv(self,file):
        with open(file,'a') as f:
            f.write('\n')
            with open(self.source_env,'r') as sourceF:
                for x in sourceF:
                    f.write('{0}\n'.format(x))
    
    def getCurrentPath(self):
        path = sys.path[0]
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        self.source_env = os.path.join(path, self.ENV)
        
    def getUserDocuments(self):
        """
        get user's documents:
        Example: C:\Users\username\Documents
        """
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            #print(buf.value)
            return buf.value
        else:
            print("get user documents Failure!")
            return None
    
    def getMayaVerList(self):
        self.maya_list = []
        try:
            docPath = self.getUserDocuments()
            mayaPath = os.path.join(docPath, 'maya')
            folders = os.listdir(mayaPath)
            for item in folders:
                path = os.path.join(mayaPath, item)
                if os.path.isdir(path) and item in self.MAYA_VER:
                    self.maya_list.append( path )
        except:
            pass
    


def main():
    obj = core()
    obj.run()
        

main()
