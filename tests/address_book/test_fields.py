import unittest

from hw06.address_book import Field, Name, Phone


class TestField(unittest.TestCase):
    def test_str_returns_the_value(self):
        self.assertEqual(str(Field("abc")), "abc")

    def test_str_converts_non_strings(self):
        self.assertEqual(str(Field(42)), "42")

    def test_equality_requires_the_same_type(self):
        self.assertEqual(Phone("1234567890"), Phone("1234567890"))
        self.assertNotEqual(Phone("1234567890"), Field("1234567890"))

    def test_is_hashable(self):
        self.assertEqual(len({Phone("1234567890"), Phone("1234567890")}), 1)


class TestName(unittest.TestCase):
    def test_stores_the_value(self):
        self.assertEqual(Name("John").value, "John")

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(Name("  John  ").value, "John")

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Name("")

    def test_whitespace_only_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Name("   ")

    def test_non_string_is_rejected(self):
        with self.assertRaises(ValueError):
            Name(None)


class TestPhone(unittest.TestCase):
    def test_accepts_ten_digits(self):
        self.assertEqual(Phone("1234567890").value, "1234567890")

    def test_too_short_is_rejected(self):
        with self.assertRaises(ValueError):
            Phone("123456789")

    def test_too_long_is_rejected(self):
        with self.assertRaises(ValueError):
            Phone("12345678901")

    def test_non_digits_are_rejected(self):
        with self.assertRaises(ValueError):
            Phone("12345abcde")

    def test_formatting_characters_are_rejected(self):
        with self.assertRaises(ValueError):
            Phone("123-456-78")

    def test_empty_is_rejected(self):
        with self.assertRaises(ValueError):
            Phone("")

    def test_non_string_is_rejected(self):
        with self.assertRaises(ValueError):
            Phone(1234567890)

    def test_error_message_mentions_the_value(self):
        with self.assertRaises(ValueError) as context:
            Phone("123")
        self.assertIn("123", str(context.exception))


if __name__ == "__main__":
    unittest.main()
