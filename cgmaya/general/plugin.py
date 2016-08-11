def reloadPlugin(pluginName):
    """
    Safely reloading a plug-in without restarting Maya
    """
    # clear the scene
    cmds.file(f=True, new=True)

    # Clear the undo queueW
    cmds.flushUndo()

    # Unload the plug-in
    cmds.unloadPlugin(pluginName)

    # Reload the plug-in
    cmds.loadPlugin(pluginName)


def loadPlugin(pluginName):
    """
    loading a plug-in
    """
    if not cmds.pluginInfo(pluginName, query=True, loaded=True):
        cmds.loadPlugin(pluginName)
