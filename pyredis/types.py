from dataclasses import dataclass


@dataclass
class SimpleString:
    data: str

    def resp_encode(self):
        return f"+{self.data}\r\n".encode()


@dataclass
class Error:
    data: str

    def resp_encode(self):
        return f"-{self.data}\r\n".encode()


@dataclass
class Integer:
    value: int

    def resp_encode(self):
        return f":{self.value}\r\n".encode()


@dataclass
class BulkString:
    data: bytes

    def resp_encode(self):
        if self.data is None:
            return b"$-1\r\n"
        return f"${len(self.data)}\r\n{self.data}\r\n".encode()


@dataclass
class Array:
    data: list

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

    def resp_encode(self):
        if self.data is None:
            return b"*-1\r\n"
        if len(self.data) == 0:
            return b"*0\r\n"
        return (
            b"*"
            + str(len(self.data)).encode()
            + b"\r\n"
            + b"".join([item.resp_encode() for item in self.data])
        )
