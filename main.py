from classes import AddressBook, Record
import re
from datetime import datetime

def input_error(func):
    """Декоратор, який обробляє помилки введення для функцій."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Недійсна кількість аргументів для цієї команди."
    return inner

def parse_input(user_input):
    """Розбирає введену користувачем команду на команду та аргументи."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def validate_date(date_text):
    """Перевіряє, чи відповідає дата вказаному формату DD.MM.YYYY."""
    try:
        datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def validate_phone(phone_number):
    """Перевіряє, чи відповідає номер телефону вказаному формату 10 цифр."""
    return bool(re.match(r'^\d{10}$', phone_number))

@input_error
def add_contact(args, book: AddressBook):
    """Додає новий контакт або оновлює існуючий."""
    if len(args) < 2:
        raise ValueError("Введіть ім'я та номер телефону, будь ласка.")
    name, phone = args[:2]
    if not validate_phone(phone):
        raise ValueError("Недійсний номер телефону. Введіть 10 цифр без роздільників.")
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    """Змінює номер телефону контакту."""
    if len(args) < 2:
        raise ValueError("Введіть ім'я та новий номер телефону.")
    name, new_phone = args[:2]
    if not validate_phone(new_phone):
        raise ValueError("Недійсний номер телефону. Введіть 10 цифр без роздільників.")
    if book.contact_exists(name):
        book.change_contact(name, new_phone)
        return "Контакт оновлено."
    else:
        return "Контакт не знайдено."

@input_error
def phone(args, book: AddressBook):
    """Повертає номер телефону за ім'ям контакту."""
    if len(args) < 1:
        raise ValueError("Введіть ім'я контакту.")
    name = args[0]
    phone = book.get_phone(name)
    if phone:
        return f"Номер телефону {name}: {phone}"
    else:
        return "Контакт не знайдено."

@input_error
def all_contacts(args, book: AddressBook):
    """Повертає всі контакти."""
    contacts = book.get_all_contacts()
    if contacts:
        return "\n".join([f"{contact.name}: {', '.join(contact.phones)}" for contact in contacts])
    else:
        return "Немає контактів у книзі."

@input_error
def add_birthday(args, book: AddressBook):
    """Додає день народження для контакту."""
    if len(args) < 2:
        raise ValueError("Введіть ім'я контакту та дату народження у форматі DD.MM.YYYY.")
    name, birthday = args[:2]
    if not validate_date(birthday):
        raise ValueError("Неправильний формат дати. Введіть у форматі DD.MM.YYYY.")
    book.add_birthday(name, birthday)
    return f"День народження додано для {name}."

@input_error
def show_birthday(args, book: AddressBook):
    """Показує день народження за ім'ям контакту."""
    if len(args) < 1:
        raise ValueError("Введіть ім'я контакту.")
    name = args[0]
    birthday = book.get_birthday(name)
    if birthday:
        return f"День народження {name}: {birthday}"
    else:
        return "День народження не знайдено."

@input_error
def birthdays(args, book: AddressBook):
    """Повертає всі наближені дні народження."""
    return book.upcoming_birthdays()

def main():
    """Основна функція програми."""
    book = AddressBook()
    print("Ласкаво просимо до помічника!")
    print("Доступні команди: add, change, phone, all, add-birthday, show-birthday, birthdays, hello, close або exit")
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу допомогти?")

        elif command == "add":
            result = add_contact(args, book)
            print(result)

        elif command == "change":
            result = change_contact(args, book)
            print(result)

        elif command == "phone":
            result = phone(args, book)
            print(result)

        elif command == "all":
            result = all_contacts(args, book)
            print(result)

        elif command == "add-birthday":
            result = add_birthday(args, book)
            print(result)

        elif command == "show-birthday":
            result = show_birthday(args, book)
            print(result)

        elif command == "birthdays":
            result = birthdays(args, book)
            print(result)

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()