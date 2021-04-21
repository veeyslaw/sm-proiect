from math import ceil


class Field:
    def __init__(self, size: int):
        self.bitsize = size
        self.value = None


class Command:
    ENDIANNESS = "big"
    MOVE = 0x0
    RCLICK = 0x1
    LCLICK = 0x2

    def __init__(self, command: int = 0, x: int = 0, y: int = 0):
        self._command = Field(4)
        self._x = Field(14)
        self._y = Field(14)

        self._command.value = command
        self._x.value = x
        self._y.value = y

    @property
    def x(self):
        return self._x.value

    @property
    def y(self):
        return self._y.value

    @property
    def command(self):
        return self._command.value

    def __str__(self) -> str:
        return "\n".join([f"{name[1:]}: {v.value}" for name, v in vars(self).items()])

    def __len__(self) -> int:
        # length in bytes
        return int(ceil(sum([v.bitsize for v in vars(self).values()]) / 8))

    def to_bytes(self) -> bytes:
        res = 0x0
        fields = [(v.value, v.bitsize) for v in vars(self).values()]
        for value, bitsize in fields:
            mask = (0x1 << bitsize) - 1
            res = (res << bitsize) | (mask & value)
        return res.to_bytes(len(self), Command.ENDIANNESS)

    @classmethod
    def from_bytes(cls, msg_bytes: bytes) -> 'Command':
        res = cls()
        msg_int = int.from_bytes(msg_bytes, Command.ENDIANNESS)
        fields = [(name, v.bitsize) for name, v in vars(res).items()]
        for name, bitsize in fields[::-1]:
            mask = (0x1 << bitsize) - 1
            value = msg_int & mask
            res.__dict__[name].value = value
            msg_int >>= bitsize
        return res
