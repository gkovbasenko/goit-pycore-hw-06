import unittest

from hw06.address_book import Name, Phone, Record


class TestRecordCreation(unittest.TestCase):
    def test_name_is_stored_as_a_name_object(self):
        record = Record("John")
        self.assertIsInstance(record.name, Name)
        self.assertEqual(record.name.value, "John")

    def test_phones_start_empty(self):
        self.assertEqual(Record("John").phones, [])

    def test_invalid_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Record("")


class TestAddPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")

    def test_stores_phone_objects(self):
        self.record.add_phone("1234567890")
        self.assertIsInstance(self.record.phones[0], Phone)
        self.assertEqual(self.record.phones[0].value, "1234567890")

    def test_keeps_insertion_order(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")
        self.assertEqual(
            [p.value for p in self.record.phones], ["1234567890", "5555555555"]
        )

    def test_invalid_phone_is_rejected(self):
        with self.assertRaises(ValueError):
            self.record.add_phone("123")
        self.assertEqual(self.record.phones, [])

    def test_duplicate_phone_is_rejected(self):
        self.record.add_phone("1234567890")
        with self.assertRaises(ValueError):
            self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)


class TestFindPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")

    def test_returns_the_matching_phone(self):
        found = self.record.find_phone("5555555555")
        self.assertIsInstance(found, Phone)
        self.assertEqual(found.value, "5555555555")

    def test_unknown_phone_returns_none(self):
        self.assertIsNone(self.record.find_phone("0000000000"))


class TestRemovePhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")

    def test_removes_the_phone(self):
        self.record.remove_phone("1234567890")
        self.assertEqual([p.value for p in self.record.phones], ["5555555555"])

    def test_unknown_phone_raises(self):
        with self.assertRaises(ValueError):
            self.record.remove_phone("0000000000")
        self.assertEqual(len(self.record.phones), 2)


class TestEditPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")

    def test_replaces_the_phone(self):
        self.record.edit_phone("1234567890", "1112223333")
        self.assertIsNone(self.record.find_phone("1234567890"))
        self.assertIsNotNone(self.record.find_phone("1112223333"))

    def test_preserves_position(self):
        self.record.edit_phone("1234567890", "1112223333")
        self.assertEqual(
            [p.value for p in self.record.phones], ["1112223333", "5555555555"]
        )

    def test_unknown_phone_raises(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("0000000000", "1112223333")

    def test_invalid_replacement_is_rejected_without_changing_anything(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("1234567890", "123")
        self.assertEqual(
            [p.value for p in self.record.phones], ["1234567890", "5555555555"]
        )


class TestRecordStr(unittest.TestCase):
    def test_matches_the_expected_format(self):
        record = Record("John")
        record.add_phone("1112223333")
        record.add_phone("5555555555")
        self.assertEqual(
            str(record), "Contact name: John, phones: 1112223333; 5555555555"
        )

    def test_record_without_phones(self):
        self.assertEqual(str(Record("John")), "Contact name: John, phones: ")


if __name__ == "__main__":
    unittest.main()
