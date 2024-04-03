import os
import re


class Validator:
    UUID_V4_PATTERN = r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$'

    @classmethod
    def length_within_range(cls, string: str, *, max_length: int, min_length: int = 0) -> bool:
        return min_length <= len(string) <= max_length

    @classmethod
    def is_uuid_v4(cls, string: str):
        return re.match(cls.UUID_V4_PATTERN, string, re.IGNORECASE)

    @classmethod
    def sanitize_file_name(cls, file_name: str) -> str:
        sanitized = re.sub(r'[ /?<>\\*|"]', '_', file_name.strip())
        return os.path.basename(sanitized or '_')
