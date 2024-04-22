import telebot
import os
import json
from icecream import ic

########### Функции ##############
from func import *

########### Работа с БД ##########
from db import *
raw_db = read_db()

###### Класс пользователя ########
from user import *
# user.id = 123
# user.pkey = "fd35s"
# user.channel = "anotheruser"
# user.avatar = "♿️"
# user.blocks = [124235]
# user.keys = {"anotheruser": "re543"}

####### Работа с хэшем ###########
from hash import hash
from random import randint

##### Инициализация токена #######
bot = telebot.TeleBot(raw_db['token'])

########## Ловим ошибки ##########
from catch_err import *


############## MAIN ##############

@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.reply_to(message, f"""Приветствую, это бот для анонимного общения.
Главное - выполняет свою функцию без рекламы, без платы и  без слежки.

Для начала зарегистрируйся:
/reg ЛюбойНикнейм
Установка адресата - { telebot.formatting.hcode(":НикАдресата") }

Исходный код: https://gitea.404.mn/justuser/just_anonchat
Связь с админом: { telebot.formatting.hcode(":justuser") }

Ещё проекты: @just_openbots""", parse_mode="HTML")

@bot.message_handler(commands=['reg'])
def reg(message):
	try:
		db = load()
		if len(message.text.split()) == 2:
			nick = message.text.split()[1]
			# Проверка ника
			if not nick_ok(bot, message, nick):
				return 0
			if nick in db:
				bot.reply_to(message, "Данный пользователь уже зарегистрирован.")
			elif str(message.chat.id) in db:
				bot.reply_to(message, "Вы уже зарегистрированы.")
			else:
				user = user_(message.chat.id, hash(randint(74287, 5747962)))
				db[nick] = user
				db[message.chat.id] = nick

				save(db)
				bot.reply_to(message, "Вы зарегистрировались!\nПриятного использования.")
		else:
			bot.reply_to(message, "Вы ввели не 2 аргумента, нужно: /reg ЛюбойНикнейм")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['b'])
def b(message):
	try:
		if is_auth(bot, message):
			db = load()
			nick = db[str(message.chat.id)]
			user = db[nick]
			block = message.text.split()[1]

			# Block by ":user"
			if block[0] == ":":
				block = block[1:]

			if block in db:
				if db[block].id not in user.blocks:
					user.blocks.append(db[block].id)
					save(db)
				bot.reply_to(message, f"Пользователь {telebot.formatting.hcode(block)} был заблокирован.",parse_mode="HTML")
			else:
				bot.reply_to(message, "Данного пользователя не существует.")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['u'])
def u(message):
	try:
		if is_auth(bot, message):
			db = load()
			nick = db[str(message.chat.id)]
			user = db[nick]
			block = message.text.split()[1]

			# Unblock by ":user"
			if block[0] == ":":
				block = block[1:]

			if db[block].id in user.blocks:
				user.blocks.remove(db[block].id)
				save(db)
			bot.reply_to(message, f"Была снята блокировка с пользователя {telebot.formatting.hcode(block)}",parse_mode="HTML")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['nick'])
def nick(message):
	try:
		if is_auth(bot, message):
			db = load()
			new_nick = message.text.split()[1]
			# Проверка ника
			if not nick_ok(message, new_nick):
				return 0
			old_nick = db[str(message.chat.id)]

			if new_nick not in db:
				db[new_nick] = db[old_nick]
				db[new_nick].avatar = "♿️"
				db[str(message.chat.id)] = new_nick
				del db[old_nick]
				save(db)
				bot.reply_to(message,f"Вы успешно сменили ник с {telebot.formatting.hcode(old_nick)} на {telebot.formatting.hcode(new_nick)}",parse_mode="HTML")
				bot.reply_to(message, """Ваша аватарка сброшена до стандартной: ♿️
Также вы можете сбросить публичный ключ: /key_res""")
			else:
				bot.reply_to(message,"Данный ник уже занят")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['av'])
def av(message):
	try:
		if is_auth(bot, message):
			db = load()
			if not len(message.text.split()) > 1:
				bot.reply_to(message,"Укажите аватарку")
				return 0
			new_avatar = message.text.split()[1]
			if len(new_avatar) > 10:
				bot.reply_to(message,"Слишком большое количество символов для аватарки")
			else:
				nick = db[str(message.chat.id)]
				db[nick].avatar = new_avatar
				save(db)
				bot.reply_to(message,"Новая аватарка успешно установлена")
	except:
		catch_error(bot, message)

######### Работа с ключом ########

@bot.message_handler(commands=['key'])
def key(message):
	try:
		if len(message.text.split()) == 2:
			db = load()
			nick = message.text.split()[1]
			if nick[0] == ':':
				nick = nick[1:]
			key = db[nick].pkey
			bot.reply_to(message,f"Ключ пользователя: {telebot.formatting.hcode(key)}", parse_mode="HTML")
		else:
			bot.reply_to(message,"/key ник")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['ver'])
def ver(message):
	try:
		if len(message.text.split()) == 3:
			db = load()
			nick = message.text.split()[1]
			if nick[0] == ':':
				nick = nick[1:]
			key = message.text.split()[2]
			if not nick in db:
				bot.reply_to(message,"Не существует такого пользователя")
				return 0

			if key == db[nick].pkey:
				bot.reply_to(message,"✅ Ключи совпадают")
			else:
				bot.reply_to(message,"❌ Ключи не совпадают")
		else:
			bot.reply_to(message,"/ver ник ключ")
	except:
		catch_error(bot, message)

@bot.message_handler(commands=['key_res'])
def key_res(message):
	try:
		if is_auth(bot, message):
			db = load()

			key = hash(randint(74287, 5747962))
			nick = db[str(message.chat.id)]
			old_key = db[nick].pkey

			db[nick].pkey = key
			save(db)

			bot.reply_to(message,f"""🔑 Ключ успешно сброшен.

Старый ключ: {telebot.formatting.hcode(old_key)}
Новый ключ: {telebot.formatting.hcode(key)}""",parse_mode="HTML")
	except:
		catch_error(bot, message)


##################################

@bot.message_handler(commands=['me'])
def me(message):
	try:
		if is_auth(bot, message):
			db = load()
			nick = db[str(message.chat.id)]
			user = db[nick]
			ch = user.channel
			if not user.channel:
				ch = "Не задан."

			bot.reply_to(message, f"""Заданный канал: {telebot.formatting.hcode(ch)}

Ваш ник: {telebot.formatting.hcode(nick)}
Ваша аватарка: {telebot.formatting.hcode(user.avatar)}
Ваш публичный ключ: {telebot.formatting.hcode(user.pkey)}""",parse_mode="HTML")
	except:
		catch_error(bot, message)


###### Передача сообщений ########

@bot.message_handler(func=lambda message: True, content_types=['photo','text', 'document', 'voice', 'video'])
def catch_all_messages(message):
	try:
		db = load()
		nick = db[str(message.chat.id)]
		user = db[nick]
		avatar = ' ' + user.avatar
		if message.content_type == "text" and message.text[:1].lower() == ":":
			channel = message.text[1:]
			if channel in db:
				# Проверяем ключи
				if not key_valid(bot, message, channel):
					return 0

				user.channel = channel
				bot.reply_to(message, "Установлен адресат: " + telebot.formatting.hcode(channel), parse_mode="HTML")
				save(db)
			else:
				bot.reply_to(message, "Не существует данного пользователя.")
		elif user.channel != None:
			channel = user.channel
			# Проверяем ключи
			if not key_valid(bot, message, channel):
				return 0
			db = load()

			if message.chat.id not in db[channel].blocks:
				try:
					# Check if image
					if "photo" in message.json:
						img_id = message.json['photo'][0]['file_id']
						# Catch caption
						if "caption" in message.json:
							caption = "\n" + message.json['caption']
						else:
							caption = ""

						bot.send_photo(db[channel].id, img_id, f"{telebot.formatting.hcode(':'+nick) + avatar}" + caption, parse_mode="HTML")

					elif "document" in message.json:
						doc_id = message.json['document']['file_id']
						if "caption" in message.json:
							caption = "\n" + message.json['caption']
						else:
							caption = ""
						bot.send_document(db[channel].id, doc_id, caption = f"{telebot.formatting.hcode(':'+nick) + avatar}" + caption, parse_mode="HTML")
					elif "voice" in message.json:
						voice_id = message.json['voice']['file_id']
						bot.send_document(db[channel].id, voice_id, caption = f"{telebot.formatting.hcode(':'+nick) + avatar}", parse_mode="HTML")
					elif "video" in message.json:
						vid_id = message.json['video']['file_id']
						if "caption" in message.json:
							caption = "\n" + message.json['caption']
						else:
							caption = ""
						bot.send_video(db[channel].id, vid_id, caption = f"{telebot.formatting.hcode(':'+nick) + avatar}", parse_mode="HTML")
					else:
						bot.send_message(db[channel].id, f"{telebot.formatting.hcode(':'+nick) + avatar}\n" + message.text, parse_mode="HTML")

				except:
					catch_error(bot, message)
					bot.reply_to(message, "Сообщение не было доставлено.\nВероятно пользователь заблокировал бота.")
			else:
				bot.reply_to(message, "Увы, но вас заблокировал данный пользователь.")
		else:
			bot.reply_to(message, f"У вас не указан чат.\nЧтобы подключится к чату напишите: {telebot.formatting.hcode(':Никнейм')} ", parse_mode="HTML")
	except:
		catch_error(bot, message)

#### POLLING ####
from sys import argv
if len(argv) > 1:
	mode = "debug"
else:
	mode = "normal"

if mode == "normal":
	while True:
		try:
			bot.polling()
		except KeyboardInterrupt:
			exit()
		except:
			pass
elif mode == "debug":
	ic("Started debug...")
	bot.polling()
