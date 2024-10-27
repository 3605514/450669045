{\rtf1\ansi\ansicpg1251\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;\f2\fnil\fcharset0 HelveticaNeue;
}
{\colortbl;\red255\green255\blue255;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cspthree\c100000\c100000\c100000;}
\paperw3288\paperh2267\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import telebot\
import gspread\
from google.oauth2.service_account import Credentials\
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton\
\
# \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1080 \
TELEGRAM_TOKEN = '
\f1\fs26 \cf2 8147464873:AAHWA1HSYs5FaI2Qn8ttwlx3ZN5A9rPkZ_k
\f2 \

\f0\fs24 \cf0 '\
SHEET_ID = '1khEnQ392mtaiDLASitShRNRluYZYH5STDnln4oHnCpc'  # ID Google \uc0\u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1099 \
\
# \uc0\u1040 \u1074 \u1090 \u1086 \u1088 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1074  Google Sheets\
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]\
creds = Credentials.from_service_account_file("/Users/denisusikov/Downloads/gentle-scene-439821-t8-eab32ae13bb6.json\'bb, scopes=scopes)\
client = gspread.authorize(creds)\
sheet = client.open_by_key(SHEET_ID).sheet1\
\
# \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1073 \u1086 \u1090 \u1072 \
bot = telebot.TeleBot(TELEGRAM_TOKEN)\
\
# \uc0\u1061 \u1088 \u1072 \u1085 \u1077 \u1085 \u1080 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 \
user_data = \{\}\
\
# \uc0\u1050 \u1086 \u1084 \u1072 \u1085 \u1076 \u1072  /start\
@bot.message_handler(commands=['start'])\
def start(message):\
    user_data[message.chat.id] = \{\}\
    services = \{row['Service'] for row in sheet.get_all_records()\}\
\
    markup = InlineKeyboardMarkup()\
    for service in services:\
        markup.add(InlineKeyboardButton(service, callback_data=f"service:\{service\}"))\
\
    bot.send_message(message.chat.id, "\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080 \u1090 \u1077  \u1089 \u1083 \u1091 \u1078 \u1073 \u1091  \u1076 \u1086 \u1089 \u1090 \u1072 \u1074 \u1082 \u1080 :", reply_markup=markup)\
\
# \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1074 \u1099 \u1073 \u1086 \u1088 \u1072  \u1089 \u1083 \u1091 \u1078 \u1073 \u1099  \u1076 \u1086 \u1089 \u1090 \u1072 \u1074 \u1082 \u1080 \
@bot.callback_query_handler(func=lambda call: call.data.startswith('service:'))\
def select_service(call):\
    service = call.data.split(':')[1]\
    user_data[call.message.chat.id]['service'] = service\
\
    cities = \{row['City'] for row in sheet.get_all_records() if row['Service'] == service\}\
    \
    markup = InlineKeyboardMarkup()\
    for city in cities:\
        markup.add(InlineKeyboardButton(city, callback_data=f"city:\{city\}"))\
    \
    bot.edit_message_text("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080 \u1090 \u1077  \u1075 \u1086 \u1088 \u1086 \u1076 :", call.message.chat.id, call.message.message_id, reply_markup=markup)\
\
# \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1074 \u1099 \u1073 \u1086 \u1088 \u1072  \u1075 \u1086 \u1088 \u1086 \u1076 \u1072 \
@bot.callback_query_handler(func=lambda call: call.data.startswith('city:'))\
def select_city(call):\
    city = call.data.split(':')[1]\
    user_data[call.message.chat.id]['city'] = city\
    \
    sizes = \{row['Size'] for row in sheet.get_all_records() if row['City'] == city\}\
    \
    markup = InlineKeyboardMarkup()\
    for size in sizes:\
        markup.add(InlineKeyboardButton(size, callback_data=f"size:\{size\}"))\
    \
    bot.edit_message_text("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080 \u1090 \u1077  \u1075 \u1072 \u1073 \u1072 \u1088 \u1080 \u1090 \u1099  \u1087 \u1086 \u1089 \u1099 \u1083 \u1082 \u1080 :", call.message.chat.id, call.message.message_id, reply_markup=markup)\
\
# \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1074 \u1099 \u1073 \u1086 \u1088 \u1072  \u1075 \u1072 \u1073 \u1072 \u1088 \u1080 \u1090 \u1086 \u1074  \u1080  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1080 \
@bot.callback_query_handler(func=lambda call: call.data.startswith('size:'))\
def select_size(call):\
    size = call.data.split(':')[1]\
    user_data[call.message.chat.id]['size'] = size\
    \
    # \uc0\u1048 \u1079 \u1074 \u1083 \u1077 \u1082 \u1072 \u1077 \u1084  \u1085 \u1091 \u1078 \u1085 \u1099 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1077  \u1080 \u1079  Google Sheets\
    service = user_data[call.message.chat.id]['service']\
    city = user_data[call.message.chat.id]['city']\
    \
    rows = sheet.get_all_records()\
    price = None\
    for row in rows:\
        if row['Service'] == service and row['City'] == city and row['Size'] == size:\
            price = row['Price']\
            break\
    \
    if price:\
        bot.edit_message_text(f"\uc0\u1057 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  \u1076 \u1086 \u1089 \u1090 \u1072 \u1074 \u1082 \u1080 : \{price\} \u1088 \u1091 \u1073 \u1083 \u1077 \u1081 ", call.message.chat.id, call.message.message_id)\
    else:\
        bot.edit_message_text("\uc0\u1050  \u1089 \u1086 \u1078 \u1072 \u1083 \u1077 \u1085 \u1080 \u1102 , \u1076 \u1086 \u1089 \u1090 \u1072 \u1074 \u1082 \u1072  \u1089  \u1090 \u1072 \u1082 \u1080 \u1084 \u1080  \u1087 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088 \u1072 \u1084 \u1080  \u1085 \u1077 \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1085 \u1072 .", call.message.chat.id, call.message.message_id)\
\
# \uc0\u1047 \u1072 \u1087 \u1091 \u1089 \u1082  \u1073 \u1086 \u1090 \u1072 \
bot.polling()}