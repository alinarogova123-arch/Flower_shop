from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

import app.func as func
import app.keyboards as kb

router = Router()


class UserState(StatesGroup):
    choosing_occasion = State()
    choosing_budget = State()

    waiting_for_phone = State()

    waiting_for_order_name = State()
    waiting_for_order_address = State()
    waiting_for_order_date = State()
    waiting_for_order_time = State()


async def show_main_menu(target, state: FSMContext):
    await state.clear()

    text = func.get_main_menu_text()
    markup = kb.main_menu_keyboard()

    if isinstance(target, CallbackQuery):
        try:
            await target.message.edit_text(text, reply_markup=markup)
        except Exception:
            await target.message.answer(text, reply_markup=markup)
        await target.answer()
    else:
        await target.answer(text, reply_markup=markup)


async def send_bouquet_message(message: Message, bouquet: dict, from_catalog: bool):
    photo = FSInputFile(func.get_bouquet_image_path(bouquet))
    await message.answer_photo(
        photo=photo,
        caption=func.format_bouquet_text(bouquet),
        reply_markup=kb.bouquet_keyboard(from_catalog=from_catalog)
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        func.get_welcome_text(),
        reply_markup=kb.consent_keyboard()
    )


@router.callback_query(F.data == "consent_yes")
async def consent_yes(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)


@router.callback_query(F.data == "consent_no")
async def consent_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Без согласия на обработку данных я не могу продолжить работу.\n\n"
        "Нажмите /start, если передумаете."
    )
    await callback.answer()


@router.callback_query(F.data == "to_main")
async def to_main(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)


@router.callback_query(F.data == "pick_bouquet")
async def pick_bouquet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.choosing_occasion)
    await callback.message.edit_text(
        func.get_pick_text(),
        reply_markup=kb.occasion_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_occasions")
async def back_to_occasions(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.choosing_occasion)
    await callback.message.edit_text(
        func.get_pick_text(),
        reply_markup=kb.occasion_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("occasion_"))
async def choose_occasion(callback: CallbackQuery, state: FSMContext):
    occasion = callback.data.replace("occasion_", "")
    await state.update_data(occasion=occasion)
    await state.set_state(UserState.choosing_budget)

    await callback.message.edit_text(
        func.get_budget_text(occasion),
        reply_markup=kb.budget_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("budget_"))
async def choose_budget(callback: CallbackQuery, state: FSMContext):
    budget = callback.data.replace("budget_", "")
    data = await state.get_data()
    occasion = data.get("occasion")

    bouquets = func.filter_bouquets(occasion=occasion, budget=budget)

    if not bouquets:
        await callback.message.edit_text(
            func.get_no_bouquet_text(),
            reply_markup=kb.budget_keyboard()
        )
        await callback.answer()
        return

    first_bouquet = bouquets[0]

    await state.update_data(
        budget=budget,
        filtered_bouquets=bouquets,
        filtered_index=0,
        bouquet_name=first_bouquet["name"]
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await send_bouquet_message(callback.message, first_bouquet, from_catalog=False)
    await callback.answer()


@router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery, state: FSMContext):
    bouquets = func.load_bouquets()

    if not bouquets:
        try:
            await callback.message.edit_text("Каталог пока пустой.", reply_markup=kb.back_keyboard())
        except Exception:
            await callback.message.answer("Каталог пока пустой.", reply_markup=kb.back_keyboard())
        await callback.answer()
        return

    first_bouquet = bouquets[0]

    await state.update_data(
        catalog_bouquets=bouquets,
        catalog_index=0,
        bouquet_name=first_bouquet["name"]
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await send_bouquet_message(callback.message, first_bouquet, from_catalog=True)
    await callback.answer()


@router.callback_query(F.data == "next_catalog_bouquet")
async def next_catalog_bouquet(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bouquets = data.get("catalog_bouquets", [])

    if not bouquets:
        await callback.answer("Каталог пустой")
        return

    index = data.get("catalog_index", 0)
    index = (index + 1) % len(bouquets)
    bouquet = bouquets[index]

    await state.update_data(
        catalog_index=index,
        bouquet_name=bouquet["name"]
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await send_bouquet_message(callback.message, bouquet, from_catalog=True)
    await callback.answer()


@router.callback_query(F.data == "next_filtered_bouquet")
async def next_filtered_bouquet(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bouquets = data.get("filtered_bouquets", [])

    if not bouquets:
        await callback.answer("Букеты не найдены")
        return

    index = data.get("filtered_index", 0)
    index = (index + 1) % len(bouquets)
    bouquet = bouquets[index]

    await state.update_data(
        filtered_index=index,
        bouquet_name=bouquet["name"]
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await send_bouquet_message(callback.message, bouquet, from_catalog=False)
    await callback.answer()


@router.callback_query(F.data == "consultation")
async def consultation_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_phone)

    try:
        await callback.message.edit_text(
            func.get_consultation_text(),
            reply_markup=kb.back_keyboard()
        )
    except Exception:
        await callback.message.answer(
            func.get_consultation_text(),
            reply_markup=kb.back_keyboard()
        )

    await callback.answer()


@router.message(UserState.waiting_for_phone)
async def get_client_phone(message: Message, state: FSMContext):
    phone = func.normalize_phone(message.text)

    if not func.is_valid_phone(phone):
        await message.answer("Введите номер телефона в формате +79991234567")
        return

    florist_id = func.get_florist_id()

    if florist_id is None:
        await message.answer("Ошибка: не указан FLORIST_ID в .env")
        await state.clear()
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    florist_text = (
        "Новая заявка на консультацию\n\n"
        f"Телефон: {phone}\n"
        f"Клиент: {user.full_name}\n"
        f"Username: {username}\n"
        f"User ID: {user.id}"
    )

    try:
        await message.bot.send_message(florist_id, florist_text)
        await message.answer(
            "Флорист скоро свяжется с вами.",
            reply_markup=kb.back_keyboard()
        )
    except Exception:
        await message.answer("Ошибка отправки заявки флористу.")

    await state.clear()


@router.callback_query(F.data == "order_bouquet")
async def order_bouquet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_order_name)
    await callback.message.answer("Как вас зовут?")
    await callback.answer()


@router.message(UserState.waiting_for_order_name)
async def get_order_name(message: Message, state: FSMContext):
    order_name = message.text.strip()

    if not order_name:
        await message.answer("Введите имя.")
        return

    await state.update_data(order_name=order_name)
    await state.set_state(UserState.waiting_for_order_address)
    await message.answer("Укажите адрес доставки:")


@router.message(UserState.waiting_for_order_address)
async def get_order_address(message: Message, state: FSMContext):
    order_address = message.text.strip()

    if not order_address:
        await message.answer("Введите адрес доставки.")
        return

    await state.update_data(order_address=order_address)
    await state.set_state(UserState.waiting_for_order_date)
    await message.answer("Укажите дату доставки:")


@router.message(UserState.waiting_for_order_date)
async def get_order_date(message: Message, state: FSMContext):
    order_date = message.text.strip()

    if not order_date:
        await message.answer("Введите дату доставки.")
        return

    await state.update_data(order_date=order_date)
    await state.set_state(UserState.waiting_for_order_time)
    await message.answer("Укажите время доставки:")


@router.message(UserState.waiting_for_order_time)
async def get_order_time(message: Message, state: FSMContext):
    order_time = message.text.strip()

    if not order_time:
        await message.answer("Введите время доставки.")
        return

    await state.update_data(order_time=order_time)
    data = await state.get_data()

    await message.answer(
        func.get_order_summary(data),
        reply_markup=kb.order_confirm_keyboard()
    )


@router.callback_query(F.data == "restart_order")
async def restart_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bouquet_name = data.get("bouquet_name")

    await state.clear()

    if bouquet_name:
        await state.update_data(bouquet_name=bouquet_name)

    await state.set_state(UserState.waiting_for_order_name)
    await callback.message.answer("Давайте заполним заказ заново.\n\nКак вас зовут?")
    await callback.answer()


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    courier_id = func.get_courier_id()
    order_text = func.get_order_summary(data)

    if courier_id is None:
        await callback.message.answer("Ошибка: не указан COURIER_ID в .env")
        await callback.answer()
        return

    try:
        await callback.message.bot.send_message(courier_id, order_text)
    except Exception:
        await callback.message.answer("Ошибка отправки заказа курьеру.")
        await callback.answer()
        return

    await state.clear()

    await callback.message.answer(
        func.get_payment_stub_text(),
        reply_markup=kb.payment_placeholder_keyboard()
    )
    await callback.answer()