from cgpython.utils import Path
from cgmaya.general import workspace
from cgmaya import assembly
reload(assembly)
from cgmaya.entity import shot
reload(shot)


class MayaScene(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(MayaScene, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def __init__(self, *args, **kwargs):
        self._rootDir = workspace.Workspace().rootDir

    @property
    def rootDir(self):
        return self._rootDir

    @staticmethod
    def open(filePath=''):
        cmds.file(filePath, ignoreVersion=True, prompt=False,
                  type="mayaAscii",
                  open=True, force=True, options="v=0;")

    @staticmethod
    def save():
        cmds.file(save=True, force=True, options="v=0;",
                  type='mayaAscii', prompt=False)

    @staticmethod
    def new():
        cmds.file(new=True, force=True, prompt=False)

    @staticmethod
    def saveAs(filePath=''):
        cmds.file(rename=filePath)
        MayaScene.save()

    @property
    def shortName(self):
        return Path(cmds.file(q=True, sn=True, shn=True)).splitext()[0]

    @property
    def sceneName(self):
        return Path(cmds.file(q=True, sn=True))


class MayaAssetScene(MayaScene):

    def __init__(self, *args, **kwargs):
        super(MayaAssetScene, self).__init__(*args, **kwargs)


class MayaShotScene(MayaScene):
    PATH_TEMPLATE = 'scenes/sequence/{sequence}/{shot}/{step}'

    def __init__(self, *args, **kwargs):
        super(MayaShotScene, self).__init__(*args, **kwargs)
        # temp workaroud to get shot depend on maya scene name
        self._shot = shot.Shot(name=self.shortName,
                               sequenceName=self.shortName.split('_', 1)[0])
        self._path = None
        self._absPath = None

    @property
    def shot(self):
        return self._shot

    @property
    def path(self):
        if self._path is None:
            self._path = Path(self.PATH_TEMPLATE.format(
                sequence=self.shot.sequenceName, shot=self.shot.name, step='ani'))
            if not self.absPath.isdir():
                self.absPath.makedirs()
        return self._path

    @property
    def absPath(self):
        if self._absPath is None:
            self._absPath = self.rootDir / self.path
        return self._absPath

    @staticmethod
    def _getTopAssemblyNodes():
        assemblyNodes = cmds.ls(type='assemblyReference')
        topTransformNodes = cmds.ls(assemblies=True)
        return set(assemblyNodes).intersection(topTransformNodes)

    def exportAssemblyEdits(self):
        """
        Export all assembly reference nodes's edits.
        """
        assemblyNodes = self._getTopAssemblyNodes()
        if assemblyNodes:
            for assemblyNode in assemblyNodes:
                io.write('export assembly edits for {0}'.format(assemblyNode))
                fPath = self.absPath.joinpath(
                    '{0}.ase.txt'.format(assemblyNode))
                assembly.Assembly.exportEdits(assemblyNode,
                                              fPath)
                io.write('exported assembly edits: {0}'.format(fPath))
        else:
            io.error('There is no assembly reference node in current scene.')

    def importAssemblyEdits(self):
        assemblyNodes = self._getTopAssemblyNodes()
        if assemblyNodes:
            for assemblyNode in assemblyNodes:
                io.write('import assembly edits for {0}'.format(assemblyNode))
                fPath = self.absPath.joinpath(
                    '{0}.ase.txt'.format(assemblyNode))
                assembly.Assembly.importEdits(assemblyNode,
                                              fPath)
                io.write('imported assembly edits: {0}'.format(fPath))
        else:
            io.error('There is no assembly reference node in current scene.')
