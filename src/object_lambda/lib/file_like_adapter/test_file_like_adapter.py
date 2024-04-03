import unittest

from .file_like_adapter import FileLikeAdapter


class TestFileLikeAdapter(unittest.TestCase):

    def test_basic_reading(self):
        adapter = FileLikeAdapter("hello")
        self.assertEqual(adapter.read(2), "he")

    def test_reading_across_multiple_chunks(self):
        adapter = FileLikeAdapter("hello")
        adapter.read(2)
        self.assertEqual(adapter.read(2), "ll")

    def test_exact_chunk_size_reading(self):
        adapter = FileLikeAdapter("hello")
        self.assertEqual(adapter.read(5), "hello")

    def test_reading_beyond_end(self):
        adapter = FileLikeAdapter("hi")
        self.assertEqual(adapter.read(10), "hi")

    def test_empty_iterable(self):
        adapter = FileLikeAdapter("")
        self.assertIsNone(adapter.read(1))

    def test_repeated_reads_after_exhaustion(self):
        adapter = FileLikeAdapter("test")
        adapter.read(4)
        self.assertIsNone(adapter.read(1))

    def test_multiple_types_in_iterable(self):
        adapter = FileLikeAdapter(['a', 'b', 'c', 123])
        self.assertRaises(TypeError, lambda: adapter.read(4))

    def test_zero_or_negative_read(self):
        adapter = FileLikeAdapter("hello")
        self.assertEqual(adapter.read(0), '')
        self.assertRaises(ValueError, lambda: adapter.read(-1))
