from ._path import Path as NativePath
from ._path import multimethod


class Path(NativePath):

    def __init__(self, *args, **kwargs):
        super(Path, self).__init__(*args, **kwargs)

    @multimethod
    def joinpath(cls, first, *others):
        """
        Join first to zero or more :class:`Path` components, adding a separator
        character (:samp:`{first}.module.sep`) if needed.  Returns a new instance of
        :samp:`{first}._next_class`.

        .. seealso:: :func:`os.path.join`
        """
        if not isinstance(first, cls):
            first = cls(first)
        return first._next_class(first.module.join(first, *others).replace('\\', '/'))

    def __div__(self, rel):
        """ fp.__div__(rel) == fp / rel == fp.joinpath(rel)

        Join two path components, adding a separator character if
        needed.

        .. seealso:: :func:`os.path.join`
        """
        return self._next_class(self.module.join(self, rel).replace('\\', '/'))
