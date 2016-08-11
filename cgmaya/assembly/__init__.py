from maya.app.general import editUtils


class AssemblyRepresentation(object):

    def __init__(self, name='', label='', data='', repType=''):
        self._name = name
        self._label = label
        self._data = data
        self._type = repType

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def data(self):
        return self._data

    @property
    def type(self):
        return self._type


class Assembly(object):

    @staticmethod
    def switchLabel(assemblyNodes, label):
        cmds.assembly(assemblyNodes, e=True, activeLabel=label)

    @staticmethod
    def getAssemblyNodes(selection=True):
        return cmds.ls(sl=selection,
                       type=['assemblyDefinition',
                             'assemblyReference'])

    @staticmethod
    def referenceAssembly(asset, **kwargs):
        """
        :Parameters:
          filePath: `str`
            assembly definition file path.
        """
        assemblyRef = cmds.assembly(type='assemblyReference',
                                    **kwargs)
        cmds.setAttr('{0}.definition'.format(assemblyRef),
                     asset.asdFilePath,
                     type='string')

    @staticmethod
    def createAssembly(asset):
        """
        :Parameters:
            asset: `cgmaya.entity.asset.MayaAsset`
        """
        assetAssembly = cmds.assembly(name=asset.name)
        reps = Assembly._generateRepresentations(asset)
        for rep in reps:
            io.write(asset.path.basename())
            cmds.assembly(assetAssembly,
                          edit=True,
                          createRepresentation=rep.type,
                          input=rep.data)
            if rep.type != 'Locator':
                cmds.assembly(assetAssembly,
                              edit=True,
                              repLabel=rep.data.basename(),
                              newRepLabel=rep.label)
            else:
                cmds.assembly(assetAssembly,
                              edit=True,
                              repLabel='Locator',
                              newRepLabel='locator')
        return assetAssembly

    @staticmethod
    def _generateRepresentations(asset):
        reps = []
        if asset.__class__.__name__ == 'SingleEnvAsset':
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='locator',
                                               data=asset.name,
                                               repType='Locator'))
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='abc',
                                               data=asset.abcFilePath,
                                               repType='Cache'))
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='gpu',
                                               data=asset.gpuFilePath,
                                               repType='Cache'))
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='ma',
                                               data=asset.maFilePath,
                                               repType='Scene'))
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='ass',
                                               data=asset.assFilePath,
                                               repType='Scene'))
        elif asset.__class__.__name__ == 'AssemblyEnvAsset':
            reps.append(AssemblyRepresentation(name=asset.name,
                                               label='ma',
                                               data=asset.asrFilePath,
                                               repType='Scene'))
        else:
            raise Exception(
                'Asset type is not "SingleEnvAsset" or "AssemblyEnvAsset"')
        return reps

    @staticmethod
    def getEditStrs(assemblyNode):
        """
        Get assembly reference edits.
        """
        edits = (edit.getString() for edit in editUtils.getEdits(
            assemblyNode, '') if edit.isApplied())
        return edits

    @staticmethod
    def exportEdits(assemblyNode, filePath):
        edits = Assembly.getEditStrs(assemblyNode)
        with open(filePath, 'w') as f:
            for editStr in edits:
                io.write('Write edit string: {0}'.format(editStr))
                f.write('{0}\n'.format(editStr))

    @staticmethod
    def importEdits(assemblyNode, filePath):
        with open(filePath, 'r') as f:
            for editStr in f:
                Assembly._applyEdits(assemblyNode, editStr)

    @staticmethod
    def _applyEdits(assemblyNode, editStr):
        cmds.select(assemblyNode, r=True)
        mel.eval(editStr)

    def __init__(self, name='', node='', asset=None, representations=None):
        self._name = name
        self._node = node

    def create(self):
        self._node = cmds.assembly(name=self._name)
        self._createRepresentations()
