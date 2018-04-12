# base class to wrap all music21 object to my own structure

import music21
import copy

class PianoReductionObject(music21.base.Music21Object):
    def __init__(self, ref):
        super(PianoReductionObject, self).__init__()
        if not isinstance(ref, music21.base.Music21Object):
            raise TypeError('Corrupted Reference')
        self.__dict__ = copy.deepcopy(ref.__dict__)

    def __deepcopy__(self, memo = None):
        return self.__class__(self)

    def __copy__(self, memo = None):
        return super.__copy__(self, memo = memo)

# END: class PianoReductionObject(object)
# ------------------------------------------------------------------------------
