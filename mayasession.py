import pprint
from cgpython.utils import Path
from cgpython import io
from cgmaya import mayascene
reload(mayascene)
from cgmaya.entity import asset
reload(asset)
from cgmaya.entity import shot
reload(shot)


def selsToDict(node, inputDict, depth):
    if depth > 1:
        children = cmds.listRelatives(node, fullPath=True,
                                      children=True, type='transform')
        if children:
            inputDict[node] = {}
            for child in children:
                inputDict[node][child] = {}
                selsToDict(child, inputDict[node], depth - 1)


class MayaAssetSession(mayascene.MayaAssetScene):

    def __init__(self, *args, **kwargs):
        """
        """
        super(MayaAssetSession, self).__init__(*args, **kwargs)

    def exportAssemblies(self, depth=2):
        """
        Export assembly definition from selection.
        """
        sels = cmds.ls(sl=True, transforms=True, l=True)
        if len(sels) != 1:
            io.write('Please select one transform node to export assemblies.')
            return

        # save current file and it will be opened again later
        self.save()
        currentScene = self.sceneName

        hierachy = {sels[0]: {}}
        selsToDict(sels[0], hierachy, depth)

        io.write('Export assemblies for selected hierachy:\n')
        pprint.pprint(hierachy)

        try:
            self._flattenDict(hierachy,
                              parentAsset=None,
                              filePath=currentScene)
        except Exception as e:
            import traceback
            traceback.print_exc(e)
            raise

    def _exportSingleAssetAssemlbyDefintionScene(self, assetObj, node=''):
        """
        :Parameters:
            assetObj: `cgmaya.entity.asset.EnvAsset`
            node: `str`
                the node name which will be package.
        """
        assetObj.package(node=node)

    def _createAssemblyDefinitionScene(self, parentAsset, childrenAssets):
        """
        Create assembly definition scene as below:
            1) new a scene, reference children's assembly defintion files,
                save as assembly reference file.
            2) new a scene, create an assembly definition node and add
                "Scene" representation(set "input" to step 1's Maya scene),
                save it as assembly definition file.

        :Parameters:
            parentAsset: `cgmaya.entity.asset.EnvAsset`
            childrenAssets: `list(cgmaya.entity.asset.EnvAsset)`
        """
        # Create assembly refrence scene to referece all sub-assets
        self.new()
        for childAsset in childrenAssets:
            childAsset.referenceAssemblyDefinitionScene()
        self.saveAs(filePath=parentAsset.asrFilePath)

        # Create assembly definition scene
        self.new()
        parentAsset.createAssemblyDefinitionScene()

    def _flattenDict(self, inputDict, parentAsset=None, filePath=''):
        childrenAssets = []
        for k, v in inputDict.items():
            # use short name as asset names
            io.write('k:{0}'.format(k))
            assetName = k.rsplit('|', 1)[-1]
            p = Path(k.replace('|', '/')).dirname()
            if p == '/':
                p = ''
            family = '{0}{1}'.format(self.shortName, p)
            io.write('asset name: {0}'.format(assetName))
            io.write('asset family: {0}'.format(family))
            if v:
                assetObj = asset.AssemblyEnvAsset(name=assetName,
                                                  family=family)
                self._flattenDict(v, assetObj, filePath=filePath)
            else:
                # Package single asset
                assetObj = asset.SingleEnvAsset(name=assetName,
                                                family=family)
                self._exportSingleAssetAssemlbyDefintionScene(assetObj,
                                                              node=k)
                self.open(filePath=filePath)

            childrenAssets.append(assetObj)
        if parentAsset:
            # Create assembly asset definition scene
            self._createAssemblyDefinitionScene(parentAsset,
                                                childrenAssets)
            self.open(filePath=filePath)


class MayaShotSession(mayascene.MayaShotScene):

    def __init__(self, *args, **kwargs):
        """
        """
        super(MayaShotSession, self).__init__(*args, **kwargs)
