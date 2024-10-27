import telebot
import gspread
from google.oauth2.service_account import Credentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройки
TELEGRAM_TOKEN = '8147464873:AAHWA1HSYs5FaI2Qn8ttwlx3ZN5A9rPkZ_k'
SHEET_ID = '1khEnQ392mtaiDLASitShRNRluYZYH5STDnln4oHnCpc'  # ID Google таблицы

# Авторизация в Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("/root/telega1_bot/gentle-scene-439821-t8-9d74c64096a0.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Хранение данных пользователя
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    services = {row['Service'] for row in sheet.get_all_records()}

    markup = InlineKeyboardMarkup()
    for service in services:
        markup.add(InlineKeyboardButton(service, callback_data=f"service:{service}"))
        
 # Добавляем кнопку "Вернуться в начало"
    markup.add(InlineKeyboardButton("Вернуться в начало", callback_data="restart"))
    
    bot.send_message(message.chat.id, "Выберите службу доставки:", reply_markup=markup)

# Обработка выбора службы доставки
@bot.callback_query_handler(func=lambda call: call.data.startswith('service:'))
def select_service(call):
    service = call.data.split(':')[1]
    user_data[call.message.chat.id]['service'] = service

    cities = {row['City'] for row in sheet.get_all_records() if row['Service'] == service}
    
    markup = InlineKeyboardMarkup()
    for city in cities:
        markup.add(InlineKeyboardButton(city, callback_data=f"city:{city}"))
    
    bot.edit_message_text("Выберите город:", call.message.chat.id, call.message.message_id, reply_markup=markup)

 # Добавляем кнопку "Вернуться в начало"
    markup.add(InlineKeyboardButton("Вернуться в начало", callback_data="restart"))
    
# Обработка выбора города
@bot.callback_query_handler(func=lambda call: call.data.startswith('city:'))
def select_city(call):
    city = call.data.split(':')[1]
    user_data[call.message.chat.id]['city'] = city
    
    sizes = {row['Size'] for row in sheet.get_all_records() if row['City'] == city}
    
    markup = InlineKeyboardMarkup()
    for size in sizes:
        markup.add(InlineKeyboardButton(size, callback_data=f"size:{size}"))
    
    bot.edit_message_text("Выберите габариты посылки:", call.message.chat.id, call.message.message_id, reply_markup=markup)

 # Добавляем кнопку "Вернуться в начало"
    markup.add(InlineKeyboardButton("Вернуться в начало", callback_data="restart"))

# Обработка выбора габаритов и расчет стоимости
@bot.callback_query_handler(func=lambda call: call.data.startswith('size:'))
def select_size(call):
    size = call.data.split(':')[1]
    user_data[call.message.chat.id]['size'] = size
    
    # Извлекаем нужные данные из Google Sheets
    service = user_data[call.message.chat.id]['service']
    city = user_data[call.message.chat.id]['city']
    
    rows = sheet.get_all_records()
    price = None
    for row in rows:
        if row['Service'] == service and row['City'] == city and row['Size'] == size:
            price = row['Price']
            break
    
    if price:
        bot.edit_message_text(f"Стоимость доставки: {price} рублей", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text("К сожалению, доставка с такими параметрами недоступна.", call.message.chat.id, call.message.message_id)

# Добавляем кнопку "Вернуться в начало"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Вернуться в начало", callback_data="restart"))
    bot.send_message(call.message.chat.id, "Хотите сделать новый запрос?", reply_markup=markup)

# Обработка нажатия кнопки "Вернуться в начало"
@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call):
    start(call.message)
    
# Запуск бота
bot.polling()
