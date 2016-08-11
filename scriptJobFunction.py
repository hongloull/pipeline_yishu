import pymel.core as pm


def open():
    # pm.mel.eval('renderThumbnailUpdate 0')
    # pm.mel.eval('EnableAll')
    # pm.currentUnit(l='centimeter',time='film')

    loadPluginCmd = ['from cgmaya.general import plugin']
    loadPluginCmd.append('plugin.loadPlugin("AbcImport")')
    loadPluginCmd.append('plugin.loadPlugin("mtoa")')
    pm.evalDeferred(';'.join(loadPluginCmd))
