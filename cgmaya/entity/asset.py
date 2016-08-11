from functools import partial
from cgmaya import alembic
reload(alembic)
from cgmaya.general import workspace
from cgmaya.arnold import standin
reload(standin)
from cgmaya import assembly
reload(assembly)
from cgmaya import mayascene


class Asset(object):

    def __init__(self, name='', path=None, family=''):
        self._name = name
        self._path = path
        self._absPath = None
        self._family = family

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def family(self):
        return self._family


class MayaAsset(Asset):
    TYPE = ''
    PATH_TEMPLATE = 'scenes/asset/{type}/{family}/{name}'

    def __init__(self, **kwargs):
        super(MayaAsset, self).__init__(**kwargs)
        self._rootDir = workspace.Workspace().rootDir

    @property
    def rootDir(self):
        return self._rootDir

    @property
    def path(self):
        if self._path is None:
            self._path = Path(MayaAsset.PATH_TEMPLATE.format(
                type=self.TYPE, family=self.family, name=self.name))
            if not self.absPath.isdir():
                self.absPath.makedirs()
        return self._path

    @property
    def absPath(self):
        if self._absPath is None:
            self._absPath = self.rootDir / self.path
        return self._absPath

    @property
    def maFilePath(self):
        return self.path / '{0}.ma'.format(self.name)

    @property
    def abcFilePath(self):
        return self.path / '{0}.abc'.format(self.name)

    @property
    def gpuFilePath(self):
        return self.path / '{0}.gpu.abc'.format(self.name)

    @property
    def assFilePath(self):
        return self.path / '{0}.ass.ma'.format(self.name)

    @property
    def standinFilePath(self):
        return self.path / '{0}.ass'.format(self.name)

    @property
    def asdFilePath(self):
        """
        Assembly definition scene file path.
        """
        return self.path / '{0}.asd.ma'.format(self.name)

    @property
    def asrFilePath(self):
        """
        Assembly reference scene file path.
        """
        return self.path / '{0}.asr.ma'.format(self.name)

    def exportMa(self, node=''):
        io.write('export ma for {0}'.format(node))
        io.write(self.maFilePath)
        io.write(self.family)
        cmds.select(node, r=True)
        cmds.file(self.maFilePath, f=True, options='v=0',
                  type='mayaAscii', exportSelected=True)
        io.write('exported ma: {0}'.format(self.maFilePath))

    def exportStandin(self, node=''):
        io.write('export standin: {0}'.format(node))
        standin.StandIn.export(filePath=self.standinFilePath,
                               node=node)
        io.write('exported standin: {0}'.format(self.standinFilePath))

    def createAssScene(self, node=''):
        """
        Generate Maya ma scene file which imported ass standin file.
        """
        io.write('create ass maya scene')
        mayascene.MayaScene.new()
        standin.StandIn().importToScene(filePath=self.standinFilePath,
                                        name=node)
        mayascene.MayaScene.saveAs(filePath=self.assFilePath)
        io.write('created ass maya scene: {0}'.format(self.assFilePath))

    def exportAbc(self, node=''):
        io.write('export abc cache')
        # for abc export, should use abs path, else root dis is "../alembic"
        alembic.AbcExport(root=node,
                          file=self.rootDir / self.abcFilePath).export()
        io.write('exported abc cache: {0}'.format(self.abcFilePath))

    def exportGpu(self, node=''):
        io.write('export gpu cache')
        fileName = self.gpuFilePath.basename().splitext()[0]
        alembic.GpuExport().export(node,
                                   fileName=fileName,
                                   directory=self.gpuFilePath.dirname())
        io.write('exported gpu cache: {0}'.format(self.gpuFilePath))

    def createAssemblyDefinitionScene(self):
        self._preCreateAssemblyDefinitionScene()
        assemblyNode = self._performCreateAssemblyDefinitionScene()
        self._postCreateAssemblyDefinitionScene([assemblyNode])

    def _performCreateAssemblyDefinitionScene(self):
        mayascene.MayaScene.new()
        assemblyNode = assembly.Assembly.createAssembly(self)
        mayascene.MayaScene.saveAs(filePath=self.asdFilePath)
        return assemblyNode

    def _preCreateAssemblyDefinitionScene(self):
        io.write('create assembly definition scene: {0}'.format(
            self.asdFilePath))

    def _postCreateAssemblyDefinitionScene(self, assemblyNodes):
        mayascene.MayaScene.save()
        io.write('created assembly definition scene: {0}'.format(
            self.asdFilePath))

    def referenceAssemblyDefinitionScene(self):
        io.write('reference assembly definition scene')
        name = '{0}_AR'.format(self.asdFilePath.basename().
                               splitext()[0].replace('.', '_'))
        assembly.Assembly.referenceAssembly(self, name=name)
        io.write('referenced assembly definition scene: {0}'.format(
            self.asdFilePath))

    def package(self, node=''):
        self._prePackage(node)
        self._performPackage(node)
        self._postPackage(node)

    def _prePackage(self, node=''):
        io.write('pre package')

    def _postPackage(self, node=''):
        io.write('post package')

    def _performPackage(self, node=''):
        io.write('perform package for {0}'.format(node))


class CharAsset(MayaAsset):
    TYPE = 'char'

    def __init__(self, **kwargs):
        super(CharAsset, self).__init__(**kwargs)


class PropAsset(MayaAsset):
    TYPE = 'prop'

    def __init__(self, **kwargs):
        super(PropAsset, self).__init__(**kwargs)


class EnvAsset(MayaAsset):
    TYPE = 'env'

    def __init__(self, **kwargs):
        super(EnvAsset, self).__init__(**kwargs)

    def _performPackage(self, node=''):
        super(EnvAsset, self)._performPackage(node=node)
        self.exportMa(node)
        self.exportAbc(node)
        self.exportGpu(node)
        self.exportStandin(node)
        self.createAssScene(node)
        self.createAssemblyDefinitionScene()


class SingleEnvAsset(EnvAsset):

    def _postCreateAssemblyDefinitionScene(self, assemblyNodes):
        # switch active label to "gpu"
        assembly.Assembly.switchLabel(assemblyNodes, 'gpu')
        super(SingleEnvAsset, self)._postCreateAssemblyDefinitionScene(
            assemblyNodes)


class AssemblyEnvAsset(EnvAsset):

    def _postCreateAssemblyDefinitionScene(self, assemblyNodes):
        # switch active label to "ma"
        assembly.Assembly.switchLabel(assemblyNodes, 'ma')
        super(AssemblyEnvAsset, self)._postCreateAssemblyDefinitionScene(
            assemblyNodes)
