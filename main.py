import json
import telebot
import random
from telebot import types
from environs import Env

ALL_BOUQUETS_NAME = []
BOUQUETS_TO_ORDER_NAME = []


env = Env()
env.read_env()
manager_id = env.str("MANAGER_ID")
tg_bot_token = env.str("POSTING_TELEGRAM_BOT_API_KEY")
bot=telebot.TeleBot(tg_bot_token)
with open('data_base.json', "r", encoding="utf8") as my_file:
    data_base = json.load(my_file)
for bouquet in data_base:
    ALL_BOUQUETS_NAME.append(bouquet['name'])


@bot.message_handler(func=lambda message: message.text == '/start' or message.text == 'Отказаться')
def request_for_consent(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Подтвердить")
    item2=types.KeyboardButton("Отказаться")
    markup.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "Подтведите согласие на обработку персональных данных"
        ,reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Подтвердить")
def start_menu(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Посмотреть весь каталог")
    item2=types.KeyboardButton("Подобрать букет")
    item3=types.KeyboardButton("Мне нужна консультация")
    markup.add(item1, item2, item3)
    bot.send_message(
        message.chat.id,
        "Для вашего удобства доступна консультация флориста, подбор букета для нужного события либо просмотр всего каталога"
        ,reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Посмотреть весь каталог")
def get_all_catalog(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for bouquet in data_base:
        item=types.KeyboardButton(bouquet['name'])
        markup.add(item)
        bot.send_message(
            message.chat.id,
            f'{bouquet['name']}\nЦена:{bouquet['price']}',
            reply_markup=markup
            )

@bot.message_handler(func=lambda message: message.text in ALL_BOUQUETS_NAME)
def get_card_bouquet(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Заказать букет", callback_data=message.text)
    markup.add(btn1)
    for bouquet in data_base:
        if message.text == bouquet["name"]:
            with open(bouquet["img"], 'rb') as file:
                bot.send_photo(
                    message.chat.id,
                    photo=file,
                    reply_markup=markup,
                    caption=f'{bouquet["name"]}\n{bouquet["structure"]}\n{bouquet["meaning"]}\nЦена:{bouquet["price"]}\n',
                    )      
    markdown = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Мне нужна консультация")
    item2 = types.KeyboardButton("Посмотреть весь каталог")
    markdown.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "*Хотите что то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста*",
        reply_markup=markdown,
        parse_mode='MarkdownV2',
    )


@bot.callback_query_handler(func=lambda call: call.data in ALL_BOUQUETS_NAME)
def order(call):
    user_data = {}
    user_data["bouquet"] = call.data
    msg = bot.send_message(call.message.chat.id, "Укажите ваши ФИО")
    bot.register_next_step_handler(msg, get_buyer_name, user_data=user_data)

def get_buyer_name(message, user_data):
    user_data["name"] = message.text
    msg = bot.send_message(message.chat.id, "Укажите ваш номер телефона")
    bot.register_next_step_handler(msg, get_buyer_number, user_data=user_data)

def get_buyer_number(message, user_data):
    user_data["number"] = message.text
    msg = bot.send_message(message.chat.id, "Укажите адрес доставки")
    bot.register_next_step_handler(msg, get_adress, user_data=user_data)

def get_adress(message, user_data):
    user_data["adress"] = message.text
    msg = bot.send_message(message.chat.id, "Укажите дату доставки")
    bot.register_next_step_handler(msg, get_date, user_data=user_data)

def get_date(message, user_data):
    user_data["date"] = message.text
    msg = bot.send_message(message.chat.id, "Укажите время доставки")
    bot.register_next_step_handler(msg, get_time, user_data=user_data)

def get_time(message, user_data):
    user_data["time"] = message.text
    msg = bot.send_message(message.chat.id, "Укажите промокод доставки")
    bot.register_next_step_handler(msg, get_promo, user_data=user_data)

def get_promo(message, user_data):
    user_data["promo"] = message.text
    bot.send_message(message.chat.id, f"Новый заказ: {user_data}")


@bot.message_handler(func=lambda message: message.text == "Подобрать букет")
def bouquet_selection(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("День рождения")
    item2=types.KeyboardButton("Свадьба")
    item3=types.KeyboardButton("В школу")
    item4=types.KeyboardButton("Без повода")
    markup.add(item1, item2, item3, item4)
    bot.send_message(
        message.chat.id,
        "К какому событию готовимся? Выберите один из вариантов."
        ,reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in [
    "День рождения",
    "Свадьба",
    "В школу",
    "Без повода",
    ]
)

def get_catalog(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for bouquet in data_base:
        for occasion in bouquet['occasion']:
            if message.text == occasion:                
                BOUQUETS_TO_ORDER_NAME.append(bouquet['name'])

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("До 500")
    item2=types.KeyboardButton("До 1000")
    item3=types.KeyboardButton("До 2000")
    item4=types.KeyboardButton("Больше")
    item5=types.KeyboardButton("Не важно")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(
        message.chat.id,
        "На какую сумму рассчитываете?"
        ,reply_markup=markup
    )                              


@bot.message_handler(func=lambda message: message.text in [
    "До 500",
    "До 1000",
    "До 2000",
    "Больше",
    "Не важно"
    ]
)
def message_reply_next(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Заказать букет", callback_data='qwerty')
    markup.add(btn1)
    for bouquet_name in BOUQUETS_TO_ORDER_NAME:
        for bouquet in data_base:
            if bouquet_name == bouquet["name"]:
                if message.text == bouquet["price_up_to"]:
                    with open(bouquet["img"], 'rb') as file:
                        bot.send_photo(
                            message.chat.id,
                            photo=file,
                            reply_markup=markup,
                            caption=f'{bouquet["name"]}\n{bouquet["structure"]}\n{bouquet["meaning"]}\nЦена:{bouquet["price"]}\n',
                            )
                elif message.text == "Не важно":
                    for bouquet in data_base:
                        with open(bouquet["img"], 'rb') as file:
                            bot.send_photo(
                                message.chat.id,
                                photo=file,
                                reply_markup=markup,
                                caption=f'{bouquet["name"]}\n{bouquet["structure"]}\n{bouquet["meaning"]}\nЦена:{bouquet["price"]}\n',
                                )             
    markdown = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Мне нужна консультация")
    item2 = types.KeyboardButton("Посмотреть весь каталог")
    markdown.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "*Хотите что то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста*",
        reply_markup=markdown,
        parse_mode='MarkdownV2',
    )


@bot.message_handler(func=lambda message: message.text == "Мне нужна консультация")
def consultation(message):
    msg = bot.send_message(
    message.chat.id,
    "Укажите ваш номер телефона, и наш флорист перезвонит вам в течение 20 минут"
    )
    bot.register_next_step_handler(msg, get_phone_number)

def get_phone_number(message):
    msg = bot.send_message(
    message.chat.id,
    "Укажите ваше имя, и наш флорист перезвонит вам в течение 20 минут"
    )
    bot.register_next_step_handler(msg, get_user_name, byuer_phone_number = message.text)

def get_user_name(message, byuer_phone_number):
    byuer_user_name = message.text
    bot.send_message(
        message.chat.id,
        "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции."
    )
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Заказать букет", callback_data='qwerty')
    markup.add(btn1)
    flowers_number = random.randint(0, 3)
    with open(data_base[flowers_number]["img"], 'rb') as file:
        bot.send_photo(
            message.chat.id,
            photo=file,
            reply_markup=markup,
            caption=data_base[flowers_number]["name"] + data_base[flowers_number]["structure"]+data_base[flowers_number]["meaning"]+data_base[flowers_number]["price"],
        )
    markdown = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заказать консультацию")
    item2 = types.KeyboardButton("Посмотреть всю коллекцию")
    markdown.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "*Хотите что то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста*",
        reply_markup=markdown,
        parse_mode='MarkdownV2',
    )
    bot.send_message(message.chat.id, f"Имя: {byuer_user_name} Номер телефона: {byuer_phone_number}")






# @bot.message_handler(content_types='text')
# def choise_price(message):
#     markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1=types.KeyboardButton("До 500")
#     item2=types.KeyboardButton("До 1000")
#     item3=types.KeyboardButton("До 2000")
#     item4=types.KeyboardButton("Больше")
#     item5=types.KeyboardButton("Не важно")
#     markup.add(item1, item2, item3, item4, item5)
#     bot.send_message(
#         message.chat.id,
#         "На какую сумму рассчитываете?"
#         ,reply_markup=markup
#     )


bot.infinity_polling()

