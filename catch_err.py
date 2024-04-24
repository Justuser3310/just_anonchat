import logging
import traceback
from io import StringIO # Для перевода лога в переменную

import telebot

# Базовая инициализация
global log_stream
log_stream = StringIO()
logging.basicConfig(stream=log_stream)

def catch_error(bot, message, err_type = None):
	try:
		if not err_type:
			global log_stream

			logging.error(traceback.format_exc()) # Логирование ошибок
			err = log_stream.getvalue() # Ошибка -> переменная

			bot.reply_to(message, 'Critical error:\n\n' + telebot.formatting.hcode(err), parse_mode='HTML')

			# Очистка логов
			log_stream.truncate(0)
			log_stream.seek(0)
		elif err_type == 'spec_symb':
			bot.reply_to(message, 'Невозможно отправить сообщение из-за специфических символов')
	except:
		pass
