# спільні дані для тестів, pytest сам знаходить цей файл

# pytest - бібліотека для тестів
import pytest

# менеджер, який будемо тестувати
from manager import ServiceManager


# готовий менеджер з клієнтом, двома послугами і препаратом
# в тестах його можна отримати просто як параметр manager
@pytest.fixture
def manager():
    m = ServiceManager()
    m.add_client("Анна", "Коваль", "0501112233", "anna@mail.com")
    m.add_service("Чистка обличчя", "опис", 800)
    m.add_service("Хімічний пілінг", "опис", 1200)
    m.add_product("Гіалуронова кислота", 10, 450)
    return m
