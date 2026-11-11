# тести для відправки повідомлень (функція send_notification з notifications.py)
#
# send_notification відправляє запит в інтернет на тестовий сервер
# сервер відповідає кодом: 201 - все ок, 500 - помилка сервера
# якщо тест буде реально ходити в інтернет, то без wi-fi він впаде, хоча код правильний
# тому справжній запит не робимо, а підміняємо його фейковим через mock
# так можна перевірити всі ситуації без інтернету

# patch - тимчасово підміняє функцію на фейкову
# Mock - фейковий об'єкт, якому можна задати будь-яку відповідь
from unittest.mock import patch, Mock

# requests - потрібен тільки щоб створити помилку "немає з'єднання"
import requests

# функція, яку тестуємо
from notifications import send_notification


# @patch підміняє requests.post у файлі notifications.py на фейкову функцію mock_post
# підміна працює тільки поки йде цей тест, потім все повертається як було


# сервер прийняв повідомлення - функція має повернути True
@patch("notifications.requests.post")
def test_send_notification(mock_post):
    # кажемо фейковій функції: "відповідай так, ніби сервер повернув 201"
    mock_post.return_value = Mock(status_code=201)
    # перевіряємо, що send_notification повернула True
    assert send_notification("0501112233", "Привіт") == True


# сервер відповів помилкою 500 - функція має повернути False
@patch("notifications.requests.post")
def test_send_notification_error(mock_post):
    # "сервер повернув 500"
    mock_post.return_value = Mock(status_code=500)
    assert send_notification("0501112233", "Привіт") == False


# немає інтернету - програма не повинна впасти, а має повернути False
@patch("notifications.requests.post")
def test_send_notification_no_internet(mock_post):
    # side_effect - замість відповіді фейкова функція викине помилку з'єднання
    mock_post.side_effect = requests.ConnectionError()
    assert send_notification("0501112233", "Привіт") == False
