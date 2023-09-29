# import os
import random
from io import BytesIO
import telebot
from PIL import Image

# Задаем токен бота
TOKEN = '5811292443:AAGYOP3ht35oIu1UIUJJxze5Ajds08ilG58'
bot = telebot.TeleBot(TOKEN)

# Создаем список kamoji
kamoji_list = [
    "¯\_(ツ)_/¯",
    "(¬‿¬)",
    "(╯°□°）╯︵ ┻━┻",
    "ಠ_ಠ",
    "┬─┬ ノ( ゜-゜ノ)",
    "(づ｡◕‿‿◕｡)づ",
    "(｡♥‿♥｡)"
]


# Функция для преобразования изображения в ASCII-арт
def image_to_ascii(image, width=60):
    ascii_chars = "@%#*+=-:. "
    # Изменяем размер изображения с учетом пропорций
    new_height = int(width * image.height / image.width)
    image = image.resize((width, new_height))
    # Конвертируем изображение в оттенки серого
    image = image.convert('L')
    # Получаем данные пикселей изображения
    pixels = image.getdata()
    # Преобразуем пиксели в символы ASCII
    ascii_str = ''.join([ascii_chars[p // 32] for p in pixels])
    # Возвращаем ASCII-арт, разбитый на строки
    return '\n'.join([ascii_str[i:i + width] for i in range(0, len(ascii_str), width)])


# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот, который преобразует изображения в ASCII-арт и отправляет различные kamoji по "
                 "запросу. Просто отправьте мне изображение или используйте команду /kamoji.")


# Обработчик команды /kamoji
@bot.message_handler(commands=['kamoji'])
def send_kamoji(message):
    # Выбираем случайный kamoji из списка
    kamoji = random.choice(kamoji_list)
    # Отправляем kamoji пользователю
    bot.send_message(message.chat.id, kamoji)


# Обработчик сообщений с изображениями
@bot.message_handler(content_types=['photo'])
def convert_image_to_ascii(message):
    # Получаем информацию о файле изображения
    file_info = bot.get_file(message.photo[-1].file_id)
    # Загружаем файл изображения
    file = bot.download_file(file_info.file_path)

    # Открываем изображение с помощью библиотеки PIL
    with Image.open(BytesIO(file)) as image:
        # Преобразуем изображение в ASCII-арт
        ascii_art = image_to_ascii(image)
        # Если длина ASCII-арта меньше 4096 символов, отправляем его пользователю
        # 4096 символов - максимальная длина сообщения в Telegram
        if len(ascii_art) < 4096:
            bot.send_message(message.chat.id, f"<pre>{ascii_art}</pre>", parse_mode='HTML')
        else:  # В противном случае отправляем сообщение об ошибке
            bot.send_message(message.chat.id,
                             "Изображение слишком большое для преобразования в ASCII-арт. Пожалуйста, попробуйте "
                             "отправить изображение меньшего размера.")


# Запускаем бота и его постоянное обновление
if __name__ == '__main__':
    bot.polling(none_stop=True)
