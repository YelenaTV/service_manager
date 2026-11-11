# тести для створення, видалення, зміни статусу і ціни візиту

# pytest - щоб перевіряти помилки через pytest.raises
import pytest

# помилки, які мають з'являтись коли щось не так
from exceptions import ClientNotFoundError, AppointmentNotFoundError, InvalidStatusError


# ----- create_order -----

# перевіряємо що візит створюється з правильними даними
def test_create_order(manager):
    order = manager.create_order(1, 2, "10.11.2026", "12:00")
    assert order.client.last_name == "Коваль"
    assert order.service.name == "Хімічний пілінг"
    assert len(manager.list_orders()) == 1


# новий візит має статус "Заплановано"
def test_new_order_status(manager):
    order = manager.create_order(1, 1, "10.11.2026", "12:00")
    assert order.status == "Заплановано"


# клієнта з номером 99 немає, тому має бути помилка
def test_create_order_client_not_found(manager):
    with pytest.raises(ClientNotFoundError):
        manager.create_order(99, 1, "10.11.2026", "12:00")


# ----- delete_order -----

# після видалення список візитів пустий
def test_delete_order(manager):
    order = manager.create_order(1, 1, "10.11.2026", "12:00")
    manager.delete_order(order.id)
    assert len(manager.list_orders()) == 0


# видаляємо візит якого немає - помилка
def test_delete_order_not_found(manager):
    with pytest.raises(AppointmentNotFoundError):
        manager.delete_order(5)


# ----- update_status -----

# міняємо статус на "Підтверджено"
def test_update_status(manager):
    order = manager.create_order(1, 1, "10.11.2026", "12:00")
    manager.update_status(order.id, "Підтверджено")
    assert order.status == "Підтверджено"


# такого статусу немає в списку - помилка
def test_update_status_invalid(manager):
    order = manager.create_order(1, 1, "10.11.2026", "12:00")
    with pytest.raises(InvalidStatusError):
        manager.update_status(order.id, "Невідомий")


# ----- calculate_total_price -----

# без препаратів ціна дорівнює ціні послуги
def test_total_price(manager):
    order = manager.create_order(1, 2, "10.11.2026", "12:00")
    assert order.calculate_total_price() == 1200


# пілінг 1200 + 2 ампули по 450 = 2100
def test_total_price_with_products(manager):
    order = manager.create_order(1, 2, "10.11.2026", "12:00")
    manager.add_product_to_order(order.id, 1, 2)
    assert order.calculate_total_price() == 2100
