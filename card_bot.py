# подключение библиотек
# В google colab добавить: !pip install pyTelegramBotAPI
# В google colab добавить: !pip install Faker
# для установки необходимо в файл requirements.text добавить строки
# 'PyTelegramBotApi'
# 'faker'

from telebot import TeleBot, types
from faker import Faker


bot = TeleBot(token='################### вставить токен', parse_mode='html') # создание бота

faker = Faker() # утилита для генерации номеров кредитных карт

# объект клавиаутры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='VISA'),
    types.KeyboardButton(text='Mastercard'),
)
# второй ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='Maestro'),
    types.KeyboardButton(text='JCB'),
)

@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Добрый день <b>{0.first_name}</b> !\nНужно сгенерировать номер тестовой банковской карты для прохождения тест-кейсов в тестовой среде? Не вопрос!\nPS: Давай, нажал, скопировал и вышел, приключение на 5 секунд! 😉\nВыбери тип карты 👇🏼:'.format(message.from_user)
,parse_mode='html', # текст сообщения
        reply_markup=card_type_keybaord,
    )
    sti = open('wabadu.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваем занчение переменной 'card_type'
    if message.text == 'VISA':
        card_type = 'visa'
    elif message.text == 'Mastercard':
        card_type = 'mastercard'
    elif message.text == 'Maestro':
        card_type = 'maestro'
    elif message.text == 'JCB':
        card_type = 'jcb'
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='<b>{0.first_name}</b>, к сожалению, я не понимаю Вас :( \nНапишите мне снова "/start"'.format(message.from_user)
,parse_mode='html',
        )
        return

    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    card_number = faker.credit_card_number(card_type)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Ваша тестовая карта {card_type}:\n<code>{card_number}</code>.\nВозможно, нужна ещё одна, или карта другого формата? Выбирайте.'
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
