import os
import json

if not os.path.exists('db.json'):
	db = {"token": "None"}
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)
	print('Создана БД')
	print('Введите токен db.json')
	exit()


def read_db(file = 'db.json'):
	with open(file, "r", encoding="utf-8") as openfile:
		db = json.load(openfile)
	return db

def write_db(db, file = 'db.json'):
	js = json.dumps(db, indent=2, ensure_ascii=False)
	with open(file, "w", encoding="utf-8") as outfile:
		outfile.write(js)
