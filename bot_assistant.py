from colorama import Fore, init
from bot_modules import AddressBook, Record
from data_storage import save_data, load_data

init(autoreset=True)


def parse_input(user_input):
    commands = user_input.split()
    if not commands:
        return "", []
    cmd, *args = commands
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            msg = str(e)
            if "unpack" in msg or "not enough values" in msg:
                return f"{Fore.RED}Give me name and phone please"
            return f"{Fore.RED}{msg}"
        except IndexError:
            return f"{Fore.RED}Enter user name"
        except KeyError:
            return f"{Fore.RED}Contact not found"

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = f"{Fore.GREEN} Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"{Fore.GREEN}Contact added"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def update_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"{Fore.GREEN}Phone updated"
    else:
        raise KeyError

@input_error
def get_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{Fore.GREEN}Contact name: {name}, phones: {'; '.join(p.value for p in record.phones)}"
    else:
        raise KeyError

@input_error
def get_all_contacts(book: AddressBook):
    if not book:
        return f"{Fore.YELLOW}Address book is empty"
    return "\n".join(f"{Fore.GREEN}{record}" for record in book.data.values())

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{Fore.GREEN}Birthday added"
    else:
        raise KeyError

@input_error
def show_birthday(args, book:AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
       return f"{Fore.MAGENTA}Contact name: {name}, birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
       raise KeyError

@input_error
def birthdays(book:AddressBook):
    if not book:
        raise KeyError
    birthdays_list = book.get_upcoming_birthdays()
    if not birthdays_list:
        return f"{Fore.YELLOW}No upcoming birthdays"
    return "\n".join(f"{Fore.MAGENTA}Contact name: {birthday['name']}, celebration day: {birthday['congratulation_date']}" for birthday in birthdays_list)

def main():
    book = load_data()
    print(f"{Fore.BLUE}Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Fore.BLUE}Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(update_contact(args, book))
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print(f"{Fore.RED}Invalid command")


if __name__ == "__main__":
    main()