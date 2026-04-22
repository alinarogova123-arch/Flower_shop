from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def consent_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Согласен", callback_data="consent_yes"),
                InlineKeyboardButton(text="Не согласен", callback_data="consent_no"),
            ]
        ]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Посмотреть весь каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="Подобрать букет", callback_data="pick_bouquet")],
            [InlineKeyboardButton(text="Мне нужна консультация", callback_data="consultation")],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="to_main")]
        ]
    )


def occasion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="День рождения", callback_data="occasion_День рождения")],
            [InlineKeyboardButton(text="Свадьба", callback_data="occasion_Свадьба")],
            [InlineKeyboardButton(text="В школу", callback_data="occasion_В школу")],
            [InlineKeyboardButton(text="Без повода", callback_data="occasion_Без повода")],
            [InlineKeyboardButton(text="Другой повод", callback_data="occasion_Другой повод")],
            [InlineKeyboardButton(text="Назад", callback_data="to_main")],
        ]
    )


def budget_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="~500", callback_data="budget_До 500")],
            [InlineKeyboardButton(text="~1000", callback_data="budget_До 1000")],
            [InlineKeyboardButton(text="~2000", callback_data="budget_До 2000")],
            [InlineKeyboardButton(text="Больше", callback_data="budget_Больше")],
            [InlineKeyboardButton(text="Не важно", callback_data="budget_Не важно")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_occasions")],
        ]
    )


def bouquet_keyboard(from_catalog: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="Заказать букет", callback_data="order_bouquet")],
        [InlineKeyboardButton(text="Заказать консультацию", callback_data="consultation")],
    ]

    if from_catalog:
        rows.insert(1, [InlineKeyboardButton(text="Следующий", callback_data="next_catalog_bouquet")])
    else:
        rows.insert(1, [InlineKeyboardButton(text="Другой букет", callback_data="next_filtered_bouquet")])

    rows.append([InlineKeyboardButton(text="Назад", callback_data="to_main")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def order_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Все верно", callback_data="confirm_order")],
            [InlineKeyboardButton(text="Составить заново", callback_data="restart_order")],
            [InlineKeyboardButton(text="Назад в меню", callback_data="to_main")],
        ]
    )


def payment_placeholder_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад в меню", callback_data="to_main")]
        ]
    )