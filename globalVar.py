import os
from os.path import join


class Global:
    SYSTEM_NAME = 'pipeline'

    MAIN_PATH = os.path.abspath(os.path.dirname(__file__))

    MAYA_SCRIPT_PATH = join(MAIN_PATH, 'scripts')
    PYTHON_PATH = join(MAIN_PATH, 'scripts')
    MAYA_PLUG_IN_PATH = join(MAIN_PATH, 'PlugIn')
    PATH = join(MAIN_PATH, 'PlugIn')
    ICON_PATH = join(MAIN_PATH, 'Icon')

    LIB_PATH = join(MAIN_PATH, 'lib')
    DATA_PATH = join(MAIN_PATH, 'Data')

    MENUITEMS_XML = join(DATA_PATH, 'menuItems.xml')

    if os.name == 'posix':
        sep = ':'
    else:
        sep = ';'
    ENV = {'MAYA_PLUG_IN_PATH': MAYA_PLUG_IN_PATH + sep,
           'MAYA_SCRIPT_PATH': MAYA_SCRIPT_PATH + sep,
           'XBMLANGPATH': ICON_PATH + sep,
           'PATH': PATH + sep + 'C:/Program Files/Autodesk/Maya2014/bin/plug-ins;'}

    MAYA_FORCE_REF_READ = 1
# init.
g = Global()
