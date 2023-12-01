import json
import telebot

def read_db():
	global db
	with open('db.json', 'r') as openfile:
		db = json.load(openfile)

read_db()
bot = telebot.TeleBot(db['token'])

message = """
Отправка сообщений была реализована, подписи тоже работают.
"""

for i in db:
	if True:
		try:
			id=int(i)
		except:
			id=None

		if id != None:
			try:
#				bot.send_message(id,message,parse_mode='Markdown')
				bot.send_message(id,message)
				print("Pass ", id)
			except:
				print("Error ",id)
