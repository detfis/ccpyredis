from pyredis.types import Array, Error, SimpleString, Integer, BulkString


_MSG_SEPARATOR = b"\r\n"
_MSG_SEPARATOR_LENGTH = len(_MSG_SEPARATOR)


def extract_frame_from_buffer(buffer):
    separator = buffer.find(_MSG_SEPARATOR)
    _MSG_SEPARATOR_LENGTH = len(_MSG_SEPARATOR)

    if separator == -1:
        return None, 0

    payload = buffer[1:separator].decode("utf-8")

    match chr(buffer[0]):
        case "+":
            return SimpleString(payload), separator + 2
        case "-":
            return Error(payload), separator + 2
        case ":":
            return Integer(int(payload)), separator + 2
        case "$":
            length = int(payload)

            if length == -1:
                return BulkString(None), len(buffer.decode("utf-8"))

            second_separator = buffer.find(_MSG_SEPARATOR, separator + 2)
            if second_separator == -1:
                return None, 0

            value = buffer[
                separator + _MSG_SEPARATOR_LENGTH : separator
                + _MSG_SEPARATOR_LENGTH
                + length
            ]
            return BulkString(value), separator + 2 * _MSG_SEPARATOR_LENGTH + length
        case "*":
            length = int(payload)

            if length == -1:
                return Array(None), len(buffer.decode("utf-8"))
            if length == 0:
                return Array([]), len(buffer.decode("utf-8"))

            array = []

            for _ in range(length):
                next_item, next_item_size = extract_frame_from_buffer(
                    buffer[separator + _MSG_SEPARATOR_LENGTH :]
                )
                if next_item and next_item_size:
                    array.append(next_item)
                    separator += next_item_size
                else:
                    return None, 0
            return Array(array), separator + _MSG_SEPARATOR_LENGTH
    return None, 0


def encode_message(message):
    return message.resp_encode()
