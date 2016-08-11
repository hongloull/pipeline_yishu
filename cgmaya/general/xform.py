class Xform(object):

    @staticmethod
    def getXform(transNode):
        """
        return ((rotatePivot, scalePivot, matrix), visibility).

        :Retype: `list((rotatePivot,scalePivot,matrix),vis))`
        """
        xforms = list()
        nodes = Xform._getChildrens()
        for node in nodes:
            xforms.append(((cmds.xform(node, worldSpace=True,
                                       rotatePivot=True, q=True),
                            cmds.xform(node, worldSpace=True,
                                       scalePivot=True, q=True),
                            cmds.xform(node, worldSpace=True,
                                       matrix=True, q=True)),
                           cmds.getAttr('{0}.visibility' .format(node))))
    return xforms

    @staticmethod
    def _getChildrens(transNode):
        nodes = cmds.listRelatives(
            transNode, children=True, fullPath=True, allDescendents=True,
            type='transform')
        if not nodes:
            nodes = list()
        nodes.append(transNode)
        # important:use reverse to get correct matrix
        nodes.reverse()
        return nodes

    @staticmethod
    def setXform(transNode, xforms):
        nodes = Xform._getChildrens(transNode)
        for transNode, matrix in zip(nodes, xforms):
            cmds.xform(transNode, worldSpace=True, rotatePivot=matrix[0][0])
            cmds.xform(transNode, worldSpace=True, scalePivot=matrix[0][1])
            cmds.xform(transNode, worldSpace=True, matrix=matrix[0][2])
            cmds.setAttr('{0}.visibility'.format(transNode), matrix[1])
