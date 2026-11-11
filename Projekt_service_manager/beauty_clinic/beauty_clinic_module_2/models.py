# Доменні моделі (domain models) Beauty Clinic:
# Person -> Client (успадкування), PatientProfile, Service, Product, Appointment.

from exceptions import InvalidPriceError, InvalidStatusError, NotEnoughStockError


def validate_price(price) -> float:
    """Перевіряє ціну: вона має бути числом більше 0. Повертає ціну як float."""
    try:
        price = float(price)
    except (TypeError, ValueError):
        # Наприклад, користувач ввів "abc" замість числа
        raise InvalidPriceError(price)
    if price <= 0:
        raise InvalidPriceError(price)
    return price


class Person:
    """Базовий клас для людини. Від нього успадковується Client."""

    def __init__(self, first_name: str, last_name: str, phone: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def __str__(self) -> str:
        return self.full_name()


class PatientProfile:
    """Картка пацієнта: тип шкіри, алергії, нотатки косметолога."""

    def __init__(self, skin_type: str = "не вказано", allergies: str = "немає"):
        self.skin_type = skin_type
        self.allergies = allergies
        self.notes = []  # список нотаток після процедур

    def add_note(self, text: str) -> None:
        self.notes.append(text)

    def __str__(self) -> str:
        return f"Тип шкіри: {self.skin_type}, алергії: {self.allergies}, нотаток: {len(self.notes)}"


class Client(Person):
    """Клієнт клініки. Успадковує ім'я, телефон, email від Person
    і додає свої поля: id, адресу та картку пацієнта."""

    def __init__(self, client_id: int, first_name: str, last_name: str,
                 phone: str, email: str, date_of_birth: str = "",
                 city: str = "", street: str = "", house_number: str = ""):
        # super() викликає конструктор батьківського класу Person
        super().__init__(first_name, last_name, phone, email)
        self.id = client_id
        self.date_of_birth = date_of_birth
        self.city = city
        self.street = street
        self.house_number = house_number
        # У кожного клієнта є своя картка пацієнта
        self.profile = PatientProfile()

    def address(self) -> str:
        return f"{self.city}, {self.street} {self.house_number}"

    def __str__(self) -> str:
        return f"{self.id} - {self.full_name()} (тел. {self.phone})"


class Service:
    """Послуга (процедура) клініки."""

    def __init__(self, service_id: int, name: str, description: str,
                 price, duration: int = 60):
        self.id = service_id
        self.name = name
        self.description = description
        self.price = validate_price(price)  # може викинути InvalidPriceError
        self.duration = duration  # тривалість у хвилинах

    def __str__(self) -> str:
        return (f"{self.id}. {self.name} — {self.price:.0f} грн ({self.duration} хв)\n"
                f"   {self.description}")


class Product:
    """Препарат або матеріал на складі."""

    def __init__(self, product_id: int, name: str, quantity: int, price):
        self.id = product_id
        self.name = name
        self.quantity = quantity
        self.price = validate_price(price)

    def use(self, amount: int = 1) -> None:
        """Списує препарат зі складу."""
        if amount > self.quantity:
            raise NotEnoughStockError(self.name, self.quantity)
        self.quantity -= amount

    def __str__(self) -> str:
        return f"{self.id}. {self.name} — {self.quantity} шт., {self.price:.0f} грн/шт"


class Appointment:
    """Запис на візит (у термінах роадмапу — Order)."""

    # Дозволені статуси візиту
    STATUSES = ["Заплановано", "Підтверджено", "Виконано", "Скасовано"]

    def __init__(self, appointment_id: int, client: Client, service: Service,
                 date: str, time: str):
        self.id = appointment_id
        self.client = client
        self.service = service
        self.date = date
        self.time = time
        self.status = self.STATUSES[0]  # новий візит завжди "Заплановано"
        self.products_used = []  # список пар (препарат, кількість)
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self) -> float:
        """Ціна послуги + вартість використаних препаратів."""
        total = self.service.price
        for product, amount in self.products_used:
            total += product.price * amount
        return total

    def add_product(self, product: Product, amount: int = 1) -> None:
        """Додає препарат до візиту, списує його зі складу і перераховує ціну."""
        product.use(amount)  # може викинути NotEnoughStockError
        self.products_used.append((product, amount))
        self.total_price = self.calculate_total_price()

    def change_status(self, new_status: str) -> None:
        if new_status not in self.STATUSES:
            raise InvalidStatusError(new_status)
        self.status = new_status

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
