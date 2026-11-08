import unittest
from collections import UserDict

from hw06.address_book import AddressBook, Record


class AddressBookTestCase(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.john = Record("John")
        self.john.add_phone("1234567890")
        self.book.add_record(self.john)


class TestAddRecord(AddressBookTestCase):
    def test_is_a_userdict(self):
        self.assertIsInstance(self.book, UserDict)

    def test_stores_the_record_under_its_name(self):
        self.assertIs(self.book.data["John"], self.john)

    def test_supports_len_and_membership(self):
        self.assertEqual(len(self.book), 1)
        self.assertIn("John", self.book)

    def test_same_name_overwrites(self):
        replacement = Record("John")
        replacement.add_phone("9999999999")
        self.book.add_record(replacement)
        self.assertEqual(len(self.book), 1)
        self.assertIs(self.book.find("John"), replacement)


class TestFind(AddressBookTestCase):
    def test_returns_the_record(self):
        self.assertIs(self.book.find("John"), self.john)

    def test_unknown_name_returns_none(self):
        self.assertIsNone(self.book.find("Nobody"))

    def test_lookup_is_case_sensitive(self):
        self.assertIsNone(self.book.find("john"))


class TestDelete(AddressBookTestCase):
    def test_removes_the_record(self):
        self.book.delete("John")
        self.assertEqual(len(self.book), 0)
        self.assertIsNone(self.book.find("John"))

    def test_returns_the_removed_record(self):
        self.assertIs(self.book.delete("John"), self.john)

    def test_unknown_name_returns_none(self):
        self.assertIsNone(self.book.delete("Nobody"))
        self.assertEqual(len(self.book), 1)


class TestAddressBookStr(unittest.TestCase):
    def test_empty_book(self):
        self.assertEqual(str(AddressBook()), "Address book is empty.")

    def test_lists_every_record(self):
        book = AddressBook()
        jane = Record("Jane")
        jane.add_phone("9876543210")
        book.add_record(jane)
        self.assertEqual(str(book), "Contact name: Jane, phones: 9876543210")


if __name__ == "__main__":
    unittest.main()
