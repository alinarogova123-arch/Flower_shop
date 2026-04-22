import json
import telebot
import random
from telebot import types
from environs import Env


env = Env()
env.read_env()
manager_id = env.str("MANAGER_ID")
tg_bot_token = env.str("POSTING_TELEGRAM_BOT_API_KEY")
bot=telebot.TeleBot(tg_bot_token)
with open('data_base.json', "r", encoding="utf8") as my_file:
    data_base = json.load(my_file)


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
def message_reply(message):
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
    if message.text == "До 500":
        with open(data_base[0]["img"], 'rb') as file:
            bot.send_photo(
                message.chat.id,
                photo=file,
                reply_markup=markup,
                caption=data_base[0]["name"] + data_base[0]["structure"]+data_base[0]["meaning"]+data_base[0]["price"],
            )
    elif message.text == "До 1000":
        with open(data_base[1]["img"], 'rb') as file:
            bot.send_photo(
                message.chat.id,
                photo=file,
                reply_markup=markup,
                caption=data_base[1]["name"] + data_base[1]["structure"]+data_base[1]["meaning"]+data_base[1]["price"],
            )        
    elif message.text == "До 2000":
        with open(data_base[2]["img"], 'rb') as file:
            bot.send_photo(
                message.chat.id,
                photo=file,
                reply_markup=markup,
                caption=data_base[2]["name"] + data_base[2]["structure"]+data_base[2]["meaning"]+data_base[2]["price"],
            )
    else:
        with open(data_base[3]["img"], 'rb') as file:
            bot.send_photo(
                message.chat.id,
                photo=file,
                reply_markup=markup,
                caption=data_base[3]["name"] + data_base[3]["structure"]+data_base[3]["meaning"]+data_base[3]["price"],
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


# @bot.message_handler(func=lambda message: message.text == "Посмотреть всю коллекцию")
# def next_fowers(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton(text="Заказать букет", callback_data='qwerty')
#     markup.add(btn1)
#     flowers_number = random.randint(0, 3)
#     with open(data_base[flowers_number]["img"], 'rb') as file:
#         bot.send_photo(
#             message.chat.id,
#             photo=file,
#             reply_markup=markup,
#             caption=data_base[flowers_number]["name"] + data_base[flowers_number]["structure"]+data_base[flowers_number]["meaning"]+data_base[flowers_number]["price"],
#         )
#     markdown = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Мне нужна консультация")
#     item2 = types.KeyboardButton("Посмотреть весь каталог")
#     markdown.add(item1, item2)
#     bot.send_message(
#         message.chat.id,
#         "*Хотите что то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста*",
#         reply_markup=markdown,
#         parse_mode='MarkdownV2',
#     )


@bot.message_handler(func=lambda message: message.text == "Мне нужна консультация")
def consultation(message):
    msg = bot.send_message(
    message.chat.id,
    "Укажите ваше имя и номер телефона, и наш флорист перезвонит вам в течение 20 минут"
    )
    bot.register_next_step_handler(msg, get_text)
def get_text(message):
    byuer_phone_number = message.text
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
    bot.send_message(manager_id, f"Покупатель просит консультацию, номер телефона: {byuer_phone_number}")


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

