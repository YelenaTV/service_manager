# відправка повідомлень клієнтам через http запит
# справжнього смс сервісу немає, тому використовуємо тестовий api jsonplaceholder
# він приймає запит і відповідає так, ніби повідомлення збережене

# requests - бібліотека для http запитів (ставиться через pip install requests)
import requests

# адреса тестового api, куди відправляємо повідомлення
NOTIFICATION_URL = "https://jsonplaceholder.typicode.com/posts"
# скільки секунд чекати відповідь, щоб програма не зависла
TIMEOUT = 5


# відправляємо повідомлення клієнту, повертає True якщо вдалось
def send_notification(phone: str, message: str) -> bool:
    # дані, які відправляємо на сервер
    data = {"phone": phone, "message": message}
    try:
        response = requests.post(NOTIFICATION_URL, json=data, timeout=TIMEOUT)
        # 200 або 201 означає що сервер прийняв запит
        return response.status_code in (200, 201)
    except requests.RequestException:
        # немає інтернету або сервер не відповів - програма працює далі
        return False


# текст повідомлення про новий візит
def visit_created_message(appointment) -> str:
    return (f"{appointment.client.first_name}, ви записані на "
            f"\"{appointment.service.name}\" {appointment.date} о {appointment.time}.")


# текст повідомлення про зміну статусу
def status_changed_message(appointment) -> str:
    return (f"{appointment.client.first_name}, статус вашого візиту "
            f"{appointment.date}: {appointment.status}.")