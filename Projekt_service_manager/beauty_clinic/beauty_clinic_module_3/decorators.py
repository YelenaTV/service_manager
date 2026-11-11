# декоратор для запису всіх дій у файл actions.log

# os - щоб знайти папку, де лежить програма
import os
# datetime - щоб записати дату і час дії
from datetime import datetime
# wraps - щоб функція після декоратора не втратила свою назву
from functools import wraps
# Callable - тип "функція", для підказки типів
from typing import Callable

# файл логу буде поруч з програмою
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions.log")


# декоратор - записує в actions.log час, назву функції і чи все пройшло ок
def log_action(func: Callable) -> Callable:

    # внутрішня функція: викликає оригінальну функцію і записує результат у лог
    @wraps(func)
    def wrapper(*args, **kwargs):
        # поточна дата і час
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # збираємо параметри в один рядок, args[0] - це сам менеджер (self), його не пишемо
        params = ", ".join([str(a) for a in args[1:]] +
                           [f"{k}={v}" for k, v in kwargs.items()])
        # якщо програму зупинять посеред функції, в лозі буде ПЕРЕРВАНО
        line = f"{time_now} | {func.__name__}({params}) | ПЕРЕРВАНО\n"
        try:
            result = func(*args, **kwargs)
            line = f"{time_now} | {func.__name__}({params}) | OK\n"
            return result
        except Exception as error:
            line = f"{time_now} | {func.__name__}({params}) | ПОМИЛКА: {error}\n"
            raise  # помилку далі обробляє меню
        finally:
            # finally спрацює в будь-якому випадку, тому запис в файл тут
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(line)

    return wrapper
