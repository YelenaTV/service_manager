# збереження і завантаження json + експорт в csv

# csv - для запису таблиці, яку відкриває excel
import csv
# json - для збереження і читання даних
import json
# os - для роботи з шляхами і перевірки чи існує файл
import os

# менеджер, з якого беремо дані і в який завантажуємо
from manager import ServiceManager
# класи, щоб з даних json знову створити об'єкти
from models import Client, Product, Appointment

# папка де лежить програма, щоб файли створювались поруч з нею
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLIENTS_FILE = os.path.join(BASE_DIR, "clients.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")  # щоб склад теж зберігався
CSV_FILE = os.path.join(BASE_DIR, "orders.csv")


# записуємо список у json файл
def write_json(filename: str, data: list) -> None:
    # ensure_ascii=False щоб українські букви нормально записувались
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# читаємо список з json файлу
def read_json(filename: str) -> list:
    # при першому запуску файлу ще немає
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # якщо файл зламаний, просто починаємо з пустими даними
        print(f"Увага: файл {filename} пошкоджений, дані не завантажено.")
        return []


# зберігаємо клієнтів, візити і склад у json файли
def save_data(manager: ServiceManager) -> None:
    write_json(CLIENTS_FILE, [client.to_dict() for client in manager.clients])
    write_json(ORDERS_FILE, [order.to_dict() for order in manager.appointments])
    write_json(PRODUCTS_FILE, [product.to_dict() for product in manager.products])


# завантажуємо дані з json файлів у менеджер
# послуги вже мають бути додані, бо візити шукають їх по id
def load_data(manager: ServiceManager) -> None:

    # склад - якщо файл є, замінюємо початкові препарати
    products_data = read_json(PRODUCTS_FILE)
    if products_data:
        manager.products = []
        for item in products_data:
            product = Product(item["id"], item["name"], item["quantity"], item["price"])
            manager.products.append(product)

    # клієнти
    for item in read_json(CLIENTS_FILE):
        client = Client(item["id"], item["first_name"], item["last_name"],
                        item["phone"], item["email"], item["date_of_birth"],
                        item["city"], item["street"], item["house_number"])
        profile = item.get("profile", {})
        client.profile.skin_type = profile.get("skin_type", "не вказано")
        client.profile.allergies = profile.get("allergies", "немає")
        client.profile.notes = profile.get("notes", [])
        manager.clients.append(client)

    # візити - по id знаходимо клієнта, послугу і препарати
    for item in read_json(ORDERS_FILE):
        client = manager.find_client(item["client_id"])
        service = manager.find_service(item["service_id"])
        order = Appointment(item["id"], client, service, item["date"], item["time"])
        order.status = item["status"]
        for p in item["products"]:
            # use() тут не викликаємо, препарат вже списаний раніше
            order.products_used.append((manager.find_product(p["product_id"]), p["amount"]))
        order.total_price = order.calculate_total_price()
        manager.appointments.append(order)

    # нові id починаємо після найбільшого завантаженого, щоб номери не повторювались
    manager._next_client_id = max([c.id for c in manager.clients], default=0) + 1
    manager._next_appointment_id = max([a.id for a in manager.appointments], default=0) + 1
    manager._next_product_id = max([p.id for p in manager.products], default=0) + 1


# записує всі візити в таблицю, повертає скільки записано
def export_orders_to_csv(manager: ServiceManager, filename: str = CSV_FILE) -> int:
    # utf-8-sig щоб excel нормально показував кирилицю
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Номер", "Клієнт", "Телефон", "Послуга",
                         "Дата", "Час", "Статус", "Препарати", "Сума, грн"])
        for order in manager.appointments:
            # всі препарати в один рядок через кому
            products = ", ".join(f"{p.name} x{amount}" for p, amount in order.products_used)
            writer.writerow([order.id, order.client.full_name(), order.client.phone,
                             order.service.name, order.date, order.time,
                             order.status, products, f"{order.total_price:.0f}"])
    return len(manager.appointments)
