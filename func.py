#### Ловим ошибки ####
from catch_err import *
######### БД #########
from db import *
######################

# -> True/False
def is_auth(bot, message):
	try:
		db = load()
		if str(message.chat.id) in db:
			return True
		else:
			bot.reply_to(message,"Извините, но Вы не авторизованы.\n\n/reg ник")
			return False
	except:
		catch_error(bot, message)


# Регулярные выражения
from re import sub, compile
# -> True/False
def nick_ok(bot, message, nick):
	try:
		if len(nick) > 30:
			bot.reply_to(message,"Слишком длинный ник, попробуйте короче.")
			return False
		if is_num(nick):
			bot.reply_to(message,"Ник должен содержать хоть 1 букву, попробуйте ещё раз.")
			return False

		en = True
		ru = True
		# Если только английский
		regex = compile('[^a-zA-Z0-9]')
		check = regex.sub('', nick)
		if check != nick:
			en = False
		# Если только русский
		regex = compile('[^а-яА-ЯЁё0-9]')
		check = regex.sub('', nick)
		if check != nick:
			ru = False

		if en == False and ru == False:
			bot.reply_to(message,"Нельзя смешивать алфавиты и ставить спец.-символы, попробуйте ещё раз")
			return False

		return True
	except:
		catch_error(bot, message)

# Проверяем совпадение ключей при отправке сообщений
# -> True/False
def key_valid(bot, message, channel):
	try:
		db = load()
		our_nick = db[str(message.chat.id)]
		user = db[our_nick]
		# Добавляем ключ если его нету в нашей БД
		if channel not in user.keys:
			user.keys[channel] = db[channel].pkey
			save(db)
			return True

		our_key = user.keys[channel]
		dest_key = db[channel].pkey

		if our_key == dest_key:
			return True
		else:
			user.keys[channel] = dest_key
			save(db)

			bot.reply_to(message, f"""⚠️ Публичные ключи не совпадают ⚠️
Ожидаемый ключ: {telebot.formatting.hcode(our_key)}

Отправка сообщения отклонена.
Если вы уверены - повторите отправку.
""", parse_mode="HTML")
			return False
	except:
		catch_error(bot, message)


# Проверка на количество аргументов
# ok_args(bot, message, 2, '/nick никнейм') + '/nick test' = True
def ok_args(bot, message, count, mess):
	try:
		count_args = len(message.text.split())
		if not count_args == count:
			bot.reply_to(message, mess, parse_mode="Markdown")
			return False
		else:
			return True
	except:
		catch_error(bot, message)
