import os
from cgpython.utils.singleton import Singleton
from cgpython.utils import Path


class Workspace(Singleton):

    def __init__(self):
        pass

    @property
    def rootDir(self):
        return Path(cmds.workspace(q=True, rd=True))
