# ServiceManager — "мозок" програми.
# Зберігає всі дані та містить бізнес-логіку.
# Тут НЕМАЄ input() і print(): менеджер лише працює з даними
# і викидає винятки, а спілкування з користувачем — у main.py.
# Завдяки цьому в модулі 4 його буде легко покрити тестами.

from models import Client, Service, Product, Appointment
from exceptions import (
    ClientNotFoundError, DuplicateClientError, ServiceNotFoundError,
    AppointmentNotFoundError, ProductNotFoundError,
)


class ServiceManager:

    def __init__(self):
        self.clients = []
        self.services = []
        self.products = []
        self.appointments = []
        # Окремі лічильники ID. На відміну від len(list) + 1,
        # вони не дають повторних ID після видалення.
        self._next_client_id = 1
        self._next_service_id = 1
        self._next_product_id = 1
        self._next_appointment_id = 1

    # ---------- Клієнти ----------

    def client_exists(self, phone: str, email: str) -> bool:
        for client in self.clients:
            if client.phone == phone or client.email == email:
                return True
        return False

    def add_client(self, first_name: str, last_name: str, phone: str,
                   email: str, **details) -> Client:
        """details — необов'язкові поля: date_of_birth, city, street, house_number."""
        if self.client_exists(phone, email):
            raise DuplicateClientError()
        client = Client(self._next_client_id, first_name, last_name,
                        phone, email, **details)
        self._next_client_id += 1
        self.clients.append(client)
        return client

    def find_client(self, client_id: int) -> Client:
        for client in self.clients:
            if client.id == client_id:
                return client
        raise ClientNotFoundError(client_id)

    # ---------- Послуги ----------

    def add_service(self, name: str, description: str, price,
                    duration: int = 60) -> Service:
        service = Service(self._next_service_id, name, description, price, duration)
        self._next_service_id += 1
        self.services.append(service)
        return service

    def find_service(self, service_id: int) -> Service:
        for service in self.services:
            if service.id == service_id:
                return service
        raise ServiceNotFoundError(service_id)

    # ---------- Склад ----------

    def add_product(self, name: str, quantity: int, price) -> Product:
        product = Product(self._next_product_id, name, quantity, price)
        self._next_product_id += 1
        self.products.append(product)
        return product

    def find_product(self, product_id: int) -> Product:
        for product in self.products:
            if product.id == product_id:
                return product
        raise ProductNotFoundError(product_id)

    # ---------- Візити (orders) ----------

    def create_order(self, client_id: int, service_id: int,
                     date: str, time: str) -> Appointment:
        client = self.find_client(client_id)      # може викинути ClientNotFoundError
        service = self.find_service(service_id)   # може викинути ServiceNotFoundError
        appointment = Appointment(self._next_appointment_id, client, service, date, time)
        self._next_appointment_id += 1
        self.appointments.append(appointment)
        return appointment

    def find_order(self, appointment_id: int) -> Appointment:
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        raise AppointmentNotFoundError(appointment_id)

    def update_status(self, appointment_id: int, new_status: str) -> Appointment:
        appointment = self.find_order(appointment_id)
        appointment.change_status(new_status)  # може викинути InvalidStatusError
        return appointment

    def add_product_to_order(self, appointment_id: int, product_id: int,
                             amount: int = 1) -> Appointment:
        appointment = self.find_order(appointment_id)
        product = self.find_product(product_id)
        appointment.add_product(product, amount)
        return appointment

    def delete_order(self, appointment_id: int) -> None:
        appointment = self.find_order(appointment_id)
        self.appointments.remove(appointment)

    def list_orders(self) -> list:
        return self.appointments
