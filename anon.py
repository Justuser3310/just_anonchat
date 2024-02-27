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
# "Anon": {"id": 2045634, channel: "AnotherUser", blocks: [5375652, 436432], avatar: "♿️", pkey: "fuD2d", keys: {AnotherUser: "dDH73s"}},
# 2045634: "Anon"
#}
# Невозможно хешировать айди - это всё ломает
#
# Первая строка - информация о пользователе (айди, канал, блокнутые пользователи)
# Вторая строчка - для отправки сообщения и блокировки
# keys - ключи , pkey - личный ключ

############WORK WITH DBs##########

from db import *
db = read_db()

###### WORK WITH HASHES ##########

from hash import hash
from random import randint

################ TOKEN INIT ######

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
		db = read_db()
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
Установка адресата - { telebot.formatting.hcode(":НикАдресата") }

Исходный код: https://gitea.gulyaipole.fun/justuser/just_anonchat
Связь с админом: { telebot.formatting.hcode(":justuser") }

Ещё проекты: @just_openbots""", parse_mode="HTML")

@bot.message_handler(commands=['reg'])
def reg(message):
	try:
		db = read_db()
		if len(message.text.split()) == 2:
			nick = message.text.split()[1]
			if nick in db:
				bot.reply_to(message, "Данный пользователь уже зарегистрирован.")
			elif str(message.chat.id) in db:
				bot.reply_to(message, "Вы уже зарегистрированы.")
			else:
				db[nick] = {"id": message.chat.id, "channel": None, "blocks": [], "avatar": "♿️", "pkey": hash(randint(74287, 5747962)), "keys": {}}
				db[message.chat.id] = nick

				write_db(db)
				bot.reply_to(message, "Вы зарегистрировались!\nПриятного использования.")
		else:
			bot.reply_to(message, "Вы ввели не 2 аргумента, нужно: /reg ЛюбойНикнейм")
	except:
		catch_error(message)

@bot.message_handler(commands=['b'])
def b(message):
	try:
		if is_auth(message):
			db = read_db()
			nick = db[str(message.chat.id)]
			block = message.text.split()[1]

			# Block by ":user"
			if block[0] == ":":
				block = block[1:]

			if block in db:
				if db[block]["id"] not in db[nick]["blocks"]:
					db[nick]["blocks"].append(db[block]["id"])
					write_db(db)
				bot.reply_to(message, f"Пользователь {telebot.formatting.hcode(block)} был заблокирован.",parse_mode="HTML")
			else:
				bot.reply_to(message, "Данного пользователя не существует.")
	except:
		catch_error(message)

@bot.message_handler(commands=['u'])
def u(message):
	try:
		if is_auth(message):
			db = read_db()
			nick = db[str(message.chat.id)]
			block = message.text.split()[1]

			# Unblock by ":user"
			if block[0] == ":":
				block = block[1:]

			if db[block]["id"] in db[nick]["blocks"]:
				db[nick]["blocks"].remove(db[block]["id"])
				write_db(db)
			bot.reply_to(message, f"Была снята блокировка с пользователя {telebot.formatting.hcode(block)}",parse_mode="HTML")
	except:
		catch_error(message)

@bot.message_handler(commands=['nick'])
def nick(message):
	try:
		if is_auth(message):
			db = read_db()
			new_nick = message.text.split()[1]
			old_nick = db[str(message.chat.id)]

			if new_nick not in db:
				db[new_nick] = db[old_nick]
				db[new_nick]["avatar"] = "♿️"
				db[str(message.chat.id)] = new_nick
				del db[old_nick]
				write_db(db)
				bot.reply_to(message,f"Вы успешно сменили ник с {telebot.formatting.hcode(old_nick)} на {telebot.formatting.hcode(new_nick)}",parse_mode="HTML")
				bot.reply_to(message, """Ваша аватарка сброшена до стандартной: ♿️
Также вы можете сбросить публичный ключ: /key_res""")
			else:
				bot.reply_to(message,"Данный ник уже занят")
	except:
		catch_error(message)

@bot.message_handler(commands=['av'])
def av(message):
	try:
		if is_auth(message):
			db = read_db()
			if not len(message.text.split()) > 1:
				bot.reply_to(message,"Укажите аватарку")
				return 0
			new_avatar = message.text.split()[1]
			if len(new_avatar) > 10:
				bot.reply_to(message,"Слишком большое количество символов для аватарки")
			else:
				nick = db[str(message.chat.id)]
				db[nick]["avatar"] = new_avatar
				write_db(db)
				bot.reply_to(message,"Новая аватарка успешно установлена")
	except:
		catch_error(message)


############# WORK WITH KEY ########

@bot.message_handler(commands=['key'])
def key(message):
	try:
		if len(message.text.split()) == 2:
			db = read_db()
			nick = message.text.split()[1]
			if nick[0] == ':':
				nick = nick[1:]
			key = db[nick]["pkey"]
			bot.reply_to(message,f"Ключ пользователя: {telebot.formatting.hcode(key)}", parse_mode="HTML")
		else:
			bot.reply_to(message,"/key ник")
	except:
		catch_error(message)

@bot.message_handler(commands=['ver'])
def ver(message):
	try:
		if len(message.text.split()) == 3:
			db = read_db()
			nick = message.text.split()[1]
			if nick[0] == ':':
				nick = nick[1:]
			key = message.text.split()[2]
			if not nick in db:
				bot.reply_to(message,"Не существует такого пользователя")
				return 0

			if key == db[nick]["pkey"]:
				bot.reply_to(message,"✅ Ключи совпадают")
			else:
				bot.reply_to(message,"❌ Ключи не совпадают")
		else:
			bot.reply_to(message,"/ver ник ключ")
	except:
		catch_error(message)

@bot.message_handler(commands=['key_res'])
def key_res(message):
	try:
		if is_auth(message):
			db = read_db()

			key = hash(randint(74287, 5747962))
			nick = db[str(message.chat.id)]
			old_key = db[nick]["pkey"]

			db[nick]["pkey"] = key
			write_db(db)

			bot.reply_to(message,f"""🔑 Ключ успешно сброшен.

Старый ключ: {telebot.formatting.hcode(old_key)}
Новый ключ: {telebot.formatting.hcode(key)}""",parse_mode="HTML")
	except:
		catch_error(message)

# Проверяем совпадение ключей при отправке сообщений
def key_valid(message, channel):
	try:
		db = read_db()
		our_nick = db[str(message.chat.id)]
		# Добавляем ключ если его нету в нашей БД
		if channel not in db[our_nick]["keys"]:
			db[our_nick]["keys"][channel] = db[channel]["pkey"]
			write_db(db)

		db = read_db()
		our_key = db[our_nick]["keys"][channel]
		dest_key = db[channel]["pkey"]

		if our_key == dest_key:
			print("Valid: ", channel)
			return True
		else:
			print("Not valid: ", channel)
			db[our_nick]["keys"][channel] = dest_key
			write_db(db)

			bot.reply_to(message, f"""⚠️ Публичные ключи не совпадают ⚠️
Ожидаемый ключ: {telebot.formatting.hcode(our_key)}

Отправка сообщения отклонена.
Если вы уверены - повторите отправку.
""", parse_mode="HTML")
			return False
	except:
		catch_error(message)

####################################



@bot.message_handler(commands=['me'])
def me(message):
	try:
		db = read_db()
		nick = db[str(message.chat.id)]
		channel = db[nick]["channel"]
		avatar = db[nick]["avatar"]
		pkey = db[nick]["pkey"]
		if not channel:
			channel = "Не задан."

		bot.reply_to(message, f"""Заданный канал: {telebot.formatting.hcode(channel)}

Ваш ник: {telebot.formatting.hcode(nick)}
Ваша аватарка: {telebot.formatting.hcode(avatar)}
Ваш публичный ключ: {telebot.formatting.hcode(pkey)}""",parse_mode="HTML")
	except:
		catch_error(message)



@bot.message_handler(func=lambda message: True, content_types=['photo','text', 'document', 'voice'])
def catch_all_messages(message):
	try:
		db = read_db()
		nick = db[str(message.chat.id)]
		avatar = ' ' + db[nick]["avatar"]
		if message.content_type == "text" and message.text[:1].lower() == ":":
			channel = message.text[1:]
			if channel in db:
				# Проверяем ключи
				if not key_valid(message, channel):
					return 0
				db = read_db()

				db[nick]["channel"] = channel
				bot.reply_to(message, "Установлен адресат: " + telebot.formatting.hcode(channel), parse_mode="HTML")
				write_db(db)
			else:
				bot.reply_to(message, "Не существует данного пользователя.")
		elif db[nick]["channel"] != None:
			channel = db[nick]["channel"]
			# Проверяем ключи
			if not key_valid(message, channel):
				return 0
			db = read_db()

			if message.chat.id not in db[channel]["blocks"]:
				try:
					# Check if image
					if "photo" in message.json:
						img_id = message.json['photo'][0]['file_id']
						# Catch caption
						if "caption" in message.json:
							caption = "\n" + message.json['caption']
						else:
							caption = ""

						bot.send_photo(db[channel]["id"], img_id, f"{telebot.formatting.hcode(':'+nick) + avatar}" + caption, parse_mode="HTML")

					elif "document" in message.json:
						doc_id = message.json['document']['file_id']
						if "caption" in message.json:
							caption = "\n" + message.json['caption']
						else:
							caption = ""
						bot.send_document(db[channel]["id"], doc_id, caption = f"{telebot.formatting.hcode(':'+nick) + avatar}" + caption, parse_mode="HTML")
					elif "voice" in message.json:
						voice_id = message.json['voice']['file_id']
						bot.send_document(db[channel]["id"], voice_id, caption = f"{telebot.formatting.hcode(':'+nick) + avatar}", parse_mode="HTML")
					else:
						bot.send_message(db[channel]["id"], f"{telebot.formatting.hcode(':'+nick) + avatar}\n" + message.text, parse_mode="HTML")

				except:
					bot.reply_to(message, "Сообщение не было доставлено.\nВероятно пользователь заблокировал бота.")
			else:
				bot.reply_to(message, "Увы, но вас заблокировал данный пользователь.")
		else:
			bot.reply_to(message, f"У вас не указан чат.\nЧтобы подключится к чату напишите: {telebot.formatting.hcode(':Никнейм')} ", parse_mode="HTML")
	except:
		catch_error(message)

#### POLLING ####
mode = 0
# Normal - 0, debug - 1

if mode == 0:
	while True:
		try:
			bot.polling()
		except KeyboardInterrupt:
			exit()
		except:
			pass
elif mode == 1:
	bot.polling()
