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
	if not err_type:
		global log_stream

		logging.error(traceback.format_exc()) # Log error
		err = log_stream.getvalue() # Error to variable

		bot.reply_to(message, "Critical error:\n\n" + telebot.formatting.hcode(err), parse_mode='HTML')

		log_stream.truncate(0) # Clear
		log_stream.seek(0) # Clear

############## MAIN

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, f"""Приветствую, это бот без слежки для анонимного общения.
Главное - выполняет свою функцию без рекламы и платы, без слежки.

Для начала зарегистрируйся:
/reg ЛюбойНикнейм

Исходный код: https://gitea.gulyaipole.fun/justuser/just_anonchat
Связь с админом: { telebot.formatting.hcode("c:justuser") }

Ещё проекты: @just_openbots""", parse_mode="HTML")

@bot.message_handler(commands=['reg'])
def reg(message):
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

@bot.message_handler(func=lambda message: True)
def catch_all_messages(message):
	global db
	read_db()
	nick = db[str(message.chat.id)]
	if message.text[:2] == "c:":
		channel = message.text[2:]
		if channel in db:
			db[nick]["channel"] = channel
			bot.reply_to(message, "Установлен адресат: " + telebot.formatting.hcode(channel), parse_mode="HTML")
			write_db()
		else:
			bot.reply_to(message, "Не существует данного пользователя.")
	elif db[nick]["channel"] != None:
		bot.send_message(db[nick]["id"], f"{telebot.formatting.hcode(nick)}\n" + message.text, parse_mode="HTML")
	else:
		bot.reply_to(message, f"У вас не указан чат.\nЧтобы подключится к чату напишите: {telebot.formatting.hcode('c:Никнейм')} ", parse_mode="HTML")

#### POLLING ####

bot.polling()
