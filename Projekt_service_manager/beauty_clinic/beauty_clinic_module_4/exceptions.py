# свої помилки для програми
# всі наслідуються від ClinicError, тому в меню можна ловити їх одним except


# головний клас помилок, від нього наслідуються всі інші
class ClinicError(Exception):
    pass


class ClientNotFoundError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, client_id):
        super().__init__(f"Клієнта з номером {client_id} не знайдено.")


# коли телефон або email вже є в базі
class DuplicateClientError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self):
        super().__init__("Клієнт з таким номером телефону чи email вже існує.")


class ServiceNotFoundError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, service_id):
        super().__init__(f"Послугу з номером {service_id} не знайдено.")


class AppointmentNotFoundError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, appointment_id):
        super().__init__(f"Візит з номером {appointment_id} не знайдено.")


class ProductNotFoundError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, product_id):
        super().__init__(f"Препарат з номером {product_id} не знайдено.")


# ціна має бути числом більше 0
class InvalidPriceError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, price):
        super().__init__(f"Некоректна ціна: '{price}'. Ціна має бути числом більше 0.")


class InvalidStatusError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, status):
        super().__init__(f"Некоректний статус візиту: '{status}'.")


# неправильний пункт меню
class InvalidMenuChoiceError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, choice):
        super().__init__(f"Некоректний вибір: '{choice}'. Спробуйте ще раз.")


# коли на складі менше препарату ніж треба
class NotEnoughStockError(ClinicError):
    # текст помилки, який побачить користувач
    def __init__(self, product_name, available):
        super().__init__(f"Недостатньо препарату '{product_name}'. На складі: {available} шт.")
