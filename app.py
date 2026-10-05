import os
import telebot
from flask import Flask, request
from telebot import types

# --- КОНФИГУРАЦИЯ ---
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise ValueError("❌ Токен не найден! Добавьте переменную TOKEN на Render.")

# Адрес вашего будущего сервиса на Render (изменим позже)
WEBHOOK_URL = 'https://hotel-bot-i0qd.onrender.com/'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ВАШИ ТЕКСТЫ И МЕНЮ ---
ANSWERS = {
    'Забронировать номер':
        'Забронировать номер вы можете на нашем сайте по ссылке https://skolkovo.smorodina-hotels.com/\n\n'
        'Или написав нам на электронную почту: booking.cssk@smorodina-hotels.com\n'
        'Или по телефону: 8(495)787-78-80',

    'Как добраться':
        'Из центра Москвы можно добраться на автомобиле по многополосному Минскому шоссе, '
        'адрес для навигатора: Сколково, Большой Бульвар д. 56.\n\n'
        'На метро: станция МЦД «Сколково» расположена в 2,5 км от отеля. От станции курсируют '
        'автобусы SK1 (на нём должно быть написано Татнефть) с интервалом 5-7 мин. (SK1 ТМК идёт не к нам, а в другую сторону).\n\n'
        'Автобусами:\n'
        'На автобусе SK2 можно добраться до отеля от метро Филёвский парк.\n'
        'На автобусе SK3 можно добраться до отеля от метро Говорово.\n'
        'На автобусе SK4 можно добраться до отеля от метро Тропарёво.',

    'Связаться с отелем':
        'Связаться с нами можно по телефону: 8(495)787-78-80\n'
        'Или по телефону: +7(967)079-04-93 (на этот номер вы также можете написать в Телеграм, Макс, WhatsApp – наши сотрудники на связи).\n'
        'Электронная почта: booking.cssk@smorodina-hotels.com',

    'Связаться с рестораном':
        'Позвонить в ресторан можно по телефону: 8(495)787-78-81',

    'Связаться со спа':
        'Связаться со спа-центром вы можете по телефону +7(967)079-04-95\n'
        'Также по этому номеру можно написать нам в Телеграм, Макс, WhatsApp.',

    'Организовать конференцию':
        'Наш конференц-центр подходит для мероприятий любого уровня. 8 конференц-залов, залы трансформеры, '
        'много света, встроенное современное оборудование, кейтеринг на любой вкус, всё это лишь малая часть того, '
        'что мы можем предложить для вашего события.\n\n'
        'Узнать подробности, получить расчёт, договориться об экскурсии по отелю можно написав на почту: '
        'sales.cssk@smorodina-hotels.com\n'
        'Или позвонив по телефону: 8(495)787-78-80 доб. 1402.',

    'Парковка':
        'Если вы едете к нам на личном автомобиле и вам необходима парковка, просьба связаться с нами заранее '
        'для организации пропуска и парковочного места. Связаться с нами можно по телефону +7(495)787-78-80 '
        'или по почте bookings.cssk@smorodina-hotels.com\n\n'
        'При оформлении пропуска, парковка возможна ТОЛЬКО на парковке отеля. В любых других местах ИЦ Сколково '
        'парковка запрещена!\n\n'
        'Более подробную информацию о парковке и правилах въезда вы можете найти по ссылке: '
        'https://skolkovo.smorodina-hotels.com/parking'
}

def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Забронировать номер',
        'Как добраться',
        'Связаться с отелем',
        'Связаться с рестораном',
        'Связаться со спа',
        'Организовать конференцию',
        'Парковка'
    ]
    keyboard.add(*buttons)
    return keyboard

# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Добрый день! С каким вопросом я могу вам помочь?',
        reply_markup=main_menu_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text in ANSWERS:
        bot.send_message(
            message.chat.id,
            ANSWERS[message.text],
            reply_markup=main_menu_keyboard()
        )

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (WEBHOOK) ---
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "Бот работает через Webhook!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)