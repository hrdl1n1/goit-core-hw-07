from classes import AddressBook, Record
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

@input_error
def add_contact(user_input, book: AddressBook):
    """Додає новий контакт або оновлює існуючий."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я та номер телефону, будь ласка.")
    name, phone = args[:2]
    if not phone.isdigit() or len(phone) != 10:
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
def change_contact(user_input, book: AddressBook):
    """Змінює номер телефону контакту."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я та новий номер телефону.")
    name, new_phone = args[:2]
    if not new_phone.isdigit() or len(new_phone) != 10:
        raise ValueError("Недійсний номер телефону. Введіть 10 цифр без роздільників.")
    if book.find(name):
        book.find(name).add_phone(new_phone)
        return "Контакт оновлено."
    else:
        return "Контакт не знайдено."

@input_error
def phone(user_input, book: AddressBook):
    """Повертає номер телефону за ім'ям контакту."""
    name = user_input.split()[1]
    record = book.find(name)
    if record:
        return f"Номер телефону {name}: {', '.join(str(phone) for phone in record.phones)}"
    else:
        return "Контакт не знайдено."

@input_error
def all_contacts(user_input, book: AddressBook):
    """Повертає всі контакти."""
    if book.data:
        return "\n".join([str(record) for record in book.data.values()])
    else:
        return "Немає контактів у книзі."

@input_error
def add_birthday(user_input, book: AddressBook):
    """Додає день народження для контакту."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я контакту та дату народження у форматі DD.MM.YYYY.")
    name, birthday = args[:2]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"День народження додано для {name}."
    else:
        return "Контакт не знайдено."

@input_error
def show_birthday(user_input, book: AddressBook):
    """Показує день народження за ім'ям контакту."""
    name = user_input.split()[1]
    record = book.find(name)
    if record and record.birthday:
        return f"День народження {name}: {record.birthday}"
    else:
        return "День народження не знайдено."

@input_error
def birthdays(user_input, book: AddressBook):
    """Повертає всі наближені дні народження."""
    return book.get_upcoming_birthdays()

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
            result = add_contact(user_input, book)
            print(result)

        elif command == "change":
            result = change_contact(user_input, book)
            print(result)

        elif command == "phone":
            result = phone(user_input, book)
            print(result)

        elif command == "all":
            result = all_contacts(user_input, book)
            print(result)

        elif command == "add-birthday":
            result = add_birthday(user_input, book)
            print(result)

        elif command == "show-birthday":
            result = show_birthday(user_input, book)
            print(result)

        elif command == "birthdays":
            result = birthdays(user_input, book)
            print(result)

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()