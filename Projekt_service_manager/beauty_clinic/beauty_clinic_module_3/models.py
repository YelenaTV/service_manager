# класи для клієнтів, послуг, препаратів і візитів

# помилки: неправильна ціна, неправильний статус, мало препарату на складі
from exceptions import InvalidPriceError, InvalidStatusError, NotEnoughStockError


# перевіряємо, що ціна - це число більше 0, і повертаємо її як дробове число
def validate_price(price) -> float:
    try:
        price = float(price)
    except (TypeError, ValueError):
        # якщо ввели не число, наприклад "abc"
        raise InvalidPriceError(price)
    if price <= 0:
        raise InvalidPriceError(price)
    return price


# загальний клас для людини, від нього наслідується Client
class Person:
    # основні дані людини
    def __init__(self, first_name: str, last_name: str, phone: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    # прізвище + ім'я
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    # що виводиться, коли робимо print() цього об'єкта
    def __str__(self) -> str:
        return self.full_name()


# картка пацієнта
class PatientProfile:
    # тип шкіри і алергії, якщо не вказали - буде "не вказано" і "немає"
    def __init__(self, skin_type: str = "не вказано", allergies: str = "немає"):
        self.skin_type = skin_type
        self.allergies = allergies
        self.notes = []  # нотатки косметолога після процедур

    # додати нотатку в картку
    def add_note(self, text: str) -> None:
        self.notes.append(text)

    # перетворюємо в словник, щоб записати в json
    def to_dict(self) -> dict:
        return {
            "skin_type": self.skin_type,
            "allergies": self.allergies,
            "notes": self.notes,
        }

    # що виводиться, коли робимо print() цього об'єкта
    def __str__(self) -> str:
        return f"Тип шкіри: {self.skin_type}, алергії: {self.allergies}, нотаток: {len(self.notes)}"


# клієнт клініки, ім'я телефон і email беремо з Person
class Client(Person):
    # дані клієнта + адреса
    def __init__(self, client_id: int, first_name: str, last_name: str,
                 phone: str, email: str, date_of_birth: str = "",
                 city: str = "", street: str = "", house_number: str = ""):
        # викликаємо конструктор Person
        super().__init__(first_name, last_name, phone, email)
        self.id = client_id
        self.date_of_birth = date_of_birth
        self.city = city
        self.street = street
        self.house_number = house_number
        # у кожного клієнта своя картка
        self.profile = PatientProfile()

    # адреса одним рядком
    def address(self) -> str:
        return f"{self.city}, {self.street} {self.house_number}"

    # перетворюємо в словник, щоб записати в json
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            "profile": self.profile.to_dict(),
        }

    # як показувати клієнта в списку
    def __str__(self) -> str:
        return f"{self.id} - {self.full_name()} (тел. {self.phone})"


# послуга клініки
class Service:
    # дані послуги, ціна перевіряється
    def __init__(self, service_id: int, name: str, description: str,
                 price, duration: int = 60):
        self.id = service_id
        self.name = name
        self.description = description
        self.price = validate_price(price)
        self.duration = duration  # в хвилинах

    # як показувати послугу в списку
    def __str__(self) -> str:
        return (f"{self.id}. {self.name} — {self.price:.0f} грн ({self.duration} хв)\n"
                f"   {self.description}")


# препарат на складі
class Product:
    # дані препарату
    def __init__(self, product_id: int, name: str, quantity: int, price):
        self.id = product_id
        self.name = name
        self.quantity = quantity  # скільки залишилось на складі
        self.price = validate_price(price)

    # списуємо препарат зі складу
    def use(self, amount: int = 1) -> None:
        if amount > self.quantity:
            raise NotEnoughStockError(self.name, self.quantity)
        self.quantity -= amount

    # перетворюємо в словник, щоб записати в json
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
        }

    # як показувати препарат на складі
    def __str__(self) -> str:
        return f"{self.id}. {self.name} — {self.quantity} шт., {self.price:.0f} грн/шт"


# візит клієнта (це і є order з завдання)
class Appointment:
    STATUSES = ["Заплановано", "Підтверджено", "Виконано", "Скасовано"]

    # створюємо візит з усіма даними
    def __init__(self, appointment_id: int, client: Client, service: Service,
                 date: str, time: str):
        self.id = appointment_id
        self.client = client
        self.service = service
        self.date = date
        self.time = time
        self.status = self.STATUSES[0]  # новий візит завжди "Заплановано"
        self.products_used = []  # пари (препарат, кількість)
        self.total_price = self.calculate_total_price()

    # ціна послуги + препарати
    def calculate_total_price(self) -> float:
        total = self.service.price
        for product, amount in self.products_used:
            total += product.price * amount
        return total

    # додаємо препарат до візиту і перераховуємо суму
    def add_product(self, product: Product, amount: int = 1) -> None:
        product.use(amount)  # спочатку списуємо зі складу
        self.products_used.append((product, amount))
        self.total_price = self.calculate_total_price()

    # змінюємо статус, тільки якщо він є в списку
    def change_status(self, new_status: str) -> None:
        if new_status not in self.STATUSES:
            raise InvalidStatusError(new_status)
        self.status = new_status

    # в json пишемо тільки id клієнта і послуги, а не весь об'єкт
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client_id": self.client.id,
            "service_id": self.service.id,
            "date": self.date,
            "time": self.time,
            "status": self.status,
            "products": [{"product_id": product.id, "amount": amount}
                         for product, amount in self.products_used],
            "total_price": self.total_price,
        }

    # що виводиться, коли робимо print() цього об'єкта
    def __str__(self) -> str:
        text = (f"Візит №{self.id}\n"
                f"  Клієнт: {self.client.full_name()}\n"
                f"  Послуга: {self.service.name}\n"
                f"  Дата: {self.date} о {self.time}\n"
                f"  Статус: {self.status}\n")
        for product, amount in self.products_used:
            text += f"  Препарат: {product.name} x{amount}\n"
        text += f"  До сплати: {self.total_price:.0f} грн"
        return text
