import numpy as np

class BaseObject:
    def __init__(self,pos,size):
        self._pos = np.array(pos, dtype='float32')