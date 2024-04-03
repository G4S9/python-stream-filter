import unittest

from .validator import Validator


class TestLengthWithinRange(unittest.TestCase):

    length_within_range = Validator.length_within_range

    def test_exact_match_max(self):
        self.assertTrue(self.length_within_range("test", min_length=0, max_length=4))

    def test_exact_match_min(self):
        self.assertTrue(self.length_within_range("", min_length=0, max_length=4))

    def test_within_range(self):
        self.assertTrue(self.length_within_range("ok", min_length=0, max_length=4))

    def test_below_min(self):
        self.assertFalse(self.length_within_range("test", min_length=5, max_length=10))

    def test_above_max(self):
        self.assertFalse(self.length_within_range("this is too long", min_length=0, max_length=10))

    def test_empty_string_with_min_length_greater_than_zero(self):
        self.assertFalse(self.length_within_range("", min_length=1, max_length=4))


class TestUuidV4(unittest.TestCase):

    is_uuid_v4 = Validator.is_uuid_v4

    def test_valid_uuid_v4(self):
        valid_uuids = [
            "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "f47ac10b-58cc-4372-a567-0e02b2c3d479".upper(),
        ]
        for uuid in valid_uuids:
            with self.subTest(uuid=uuid):
                self.assertIsNotNone(self.is_uuid_v4(uuid))

    def test_invalid_uuid_v4_version(self):
        invalid_uuids = [
            "f47ac10b-58cc-1372-a567-0e02b2c3d479",
            "f47ac10b-58cc-5372-a567-0e02b2c3d479",
        ]
        for uuid in invalid_uuids:
            with self.subTest(uuid=uuid):
                self.assertIsNone(self.is_uuid_v4(uuid))

    def test_invalid_uuid_v4_variant(self):
        invalid_uuids = [
            "f47ac10b-58cc-4372-2a67-0e02b2c3d479",
            "f47ac10b-58cc-4372-7a67-0e02b2c3d479",
        ]
        for uuid in invalid_uuids:
            with self.subTest(uuid=uuid):
                self.assertIsNone(self.is_uuid_v4(uuid))

    def test_invalid_uuid_v4_format(self):
        invalid_uuids = [
            "g47ac10b-58cc-4372-a567-0e02b2c3d479",
            "f47ac10b58cc-4372-a567-0e02b2c3d479",
            "f47ac10b-58cc4372-a567-0e02b2c3d479",
            "",
            "not-a-uuid",
        ]
        for uuid in invalid_uuids:
            with self.subTest(uuid=uuid):
                self.assertIsNone(self.is_uuid_v4(uuid))


class TestSanitizeFileName(unittest.TestCase):

    sanitize_file_name = Validator.sanitize_file_name

    def test_basic_functionality(self):
        self.assertEqual(self.sanitize_file_name("example?file*name.txt"), "example_file_name.txt")

    def test_leading_and_trailing_spaces(self):
        self.assertEqual(self.sanitize_file_name("  file name.txt  "), "file_name.txt")

    def test_empty_string(self):
        self.assertEqual(self.sanitize_file_name(""), "_")

    def test_only_prohibited_characters(self):
        self.assertEqual(self.sanitize_file_name("?><*|"), "_____")

    def test_file_names_with_path_separators(self):
        self.assertEqual(self.sanitize_file_name("/path/to/file/name.txt"), "_path_to_file_name.txt")

    def test_edge_cases(self):
        self.assertEqual(self.sanitize_file_name("   "), "_")
        self.assertEqual(self.sanitize_file_name("****"), "____")
