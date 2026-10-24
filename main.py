from collections import UserDict
import re

# Base Field class for record fields 
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Name field class for contact names
class Name(Field):
    pass

# Phone field class for contact phone numbers
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)


# Record class for contact information, including name and phone numbers
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Add a phone number to the record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove a phone number from the record
    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    # Edit an existing phone number in the record
    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if found_phone is None:
            raise ValueError("Phone number not found.")

        new_phone = Phone(new_phone)
        found_phone.value = new_phone.value

    # Find a phone number in the record
    # Returns the Phone object if found, otherwise None
    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# AddressBook class for managing multiple contact records
class AddressBook(UserDict):

    # Add a new contact record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a contact record by name
    def find(self, name):
        return self.data.get(name)

    # Delete a contact record by name
    def delete(self, name):
        if name in self.data:
            del self.data[name]


# Example usage:
def main():
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")



if __name__ == "__main__":
    main()
