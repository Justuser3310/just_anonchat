import telebot
import os
import json

global db

########### CREATE DB IF NOT EXIST

if not os.path.exists('db.json'):
	db = {"token": "None"}
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)

	print('Input token in "None" (db.json)')
	exit()

# db = {
# "Anon": {"id": 2045634, channel: "AnotherUser", blocks: [5375652, 436432]},
# 2045634: "Anon"
#}
# Can't hash Username :(
# (It broke all)

############WORK WITH DBs##########

def read_db():
        global db
        with open('db.json', 'r') as openfile:
                db = json.load(openfile)
def write_db():
        global db
        js = json.dumps(db, indent=2)
        with open("db.json", "w") as outfile:
                outfile.write(js)

################ TOKEN INIT ######

read_db()
bot = telebot.TeleBot(db['token'])

##################CATCH ERRORS####

import logging
import traceback

from io import StringIO # For catch log to variable

# Basic init
global log_stream
log_stream = StringIO()
logging.basicConfig(stream=log_stream)

def catch_error(message, err_type = None):
	try:
		if not err_type:
			global log_stream

			logging.error(traceback.format_exc()) # Log error
			err = log_stream.getvalue() # Error to variable

			bot.reply_to(message, "Critical error:\n\n" + telebot.formatting.hcode(err), parse_mode='HTML')

			log_stream.truncate(0) # Clear
			log_stream.seek(0) # Clear
	except:
		pass

def is_auth(message):
	try:
		global db
		read_db()
		if str(message.chat.id) in db:
			return True
		else:
			bot.reply_to(message,"Извините, но Вы не авторизованы.")
			return False
	except:
		catch_error(message)

############## MAIN

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, f"""Приветствую, это бот для анонимного общения.
Главное - выполняет свою функцию без рекламы, без платы и  без слежки.

Для начала зарегистрируйся:
/reg ЛюбойНикнейм
Установка адресата - :НикАдресата

Исходный код: https://gitea.gulyaipole.fun/justuser/just_anonchat
Связь с админом: { telebot.formatting.hcode(":justuser") }

Ещё проекты: @just_openbots""", parse_mode="HTML")

@bot.message_handler(commands=['reg'])
def reg(message):
	try:
		global db
		read_db()
		if len(message.text.split()) == 2:
			if message.text.split()[1] in db:
				bot.reply_to(message, "Данный пользователь уже зарегистрирован.")
			elif str(message.chat.id) in db:
				bot.reply_to(message, "Вы уже зарегистрированы.")
			else:
				db[message.text.split()[1]] = {"id": message.chat.id, "channel": None, "blocks": []}
				db[message.chat.id] = message.text.split()[1]

				write_db()
				bot.reply_to(message, "Вы зарегистрировались!\nПриятного использования.")
		else:
			bot.reply_to(message, "Вы ввели не 2 аргумента, нужно: /reg ЛюбойНикнейм")
	except:
		catch_error(message)

@bot.message_handler(commands=['b'])
def b(message):
	try:
		if is_auth(message):
			global db; read_db()
			nick = db[str(message.chat.id)]
			block = message.text.split()[1]

			if block in db:
				if db[block]["id"] not in db[nick]["blocks"]:
					db[nick]["blocks"].append(db[block]["id"])
					write_db()
				bot.reply_to(message, f"Пользователь {telebot.formatting.hcode(block)} был заблокирован.",parse_mode="HTML")
			else:
				bot.reply_to(message, "Данного пользователя не существует.")
	except:
		catch_error(message)

@bot.message_handler(commands=['u'])
def u(message):
	try:
		if is_auth(message):
			global db; read_db()
			nick = db[str(message.chat.id)]
			block = message.text.split()[1]

			if db[block]["id"] in db[nick]["blocks"]:
				db[nick]["blocks"].remove(db[block]["id"])
				write_db()
			bot.reply_to(message, f"Была снята блокировка с пользователя {telebot.formatting.hcode(block)}",parse_mode="HTML")
	except:
		catch_error(message)

@bot.message_handler(commands=['nick'])
def nick(message):
	try:
		if is_auth(message):
			global db; read_db()
			new_nick=message.text.split()[1]
			old_nick=db[str(message.chat.id)]

			if new_nick not in db:
				db[new_nick] = db[old_nick]
				db[str(message.chat.id)] = new_nick
				del db[old_nick]
				write_db()
				bot.reply_to(message,f"Вы успешно сменили ник с {telebot.formatting.hcode(old_nick)} на {telebot.formatting.hcode(new_nick)}",parse_mode="HTML")
			else:
				bot.reply_to(message,"Данный ник уже занят")
	except:
		catch_error(message)

@bot.message_handler(commands=['me'])
def me(message):
	try:
		read_db()
		nick = db[str(message.chat.id)]
		channel = db[nick]["channel"]
		if not channel:
			channel = "Не задан."

		bot.reply_to(message, f"""Ваш ник: {telebot.formatting.hcode(nick)}
Заданный канал: {telebot.formatting.hcode(channel)}""",parse_mode="HTML")
	except:
		catch_error(message)


@bot.message_handler(func=lambda message: True)
def catch_all_messages(message):
	try:
		global db
		read_db()
		nick = db[str(message.chat.id)]
		if message.text[:1].lower() == ":":
			channel = message.text[1:]
			if channel in db:
				db[nick]["channel"] = channel
				bot.reply_to(message, "Установлен адресат: " + telebot.formatting.hcode(channel), parse_mode="HTML")
				write_db()
			else:
				bot.reply_to(message, "Не существует данного пользователя.")
		elif db[nick]["channel"] != None:
			channel = db[nick]["channel"]

			if message.chat.id not in db[channel]["blocks"]:
				try:
					bot.send_message(db[channel]["id"], f"{telebot.formatting.hcode(nick)}\n" + message.text, parse_mode="HTML")
				except:
					bot.reply_to(message, "Сообщение не было доставлено.\nВероятно пользователь заблокировал бота.")
			else:
				bot.reply_to(message, "Увы, но вас заблокировал данный пользователь.")
		else:
			bot.reply_to(message, f"У вас не указан чат.\nЧтобы подключится к чату напишите: {telebot.formatting.hcode('c:Никнейм')} ", parse_mode="HTML")
	except:
		catch_error(message)

#### POLLING ####
'''
while True:
	try:
		bot.polling()
	except KeyboardInterrupt:
		exit()
	except:
		pass
'''
bot.polling()
