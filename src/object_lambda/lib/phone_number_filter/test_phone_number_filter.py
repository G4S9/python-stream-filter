import unittest

from .phone_number_filter import PhoneNumberFilter, _split_on_last_newline


class TestPhoneNumberFilter(unittest.TestCase):
    def test_initialization(self):
        data = ["sample"]
        pnf = PhoneNumberFilter(data)
        self.assertEqual(list(pnf.it), data)

    def test_filter_method(self):
        data = "\n".join(
            [
                "",  # invalid empty line
                "004912345678910",  # invalid prefix
                "",  # invalid empty line
                "+36 123 456 78",
                "00 36 123 456 78",
                "+35 123456789012",  # invalid, too many digits
                "Hello World!",  # invalid
            ]
        )
        pnf = PhoneNumberFilter([])
        filtered = pnf._filter(data)
        expected = "+36 123 456 78\n00 36 123 456 78\n"
        self.assertEqual(filtered, expected)

    def test_iteration(self):
        data = [b"+36 123 456 78\n0036 123 456 78\nextra", b" line\n+36 123 456 78"]
        pnf = PhoneNumberFilter(data)
        expected = [
            "+36 123 456 78\n0036 123 456 78\n",
            "",
            "+36 123 456 78\n"
        ]
        result = list(pnf)
        self.assertEqual(result, expected)

    def test_split_on_last_newline(self):
        buffer = b"Hello\nWorld\nTest"
        expected = (b"Hello\nWorld\n", b"Test")
        result = _split_on_last_newline(buffer)
        self.assertEqual(result, expected)
