# goit-pycore-hw-06

Homework 6 — an address book built from OOP entities: `Field`, `Name`, `Phone`, `Record`, `AddressBook`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

`-e .` makes the `hw06` package importable, which the tests rely on; `[dev]` pulls in
pytest from the `dev` extra declared in [pyproject.toml](pyproject.toml).

## Project layout

Entities are grouped by concept rather than one file per class, and the tests mirror that structure.

```
src/hw06/
    address_book/
        __init__.py     public re-exports
        fields.py       Field, Name, Phone
        record.py       Record
        book.py         AddressBook
tests/
    address_book/
```

Everything public is re-exported from the package:

```python
from hw06.address_book import AddressBook, Field, Name, Phone, Record
```

---

## `Field`

[src/hw06/address_book/fields.py](src/hw06/address_book/fields.py)

Base class for record fields. Stores a `value` and renders it via `__str__`.

Fields compare by type *and* value, so `Phone("1234567890") != Field("1234567890")`. They are hashable, which is what lets `Record.remove_phone` use `list.remove()`.

## `Name`

Required field. Surrounding whitespace is stripped; an empty, whitespace-only, or non-string name raises `ValueError`.

```python
Name("  John  ").value   # "John"
Name("")                 # ValueError
```

## `Phone`

Validated on construction — exactly 10 digits — so an invalid phone can never exist as an object.

```python
Phone("1234567890").value   # "1234567890"
Phone("123")                # ValueError
Phone("123-456-78")         # ValueError
```

---

## `Record`

[src/hw06/address_book/record.py](src/hw06/address_book/record.py)

Holds one `Name` and a list of `Phone` objects.

```python
record = Record("John")
record.add_phone("1234567890")
record.add_phone("5555555555")

record.find_phone("5555555555")              # Phone("5555555555")
record.edit_phone("1234567890", "1112223333")
record.remove_phone("5555555555")

print(record)   # Contact name: John, phones: 1112223333
```

| method | behaviour |
| --- | --- |
| `add_phone(phone)` | validates, appends, returns the new `Phone`. Rejects duplicates. |
| `find_phone(phone)` | returns the matching `Phone`, or `None` |
| `remove_phone(phone)` | removes and returns it; raises `ValueError` if absent |
| `edit_phone(old, new)` | replaces **in place**, so phone order is preserved |

`edit_phone` builds the replacement before looking up the old number, so an invalid new value raises without mutating the record.

---

## `AddressBook`

[src/hw06/address_book/book.py](src/hw06/address_book/book.py)

A `UserDict` keyed by contact name, so `len()`, `in`, and iteration all work.

```python
book = AddressBook()
book.add_record(record)

book.find("John")      # the Record, or None
book.delete("John")    # the removed Record, or None
```

| method | behaviour |
| --- | --- |
| `add_record(record)` | stores under `record.name.value`; the same name overwrites |
| `find(name)` | returns the `Record`, or `None`. Case-sensitive. |
| `delete(name)` | removes and returns the `Record`, or `None` if absent |

`find` and `delete` return `None` rather than a message string, leaving the wording to the caller.

---

## Usage example

```python
from hw06.address_book import AddressBook, Record

book = AddressBook()

john = Record("John")
john.add_phone("1234567890")
john.add_phone("5555555555")
book.add_record(john)

jane = Record("Jane")
jane.add_phone("9876543210")
book.add_record(jane)

for name, record in book.data.items():
    print(record)
# Contact name: John, phones: 1234567890; 5555555555
# Contact name: Jane, phones: 9876543210

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)
# Contact name: John, phones: 1112223333; 5555555555

print(f"{john.name}: {john.find_phone('5555555555')}")
# John: 5555555555

book.delete("Jane")
```

## Tests

```bash
pytest
```

46 tests covering field validation, every `Record` method, and the `AddressBook` dictionary behaviour.
