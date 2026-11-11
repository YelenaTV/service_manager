# Beauty Clinic — Service Management System

## Встановлення

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Файли даних (створюються автоматично)

| Файл | Що зберігає |
|---|---|
| clients.json | клієнти та картки пацієнтів |
| orders.json | візити, статуси, препарати |
| products.json | залишки складу |
| orders.csv | експорт візитів (пункт меню 10) |
| actions.log | журнал дій (декоратор `@log_action`) |

## Структура

- `main.py` — меню
- `manager.py` — бізнес-логіка (`ServiceManager`)
- `models.py` — класи `Client`, `PatientProfile`, `Service`, `Product`, `Appointment`
- `storage.py` — JSON та CSV
- `decorators.py` — `@log_action`
- `exceptions.py` — власні винятки
