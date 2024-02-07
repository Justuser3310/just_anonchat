import os
import json

if not os.path.exists('db.json'):
	db = {}
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)
	print('Created new db.json')


def read_db(file = 'db.json'):
	with open(file, "r", encoding="utf-8") as openfile:
		db = json.load(openfile)
	return db

def write_db(db, file = 'db.json'):
	js = json.dumps(db, indent=2, ensure_ascii=False)
	with open(file, "w", encoding="utf-8") as outfile:
		outfile.write(js)
