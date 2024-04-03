import re


class PhoneNumberFilter:
    def __init__(self, it):
        self.it = iter(it)
        self.regex = r"^\s*(\+|0\s*0)\s*3\s*6\s*(1|[2-9]\s*[0-9])\s*([0-9]\s*){7}$"

    def _filter(self, data):
        filtered_lines = [line for line in data.split('\n') if re.match(self.regex, line)]
        if filtered_lines:
            return '\n'.join(filtered_lines) + '\n'
        return ''

    def __iter__(self):
        tail = b''
        while True:
            try:
                data = next(self.it)
            except StopIteration:
                break
            data = tail + data
            data, tail = _split_on_last_newline(data)
            data = data.decode('utf-8')
            yield self._filter(data)
        if tail:
            yield self._filter(tail.decode('utf-8'))


def _split_on_last_newline(buffer):
    last_newline_index = buffer.rfind(b'\n')

    if last_newline_index != -1:
        return buffer[:last_newline_index + 1], buffer[last_newline_index + 1:]
    else:
        return buffer, b''
