from mtoa.core import createStandIn


class StandIn(object):
    _NODE_TYPE = 'aiStandIn'

    @classmethod
    def export(cls, filePath='', node=''):
        cmds.select(node, r=True)
        io.write('exporting aiStandIn')
        cmds.file(filePath, f=True,
                  options='-mask 248;-lightLinks 0;-boundingBox;-shadowLinks 0',
                  type='ASS Export', pr=True, es=True)

    def __init__(self, **kwargs):
        super(StandIn, self).__init__()
        self._node = ''
        self._transform = ''

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    @property
    def transform(self):
        self._transform = cmds.listRelatives(self.node, parent=True).pop()
        return self._transform

    def importToScene(self, filePath='', name=''):
        """
        Add aiStandIn to Maya scene
        """
        standInNode = createStandIn()
        self.node = standInNode.name()
        cmds.setAttr('{0}.dso'.format(self.node),
                     filePath, type='string')
        # Rename transform node
        cmds.rename(self.transform, 'aiStandIn_{0}'.format(name))
