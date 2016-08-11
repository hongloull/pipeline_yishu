print('init pipeline')

import __builtin__
exec(('import os.path;from maya import cmds;'
      'from maya import mel;import pymel.core as pm;'),
     vars(__builtin__))

import setEnv
setEnv.setEnv()

import leadMel
leadMel.leadMel()


import scriptJobFunction
pm.scriptJob(event=["SceneOpened", scriptJobFunction.open], permanent=True)
print 'activate open script job'

# set project
# import scripts.general.project as project
# project.setProject()

import pymel.mayautils
import menu_pipeline
print 'create pipeline custom menu'
pymel.mayautils.executeDeferred(menu_pipeline.loadMenu)
