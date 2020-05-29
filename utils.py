import os
import binascii
from struct import pack


def _pad_for_encryption(message, target_length):
    max_msglength = target_length - 11
    msglength = len(message)

    if msglength > max_msglength:
        raise OverflowError('%i bytes needed for message, but there is only'
                            ' space for %i' % (msglength, max_msglength))

    # Get random padding
    padding = b''
    padding_length = target_length - msglength - 3

    # We remove 0-bytes, so we'll end up with less padding than we've asked for,
    # so keep adding data until we're at the correct length.
    while len(padding) < padding_length:
        needed_bytes = padding_length - len(padding)

        # Always read at least 8 bytes more than we need, and trim off the rest
        # after removing the 0-bytes. This increases the chance of getting
        # enough bytes, especially when needed_bytes is small
        new_padding = os.urandom(needed_bytes + 5)
        new_padding = new_padding.replace(b'\x00', b'')
        padding = padding + new_padding[:needed_bytes]

    assert len(padding) == padding_length

    return b''.join([b'\x00\x02',
                     padding,
                     b'\x00',
                     message])


def read_random_odd_int(nbits):

    value = read_random_int(nbits)

    # Make sure it's odd
    return value | 1


def read_random_int(nbits):
    randomdata = read_random_bits(nbits)
    value = bytes2int(randomdata)

    # Ensure that the number is large enough to just fill out the required
    # number of bits.
    value |= 1 << (nbits - 1)

    return value


def read_random_bits(nbits):
    nbytes, rbits = divmod(nbits, 8)

    # Get the random bytes
    randomdata = os.urandom(nbytes)

    # Add the remaining random bits
    if rbits > 0:
        randomvalue = ord(os.urandom(1))
        randomvalue >>= (8 - rbits)
        randomdata = byte(randomvalue) + randomdata

    return randomdata


def byte(num):
    return pack("B", num)


def bytes2int(raw_bytes):
    return int(binascii.hexlify(raw_bytes), 16)


def randint(maxvalue):
    b_size = bit_size(maxvalue)

    tries = 0
    while True:
        value = read_random_int(b_size)
        if value <= maxvalue:
            break

        if tries % 10 == 0 and tries:
            # After a lot of tries to get the right number of bits but still
            # smaller than maxvalue, decrease the number of bits by 1. That'll
            # dramatically increase the chances to get a large enough number.
            b_size -= 1
        tries += 1

    return value


def bit_size(num):
    try:
        return num.bit_length()
    except AttributeError:
        raise TypeError('bit_size(num) only supports integers, not %r' % type(num))


def byte_size(number):
    if number == 0:
        return 1
    return ceil_div(bit_size(number), 8)


def ceil_div(num, div):
    quanta, mod = divmod(num, div)
    if mod:
        quanta += 1
    return quanta


def int2bytes(number, fill_size=None, chunk_size=None, overflow=False):
    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)

    if fill_size and chunk_size:
        raise ValueError("You can either fill or pad chunks, but not both")

    # Ensure these are integers.
    number & 1

    raw_bytes = b''

    # Pack the integer one machine word at a time into bytes.
    num = number
    word_bits, _, max_uint, pack_type = get_word_alignment(num)
    pack_format = ">%s" % pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
        num >>= word_bits
    # Obtain the index of the first non-zero byte.
    zero_leading = bytes_leading(raw_bytes)
    if number == 0:
        raw_bytes = b'\x00'
    # De-padding.
    raw_bytes = raw_bytes[zero_leading:]

    length = len(raw_bytes)
    if fill_size and fill_size > 0:
        if not overflow and length > fill_size:
            raise OverflowError(
                    "Need %d bytes for number, but fill size is %d" %
                    (length, fill_size)
            )
        raw_bytes = raw_bytes.rjust(fill_size, b'\x00')
    elif chunk_size and chunk_size > 0:
        remainder = length % chunk_size
        if remainder:
            padding_size = chunk_size - remainder
            raw_bytes = raw_bytes.rjust(length + padding_size, b'\x00')
    return raw_bytes


def get_word_alignment(num, force_arch=64, _machine_word_size=64):
    max_uint64 = 0xffffffffffffffff
    max_uint32 = 0xffffffff
    max_uint16 = 0xffff
    max_uint8 = 0xff

    if force_arch == 64 and _machine_word_size >= 64 and num > max_uint32:
        # 64-bit unsigned integer.
        return 64, 8, max_uint64, "Q"
    elif num > max_uint16:
        # 32-bit unsigned integer
        return 32, 4, max_uint32, "L"
    elif num > max_uint8:
        # 16-bit unsigned integer.
        return 16, 2, max_uint16, "H"
    else:
        # 8-bit unsigned integer.
        return 8, 1, max_uint8, "B"


def bytes_leading(raw_bytes, needle=b'\x00'):
    leading = 0
    # Indexing keeps compatibility between Python 2.x and Python 3.x
    _byte = needle[0]
    for x in raw_bytes:
        if x == _byte:
            leading += 1
        else:
            break
    return leading

