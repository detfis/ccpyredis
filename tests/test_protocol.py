import pytest
from protocol import SimpleString, extract_frame_from_buffer


@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n:extra data\r\n", (SimpleString("OK"), 5)),
])
def test_read_frame_simple_string(buffer, expected):
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == expected[0]
    assert frame_size == expected[1]
