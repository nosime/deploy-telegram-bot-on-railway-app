
import psycopg2

import asyncio
from datetime import datetime
from typing import Optional

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup    
from aiogram.dispatcher.filters import Text
import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import signal
import requests
import json
import emoji
import time
import os
import socks
import socket
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes



API_TOKEN = '5511970076:AAHbXkdtloQ2fHt3qwrwAm0QZ2yCKfarV0I'
DB_URI =""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

async def gen_main_markup():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    #arkup = ReplyKeyboardMarkup(resize_keyboard=False,one_time_keyboard=False)
    
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📖BUTTON1📖", callback_data="inst"),
               InlineKeyboardButton("💰BUTTON2💰", callback_data="bal"),
               InlineKeyboardButton("✍NOTE✍️", callback_data="add_comment"),
			   
               
               )
                                    
              
    return markup

    
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
	user_id = message.from_user.id
	username = message.from_user.username
	if message.chat.type== "private":




				

		db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
	    
		result = db_object.fetchone()

	    

		if not result:
			db_object.execute("INSERT INTO users(id, username) VALUES (%s, %s)", (user_id, username))
			db_connection.commit()
			await bot.send_message(message.chat.id, f"السلام عليكم 🖐\n Welcome {username}\nYou have got 2 points for free",reply_markup=await gen_main_markup())
	  		
	  		
		else:
			await bot.send_message(message.chat.id, f"السلام عليكم 🖐\n Welcome {username}",reply_markup=await gen_main_markup())

  	

		   
		    

print("working..............")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)



# Sử dụng hàm send_telegram_message
async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)
bot_token = "5511970076:AAHbXkdtloQ2fHt3qwrwAm0QZ2yCKfarV0I"
chat_id = "-1001896695563"

#Lấy proxy HTTP bằng API từ website
def get_proxy_list_http():
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(url)
    
    if response.status_code == 200:
        proxy_list = response.text.split('\n')
        return proxy_list
    else:
        return []

#Lấy proxy SOCKS4 bằng API từ website
def get_proxy_list_socks4():
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(url)
    
    if response.status_code == 200:
        proxy_list = response.text.split('\n')
        return proxy_list
    else:
        return []

#Lấy proxy SOCKS5 bằng API từ website
def get_proxy_list_sock5():
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(url)
    
    if response.status_code == 200:
        proxy_list = response.text.split('\n')
        return proxy_list
    else:
        return []

#Check loại proxy
def check_proxy_type(proxy_list):
    result = {}

    for proxy in proxy_list:
        proxy_type = check_single_proxy_type(proxy)
        result[proxy] = proxy_type

    return result

def check_single_proxy_type(proxy):
    proxy_type = 'Unknown'

    # Chuyển đổi proxy thành tuple (host, port)
    proxy_parts = proxy.split(':')
    proxy_host = proxy_parts[0]
    proxy_port = int(proxy_parts[1])

    # Kiểm tra loại proxy HTTP
    try:
        socks.set_default_proxy(socks.HTTP, proxy_host, proxy_port)
        socket.socket = socks.socksocket
        response = socket.socket().connect(('www.google.com', 80))
        return 'HTTP'
    except Exception:
        pass

    # Kiểm tra loại proxy HTTPS
    try:
        socks.set_default_proxy(socks.HTTPS, proxy_host, proxy_port)
        socket.socket = socks.socksocket
        response = socket.socket().connect(('www.google.com', 443))
        return 'HTTPS'
    except Exception:
        pass

    # Kiểm tra loại proxy SOCKS4
    try:
        socks.set_default_proxy(socks.SOCKS4, proxy_host, proxy_port)
        socket.socket = socks.socksocket
        response = socket.socket().connect(('www.google.com', 80))
        return 'SOCKS4'
    except Exception:
        pass

    # Kiểm tra loại proxy SOCKS5
    try:
        socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
        socket.socket = socks.socksocket
        response = socket.socket().connect(('www.google.com', 80))
        return 'SOCKS5'
    except Exception:
        pass

    return proxy_type

def check_proxy(proxy):
    # Sử dụng proxy để gửi yêu cầu HTTP và kiểm tra tính sống còn của proxy
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy}, timeout=10)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# #Gửi proxy HTTP đã lấy vể telegram - Trả lời lệnh /hp +(số lượng proxy)
async def send_proxy_hp(rep) -> None:
    proxies = get_proxy_list_http()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            break
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# #Gửi proxy HTTP đã lấy vể telegram - Trả lời lệnh /hpa +(số lượng proxy)
async def send_proxy_hpa(rep) -> None:
    proxies = get_proxy_list_http()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            time.sleep(10)
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# #Gửi proxy SOCKS4 đã lấy vể telegram - Trả lời lệnh /sk4 +(số lượng proxy)
async def send_proxy_sk4(rep) -> None:
    proxies = get_proxy_list_socks4()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            break
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# #Gửi proxy SOCKS4 đã lấy vể telegram - Trả lời lệnh /sk4a +(số lượng proxy)
async def send_proxy_sk4a(rep) -> None:
    proxies = get_proxy_list_socks4()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            time.sleep(10)
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# #Gửi proxy SOCKS5 đã lấy vể telegram - Trả lời lệnh /sk5 +(số lượng proxy)
async def send_proxy_sk5(rep) -> None:
    proxies = get_proxy_list_sock5()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            break
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# #Gửi proxy SOCKS5 đã lấy vể telegram - Trả lời lệnh /sk5a +(số lượng proxy)
async def send_proxy_sk5a(rep) -> None:
    proxies = get_proxy_list_sock5()
    count = 0
    message = ''
    total_proxies = len(proxies)
    for proxy in proxies:
        count += 1
        #result = check_proxy_type([proxy])
        #for proxy, proxy_type in result.items():
        message += f'{proxy}\n'
        if count == rep:
            await send_telegram_message(bot_token, chat_id, message)
            count = 0
            message = ''
            time.sleep(10)
    
    if message != '':
        await send_telegram_message(bot_token, chat_id, message)
    await send_telegram_message(bot_token, chat_id, f'Total proxies: {total_proxies}')

# Gửi proxy + loại proxy đã check về Telegram - Trả lời lệnh /ck +(list proxy)
async def check_vs_send_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    proxy_list = []

    # Kiểm tra xem tin nhắn có phản hồi từ bot hay không
    if update.message.reply_to_message:
        # Lấy nội dung của tin nhắn được phản hồi
        replied_message = update.message.reply_to_message.text
        # Tách các proxy từ nội dung
        proxy_list = replied_message.split('\n')

    # Lấy danh sách proxy từ đối số truyền vào
    proxy_list += context.args

    await send_check_proxies(update, context, proxy_list)

async def send_check_proxies(update: Update, context: ContextTypes.DEFAULT_TYPE, proxy_list) -> None:
    live_proxies = []

    for proxy in proxy_list:
        if check_proxy(proxy):
            proxy_type = check_single_proxy_type(proxy)
            live_proxies.append(f"{proxy} => {proxy_type}")

    if len(live_proxies) > 0:
        proxy_message = icon_x+"Proxy live:\n" + "\n".join(live_proxies)
    else:
        proxy_message = icon_d+"Không có proxy live !"

    await send_telegram_message(bot_token, chat_id, proxy_message)



async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# #Lệnh thi hành yêu cầu => /hp
async def hp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_hp(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

# #Lệnh thi hành yêu cầu => /hpa
async def hpa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_hpa(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

# #Lệnh thi hành yêu cầu => /sk4
async def sk4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_sk4(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

# #Lệnh thi hành yêu cầu => /sk4a
async def sk4a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_sk4a(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

# #Lệnh thi hành yêu cầu => /sk5
async def sk5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_sk5(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

# #Lệnh thi hành yêu cầu => /sk5a
async def sk5a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1:
        rep_sl = int(args[0])
        await send_proxy_sk5a(rep_sl)
    else:
        await update.message.reply_text("Lệnh không hợp lệ. Vui lòng chỉ định số lượng proxy cần in.")

#Lệnh thi hành yêu cầu => /ck
async def check_and_send_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    proxy_list = context.args
    await check_vs_send_proxy(update, context)


icon_x = emoji.emojize(":green_circle:")
icon_d = emoji.emojize(":red_circle:")

app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("hp",hp ))
app.add_handler(CommandHandler("hpa",hpa ))
app.add_handler(CommandHandler("sk4",sk4 ))
app.add_handler(CommandHandler("sk4a",sk4a ))
app.add_handler(CommandHandler("sk5",sk5 ))
app.add_handler(CommandHandler("sk5a",sk5a ))
app.add_handler(CommandHandler("ck", check_and_send_proxy))
app.run_polling()

  

    
     
	     		
