from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        # Перевірка правильності формату номеру телефону
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise ValueError("Номер телефону повинен бути рядком з 10 цифрами")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Перевірка правильності формату дати народження
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")

class Record:
    def __init__(self, name):
        # Ім'я контакту
        self.name = Name(name)
        # Список телефонів
        self.phones = []
        # Дата народження
        self.birthday = None

    def add_phone(self, phone):
        # Додавання нового телефонного номера
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видалення телефонного номера
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефонного номера
        if not self.find_phone(old_phone):
            raise ValueError("Номер телефону для редагування не існує")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        # Пошук телефонного номера
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        # Додавання дати народження
        if self.birthday:
            raise ValueError("Дата народження вже існує для цього контакту")
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Представлення запису у зрозумілому форматі
        return f"Ім'я контакту: {str(self.name)}, телефони: {'; '.join(str(p) for p in self.phones)}, дата народження: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        # Додавання нового запису в телефонну книгу
        self.data[record.name.value] = record

    def find(self, name):
        # Пошук запису за ім'ям
        return self.data.get(name)

    def delete(self, name):
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_bdays = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()

                # Визначення дати наступного дня народження
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday = bday.replace(year=today.year + 1)
                else:
                    bday = bday_this_year

                days_until_bday = (bday - today).days

                # Перевірка, чи наступний день народження відбудеться протягом наступного тижня
                if 0 <= days_until_bday <= 7:
                    if bday.weekday() >= 5:
                        days_until_monday = (7 - bday.weekday())
                        bday += timedelta(days_until_monday)

                    upcoming_bdays.append({
                        "name": record.name.value,
                        "congratulation_date": bday.strftime("%Y.%m.%d")
                    })

        return upcoming_bdays

    def __str__(self):
        # Представлення телефонної книги у зрозумілому форматі
        return "\n".join(str(record) for record in self.data.values())