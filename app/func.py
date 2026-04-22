import json
import os


def get_welcome_text() -> str:
    return (
        "Добро пожаловать в FlowerShop.\n\n"
        "Закажите доставку праздничного букета, собранного специально для ваших "
        "любимых, родных и коллег.\n\n"
        "Для продолжения необходимо согласие на обработку персональных данных."
    )


def get_main_menu_text() -> str:
    return "Выберите, что хотите сделать:"


def get_pick_text() -> str:
    return "К какому событию готовимся? Выберите один из вариантов:"


def get_budget_text(occasion: str) -> str:
    return f"Повод: {occasion}\n\nНа какую сумму рассчитываете?"


def get_consultation_text() -> str:
    return (
        "Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут.\n\n"
        "Пример: +79991234567"
    )


def normalize_phone(phone: str) -> str:
    return phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def is_valid_phone(phone: str) -> bool:
    phone = normalize_phone(phone)

    if phone.startswith("+"):
        return phone[1:].isdigit() and 10 <= len(phone[1:]) <= 15

    return phone.isdigit() and 10 <= len(phone) <= 15


def _get_env_int(name: str) -> int | None:
    value = os.getenv(name)

    if not value:
        return None

    value = value.strip()
    if value.lstrip("-").isdigit():
        return int(value)

    return None


def get_florist_id() -> int | None:
    return _get_env_int("FLORIST_ID")


def get_courier_id() -> int | None:
    return _get_env_int("COURIER_ID")


def load_bouquets() -> list:
    with open("data_base.json", "r", encoding="utf-8") as file:
        return json.load(file)


def filter_bouquets(occasion: str | None = None, budget: str | None = None) -> list:
    bouquets = load_bouquets()
    result = []

    for bouquet in bouquets:
        occasion_ok = True
        budget_ok = True

        if occasion:
            occasion_ok = occasion in bouquet.get("occasion", [])

        if budget and budget != "Не важно":
            budget_ok = bouquet.get("price_up_to") == budget

        if occasion_ok and budget_ok:
            result.append(bouquet)

    return result


def format_bouquet_text(bouquet: dict) -> str:
    return (
        f"{bouquet['name']}\n\n"
        f"{bouquet['meaning']}\n\n"
        f"Состав:\n{bouquet['structure']}\n\n"
        f"Цена: {bouquet['price']}"
    )


def get_bouquet_image_path(bouquet: dict) -> str:
    return bouquet["img"]


def get_no_bouquet_text() -> str:
    return "Подходящих букетов пока не нашлось. Попробуйте изменить повод или бюджет."


def get_order_summary(data: dict) -> str:
    return (
        "Новый заказ\n\n"
        f"Букет: {data.get('bouquet_name', 'Не указан')}\n"
        f"Имя: {data.get('order_name', 'Не указано')}\n"
        f"Адрес: {data.get('order_address', 'Не указан')}\n"
        f"Дата: {data.get('order_date', 'Не указана')}\n"
        f"Время: {data.get('order_time', 'Не указано')}"
    )


def get_payment_stub_text() -> str:
    return (
        "Заказ сохранен.\n\n"
        "Далее здесь будет этап оплаты.\n"
        "Пока что оплата не подключена."
    )