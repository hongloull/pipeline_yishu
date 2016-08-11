class AbcBase(object):

    def __init__(self):
        self._currentTime = None

    @property
    def currentTime(self):
        if self._currentTime is None:
            self._currentTime = cmds.currentTime(q=True)
        return self._currentTime


class GpuExport(AbcBase):
    """
    Export gpu cache command looks as below:
        gpuCache -startTime 1 -endTime 1 -optimize -optimizationThreshold
        40000 -writeMaterials -dataFormat ogawa -directory
        "/data/projects/assemblyTest/cache/alembic"
        -fileName "sphere.gpu" sphere;

    """

    def __init__(self, ):
        super(GpuExport, self).__init__()

    def export(self, node, startTime=None, endTime=None,
               directory='', fileName='', **kwargs):
        if startTime is None:
            startTime = self.currentTime
        if endTime is None:
            endTime = self.currentTime
        options = {"startTime": startTime,
                   "endTime": endTime,
                   "writeMaterials": True,
                   "optimize": True,
                   "optimizationThreshold": 40000,
                   "useBaseTessellation": True,
                   "saveMultipleFiles": False,
                   "fileName": fileName,
                   "directory": directory}
        options.update(kwargs)
        cmds.gpuCache(node, **options)


class AbcExport(AbcBase):
    """
    Export abc commands looks as below:
        opts = '-frameRange 101 101 -frameRelativeSample -0.15
        -frameRelativeSample 0 -frameRelativeSample 0.15
        -attr SubDivisionMesh -stripNamespaces -uvWrite -worldSpace
        -dataFormat ogawa -root pCube1 -file /tmp/test.abc'
        cmds.AbcExport(j=self._options)

    """

    def __init__(self, startFrame=None, endFrame=None,
                 frameRelativeSamples=(-.25, 0, .25),
                 attributes=[], root='', file='', stripNamespaces=True,
                 uvWrite=True, worldSpace=True, dataFormat='ogawa'):
        super(AbcExport, self).__init__()
        if startFrame is None:
            startFrame = self.currentTime
        if endFrame is None:
            endFrame = self.currentTime
        options = []
        options.append(('-frameRange '
                        '{startFrame} '
                        '{endFrame}').format(startFrame=startFrame,
                                             endFrame=endFrame))
        for sample in frameRelativeSamples:
            options.append('-frameRelativeSample {0}'.format(sample))
        for attr in attributes:
            options.append('-attr {0}'.format(attr))
        if stripNamespaces:
            options.append('-stripNamespaces')
        if uvWrite:
            options.append('-uvWrite')
        if worldSpace:
            options.append('-worldSpace')

        options.append(('-dataFormat {dataFormat} '
                        '-root {root} '
                        '-file {outputFile}').format(dataFormat=dataFormat,
                                                     root=root,
                                                     outputFile=file))

        self._options = ' '.join(options)

    def export(self):
        return cmds.AbcExport(j=self._options)
