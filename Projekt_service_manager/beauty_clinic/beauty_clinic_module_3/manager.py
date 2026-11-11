# тут вся логіка роботи з даними
# input і print тут немає, вони тільки в main.py

# класи, з яких створюємо клієнтів, послуги, препарати і візити
from models import Client, Service, Product, Appointment
# декоратор, який записує дії в лог
from decorators import log_action
# помилки, коли щось не знайдено або клієнт вже існує
from exceptions import (
    ClientNotFoundError, DuplicateClientError, ServiceNotFoundError,
    AppointmentNotFoundError, ProductNotFoundError,
)


class ServiceManager:

    # при створенні менеджера всі списки пусті
    def __init__(self):
        self.clients = []
        self.services = []
        self.products = []
        self.appointments = []
        # лічильники для id, щоб після видалення номери не повторювались
        self._next_client_id = 1
        self._next_service_id = 1
        self._next_product_id = 1
        self._next_appointment_id = 1

    # ----- клієнти -----

    # чи є вже клієнт з таким телефоном або email
    def client_exists(self, phone: str, email: str) -> bool:
        for client in self.clients:
            if client.phone == phone or client.email == email:
                return True
        return False

    # додаємо нового клієнта
    # details - необов'язкові дані: дата народження, місто, вулиця, будинок
    @log_action
    def add_client(self, first_name: str, last_name: str, phone: str,
                   email: str, **details) -> Client:
        if self.client_exists(phone, email):
            raise DuplicateClientError()
        client = Client(self._next_client_id, first_name, last_name,
                        phone, email, **details)
        self._next_client_id += 1
        self.clients.append(client)
        return client

    # шукаємо клієнта по id, якщо нема - помилка
    def find_client(self, client_id: int) -> Client:
        for client in self.clients:
            if client.id == client_id:
                return client
        raise ClientNotFoundError(client_id)

    # ----- послуги -----

    # додаємо послугу
    def add_service(self, name: str, description: str, price,
                    duration: int = 60) -> Service:
        service = Service(self._next_service_id, name, description, price, duration)
        self._next_service_id += 1
        self.services.append(service)
        return service

    # шукаємо послугу по id
    def find_service(self, service_id: int) -> Service:
        for service in self.services:
            if service.id == service_id:
                return service
        raise ServiceNotFoundError(service_id)

    # ----- склад -----

    # додаємо препарат на склад
    def add_product(self, name: str, quantity: int, price) -> Product:
        product = Product(self._next_product_id, name, quantity, price)
        self._next_product_id += 1
        self.products.append(product)
        return product

    # шукаємо препарат по id
    def find_product(self, product_id: int) -> Product:
        for product in self.products:
            if product.id == product_id:
                return product
        raise ProductNotFoundError(product_id)

    # ----- візити -----

    # створюємо новий візит
    @log_action
    def create_order(self, client_id: int, service_id: int,
                     date: str, time: str) -> Appointment:
        # якщо клієнта або послуги немає - буде помилка
        client = self.find_client(client_id)
        service = self.find_service(service_id)
        appointment = Appointment(self._next_appointment_id, client, service, date, time)
        self._next_appointment_id += 1
        self.appointments.append(appointment)
        return appointment

    # шукаємо візит по id
    def find_order(self, appointment_id: int) -> Appointment:
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        raise AppointmentNotFoundError(appointment_id)

    # змінюємо статус візиту
    @log_action
    def update_status(self, appointment_id: int, new_status: str) -> Appointment:
        appointment = self.find_order(appointment_id)
        appointment.change_status(new_status)
        return appointment

    # додаємо препарат до візиту
    @log_action
    def add_product_to_order(self, appointment_id: int, product_id: int,
                             amount: int = 1) -> Appointment:
        appointment = self.find_order(appointment_id)
        product = self.find_product(product_id)
        appointment.add_product(product, amount)
        return appointment

    # видаляємо візит
    @log_action
    def delete_order(self, appointment_id: int) -> None:
        appointment = self.find_order(appointment_id)
        self.appointments.remove(appointment)

    # повертаємо всі візити
    def list_orders(self) -> list:
        return self.appointments
