class Shot(object):

    def __init__(self, name='', path=None, sequenceName=''):
        self._name = name
        self._path = path
        self._absPath = None
        self._sequenceName = sequenceName

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def sequenceName(self):
        return self._sequenceName
