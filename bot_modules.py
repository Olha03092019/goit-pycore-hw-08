from collections import UserDict
from datetime import datetime,timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
     if len(value) != 10 or not value.isdigit():
         raise ValueError("Phone number must be 10 digits")
     super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        for phone_number in self.phones:
         if phone_number.value == phone:
            self.phones.remove(phone_number)
            return True
        return False

    def edit_phone(self, phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             phone_number.value = Phone(new_phone).value
             return True
        return False

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             return phone_number
        return None

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
         del self.data[name]
         return True
        return False

    def get_upcoming_birthdays(self):
        current_day = datetime.today().date()
        birthdays_list = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=current_day.year)

                # Check if the birthday has passed, if so, postpone it to next year
                if birthday_this_year < current_day:
                   birthday_this_year = birthday_this_year.replace(year=current_day.year + 1)

                days_till_birthday = (birthday_this_year - current_day).days

                # Check if birthday is in the next 7 days
                if 0 <= days_till_birthday <= 7:
                     celebration_date = birthday_this_year

                     # Check if celebration_date is on a weekend
                     if celebration_date.weekday() == 5:  # субота
                        celebration_date += timedelta(days=2)
                     elif celebration_date.weekday() == 6:  # неділя
                        celebration_date += timedelta(days=1)

                     birthdays_list.append({
                              "name": record.name.value,
                              "congratulation_date": celebration_date.strftime("%d.%m.%Y")
                     })

        return birthdays_list

if __name__ == "__main__":
        # Створення книги
        book = AddressBook()

        # Додавання контактів
        john = Record("John")
        john.add_phone("1234567890")
        john.add_birthday("04.11.1988")
        book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("0987654321")
        jane.add_birthday("05.11.2000")
        book.add_record(jane)

        # Виведення
        for record in book.data.values():
            print(record)

        print("Дні народження наступного тижня:")
        for user in book.get_upcoming_birthdays():
            print(user)