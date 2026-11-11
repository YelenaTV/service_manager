# Власні винятки (exceptions) програми Beauty Clinic.
# Усі вони успадковуються від ClinicError, тому в меню
# достатньо одного блоку `except ClinicError`, щоб перехопити будь-яку з них.


class ClinicError(Exception):
    """Базовий клас для всіх помилок клініки."""


class ClientNotFoundError(ClinicError):
    """Клієнта з таким номером не існує."""

    def __init__(self, client_id):
        super().__init__(f"Клієнта з номером {client_id} не знайдено.")


class DuplicateClientError(ClinicError):
    """Клієнт з таким телефоном або email уже зареєстрований."""

    def __init__(self):
        super().__init__("Клієнт з таким номером телефону чи email вже існує.")


class ServiceNotFoundError(ClinicError):
    """Послуги з таким номером не існує."""

    def __init__(self, service_id):
        super().__init__(f"Послугу з номером {service_id} не знайдено.")


class AppointmentNotFoundError(ClinicError):
    """Візиту з таким номером не існує."""

    def __init__(self, appointment_id):
        super().__init__(f"Візит з номером {appointment_id} не знайдено.")


class ProductNotFoundError(ClinicError):
    """Препарату з таким номером немає на складі."""

    def __init__(self, product_id):
        super().__init__(f"Препарат з номером {product_id} не знайдено.")


class InvalidPriceError(ClinicError):
    """Ціна не є додатним числом."""

    def __init__(self, price):
        super().__init__(f"Некоректна ціна: '{price}'. Ціна має бути числом більше 0.")


class InvalidStatusError(ClinicError):
    """Статус візиту не входить до списку дозволених."""

    def __init__(self, status):
        super().__init__(f"Некоректний статус візиту: '{status}'.")


class InvalidMenuChoiceError(ClinicError):
    """Користувач обрав пункт меню, якого не існує."""

    def __init__(self, choice):
        super().__init__(f"Некоректний вибір: '{choice}'. Спробуйте ще раз.")


class NotEnoughStockError(ClinicError):
    """На складі недостатньо препарату."""

    def __init__(self, product_name, available):
        super().__init__(f"Недостатньо препарату '{product_name}'. На складі: {available} шт.")
