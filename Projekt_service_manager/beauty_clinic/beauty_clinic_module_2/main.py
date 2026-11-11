# Точка входу: меню рецепції.
# Тут тільки input()/print(). Уся логіка — у ServiceManager.

from manager import ServiceManager
from models import Appointment
from exceptions import ClinicError, InvalidMenuChoiceError


def load_demo_data(manager: ServiceManager) -> None:
    """Початкові послуги та препарати (у модулі 3 замінимо на JSON)."""
    manager.add_service("Чистка обличчя",
                        "Глибоке очищення шкіри, видалення забруднень і надлишкового себуму.", 800)
    manager.add_service("Масаж обличчя",
                        "Розслаблювальний масаж для покращення тонусу шкіри та кровообігу.", 650, 45)
    manager.add_service("Хімічний пілінг",
                        "Оновлення шкіри, вирівнювання текстури та кольору обличчя.", 1200)
    manager.add_service("Лазерна епіляція",
                        "Довготривале зменшення росту небажаного волосся.", 1500, 90)
    manager.add_service("Мезотерапія",
                        "Введення препаратів для покращення стану та зволоження шкіри.", 1200)
    manager.add_service("Біоревіталізація",
                        "Ін'єкційна процедура для глибокого зволоження та пружності шкіри.", 1800)

    manager.add_product("Гіалуронова кислота (ампула)", 10, 450)
    manager.add_product("Пілінг-розчин", 5, 300)
    manager.add_product("Маска заспокійлива", 20, 120)


def ask_int(prompt: str) -> int:
    """Запитує число. Якщо введено не число — викидає помилку замість падіння програми."""
    value = input(prompt).strip()
    if not value.isdigit():
        raise ClinicError(f"'{value}' — це не число.")
    return int(value)


# ---------- Дії меню ----------

def show_services(manager: ServiceManager) -> None:
    print("\nПОСЛУГИ КЛІНІКИ")
    for service in manager.services:
        print(service)


def register_client(manager: ServiceManager) -> None:
    print("\nРЕЄСТРАЦІЯ КЛІЄНТА")
    last_name = input("Прізвище: ")
    first_name = input("Ім'я: ")
    date_of_birth = input("Дата народження: ")
    city = input("Місто: ")
    street = input("Вулиця: ")
    house_number = input("Номер будинку: ")
    phone = input("Телефон: ")
    email = input("Email: ")

    client = manager.add_client(first_name, last_name, phone, email,
                                date_of_birth=date_of_birth, city=city,
                                street=street, house_number=house_number)
    print(f"Клієнта зареєстровано: {client}")


def show_clients(manager: ServiceManager) -> None:
    if not manager.clients:
        print("Немає зареєстрованих клієнтів.")
        return
    print("\nКЛІЄНТИ КЛІНІКИ")
    for client in manager.clients:
        print(client)


def create_visit(manager: ServiceManager) -> None:
    if not manager.clients:
        print("Спочатку зареєструйте клієнта.")
        return
    print("\nЗАПИС НА ВІЗИТ")
    show_clients(manager)
    client_id = ask_int("Номер клієнта: ")
    manager.find_client(client_id)  # перевіряємо одразу, щоб не питати зайвого

    show_services(manager)
    service_id = ask_int("Номер послуги: ")
    date = input("Дата візиту: ")
    time = input("Час візиту: ")

    appointment = manager.create_order(client_id, service_id, date, time)
    print("Візит створено!")
    print(appointment)


def show_visits(manager: ServiceManager) -> None:
    appointments = manager.list_orders()
    if not appointments:
        print("Немає запланованих візитів.")
        return
    print("\nВІЗИТИ")
    for appointment in appointments:
        print(appointment)
        print("-" * 30)


def change_visit_status(manager: ServiceManager) -> None:
    show_visits(manager)
    if not manager.appointments:
        return
    appointment_id = ask_int("Номер візиту: ")

    # Показуємо статуси з номерами: 1 - Заплановано, 2 - Підтверджено ...
    for number, status in enumerate(Appointment.STATUSES, start=1):
        print(f"{number} - {status}")
    choice = ask_int("Новий статус: ")
    if choice < 1 or choice > len(Appointment.STATUSES):
        raise InvalidMenuChoiceError(choice)

    new_status = Appointment.STATUSES[choice - 1]
    manager.update_status(appointment_id, new_status)
    print(f"Статус змінено на '{new_status}'.")


def add_product_to_visit(manager: ServiceManager) -> None:
    show_visits(manager)
    if not manager.appointments:
        return
    appointment_id = ask_int("Номер візиту: ")
    show_products(manager)
    product_id = ask_int("Номер препарату: ")
    amount = ask_int("Кількість: ")

    appointment = manager.add_product_to_order(appointment_id, product_id, amount)
    print(f"Препарат додано. Нова сума: {appointment.total_price:.0f} грн")


def delete_visit(manager: ServiceManager) -> None:
    show_visits(manager)
    if not manager.appointments:
        return
    appointment_id = ask_int("Номер візиту для видалення: ")
    manager.delete_order(appointment_id)
    print("Візит видалено.")


def show_products(manager: ServiceManager) -> None:
    print("\nСКЛАД ПРЕПАРАТІВ")
    for product in manager.products:
        print(product)


# Словник "пункт меню -> (назва, функція)".
# Замінює довгий ланцюжок if/elif з модуля 1.
MENU = {
    "1": ("Ознайомитися з послугами", show_services),
    "2": ("Зареєструвати клієнта", register_client),
    "3": ("Переглянути клієнтів", show_clients),
    "4": ("Записати клієнта на візит", create_visit),
    "5": ("Переглянути візити", show_visits),
    "6": ("Змінити статус візиту", change_visit_status),
    "7": ("Додати препарат до візиту", add_product_to_visit),
    "8": ("Видалити візит", delete_visit),
    "9": ("Склад препаратів", show_products),
}


def reception(manager: ServiceManager) -> None:
    while True:
        print("\n=== РЕЦЕПЦІЯ BEAUTY CLINIC ===")
        for key, (title, _) in MENU.items():
            print(f"{key} - {title}")
        print("0 - Вийти")

        choice = input("Виберіть дію: ").strip()
        if choice == "0":
            print("До побачення!")
            break

        try:
            if choice not in MENU:
                raise InvalidMenuChoiceError(choice)
            _, action = MENU[choice]
            action(manager)  # викликаємо функцію з меню
        except ClinicError as error:
            # Будь-яка наша помилка: показуємо повідомлення і повертаємось у меню
            print(f"Помилка: {error}")


if __name__ == "__main__":
    clinic = ServiceManager()
    load_demo_data(clinic)
    reception(clinic)
