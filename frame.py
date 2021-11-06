import struct
from abc import ABC
from random import seed
from random import randint
class Frame(ABC):
    # Frame INIT sequence / 2 bytes /
    DEFAULT_FRAME_INIT_SEQ = 0x7F

    # Frame END sequence / 1 byte /
    DEFAULT_FRAME_END_SEQ = b'\x7F'

    def __init__(self, type: bytes):
        self._FrameInitSeq = self.DEFAULT_FRAME_INIT_SEQ
        self._FrameEndSeq = self.DEFAULT_FRAME_END_SEQ
        assert len(type) == 1, 'The Frame TYPE must be 01 byte'
        self._FrameType = type

    def __repr__(self):
        return str(self.__dict__)

class ID_Dat(Frame):
    '''
    Trame envoyée par l'arbitre de bus pour indiqué l'objet à transmettre
    '''
    TYPE = b'\x01'

    def __init__(self, id: int, *args, **kwargs):
        super().__init__(self.TYPE, *args, **kwargs)
        self._id = id

    @property
    def id(self):
        return self._id

    def get_repr(self):
        fmt = f'hchc'
        vals = (self._FrameInitSeq, self._FrameType, self._id, self._FrameEndSeq)
        return struct.pack(fmt, *vals)

    @classmethod
    def from_repr(cls, repr: bytes):
        fmt = f'hchc'
        _, type, id, _ = struct.unpack(fmt, repr)
        assert type == cls.TYPE, f'Bad frame type, expected {cls.TYPE}, got {type}'
        return cls(id)

    @classmethod
    def size(cls):
        '''The ID_Dat frame is represented with 7 bytes'''
        return 7


class RP_Dat(Frame):
    '''
    Trame envoyée par les producteur en réponse à une trame ID_Dat
    '''
    TYPE = b'\x8F'

    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(self.TYPE, *args, **kwargs)
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: bytes):
        '''
        Contenu de la trame (128 bytes max)
        '''
        assert len(data) <= 128, 'RP_Dat frame data must be <= 128 bytes'
        self._data = data

    def get_repr(self):
        fmt = f'hc{len(self._data)}sc'
        vals = (self._FrameInitSeq, self._FrameType, self.data, self._FrameEndSeq)
        return struct.pack(fmt, *vals)

    @classmethod
    def from_repr(cls, repr: bytes):
        fmt = f'hc{0}sc'
        size = len(repr) - struct.calcsize(fmt)
        fmt = f'hc{size}sc'
        _, type, data, _ = struct.unpack(fmt, repr)
        assert type == cls.TYPE, 'Bad frame type'
        return cls(data)



    @classmethod
    def size(cls):
        '''The RP_Dat frame is represented with 5 + `n` bytes where `1 <= n <= 128`'''
        return 6 + 128


if __name__ == '__main__':
    # f = Frame(0xD0A12FF7EFFC)
    value = 0x0001
    frame_01 = ID_Dat(value)
    print(frame_01)
    reps = frame_01.get_repr()
    frame_02 = type(frame_01).from_repr(reps)
    print(frame_02)

    print('===============')

    value = 0xD0A12FF7EFFC
    frame_01 = RP_Dat(b'{value}')
    print(frame_01)
    reps = frame_01.get_repr()
    frame_02 = type(frame_01).from_repr(reps)
    print(frame_02)
