import json
import telebot
import random
from telebot import types
from environs import Env



env = Env()
env.read_env()
tg_bot_token = env.str("POSTING_TELEGRAM_BOT_API_KEY")
bot=telebot.TeleBot(tg_bot_token)
with open('data_base.json', "r", encoding="utf8") as my_file:
    data_base = json.load(my_file)



@bot.message_handler(commands=['start'])
def start_button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("День рождения", )
    item2=types.KeyboardButton("Свадьба")
    item3=types.KeyboardButton("В школу")
    item4=types.KeyboardButton("Без повода")
    item5=types.KeyboardButton("Другой повод")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(
        message.chat.id,
        "К какому событию готовимся? Выберите один из вариантов, либо укажите свой"
        ,reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in [
    "День рождения",
    "Свадьба",
    "В школу",
    "Без повода",
    "Другой повод"
    ]
)
def message_reply(message):
    if message.text != "Другой повод":
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
    else:
        bot.send_message(
            message.chat.id,
            "Какой у вас повод?",
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
    item1 = types.KeyboardButton("Заказать консультацию")
    item2 = types.KeyboardButton("Посмотреть всю коллекцию")
    markdown.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "*Хотите что то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста*",
        reply_markup=markdown,
        parse_mode='MarkdownV2',
    )


@bot.message_handler(func=lambda message: message.text == "Посмотреть всю коллекцию")
def next_fowers(message):
    flowers_number = random.randint(0, 3)
    with open(data_base[flowers_number]["img"], 'rb') as file:
        bot.send_photo(
            message.chat.id,
            photo=file,
            caption=data_base[flowers_number]["name"] + data_base[flowers_number]["structure"]+data_base[flowers_number]["meaning"]+data_base[flowers_number]["price"],
        )


@bot.message_handler(content_types='text')
def choise_price(message):
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


bot.infinity_polling()

