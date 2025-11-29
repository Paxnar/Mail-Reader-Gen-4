import struct

def readlittleendian(data, offset, amount: int = 1):
    rd = {1: '<B', 2: '<H', 4: '<I'}
    byteslist = data[offset:amount + offset]
    return struct.unpack(rd[amount] if amount in rd else '<B', byteslist)[0]


def read8(data, offset=0):
    return readlittleendian(data, offset)


def read16(data, offset=0):
    return readlittleendian(data, offset, 2)


def read32(data, offset=0):
    return readlittleendian(data, offset, 4)
