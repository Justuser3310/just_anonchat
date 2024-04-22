import os
import json

# Создаём БД, если её нету
if not os.path.exists('db.json'):
	db = {"token": "None"}
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)
	print('Создана БД')
	print('Введите токен db.json')
	exit()


# raw_db = {
# "Anon": {"id": 2045634, pkey: "fuD2d", channel: "AnotherUser", avatar: "♿️", blocks: [5375652, 436432], keys: {AnotherUser: "dDH73s"}},
# "2045634": "Anon"
# }
def read_db(file = 'db.json'):
	with open(file, "r", encoding="utf-8") as openfile:
		raw_db = json.load(openfile)
	return raw_db

def write_db(raw_db, file = 'db.json'):
	js = json.dumps(raw_db, indent=2, ensure_ascii=False)
	with open(file, "w", encoding="utf-8") as outfile:
		outfile.write(js)



from user import *
# db = {
# "Anon": user.*,
# "2045634": "Anon"
# }

def is_num(str):
	try:
		int(str)
		return True
	except:
		return False

def load():
	raw_db = read_db()
	db = {}
	for i in raw_db:
		if is_num(i) == True:
			db[i] = raw_db[i]
		elif "token" == i:
			db["token"] = raw_db["token"]
		else:
			id, pkey, channel, avatar, blocks, keys = raw_db[i]["id"], raw_db[i]["pkey"], raw_db[i]["channel"], raw_db[i]["avatar"], raw_db[i]["blocks"], raw_db[i]["keys"],
			user = user_(id, pkey, channel, avatar, blocks, keys)
			db[i] = user

	return db

def save(db):
	raw_db = {}
	for i in db:
		if is_num(i) == True:
			raw_db[i] = db[i]
		elif "token" == i:
			raw_db["token"] = db["token"]
		else:
			raw_db[i] = {"id": db[i].id, "pkey": db[i].pkey, "channel": db[i].channel, "avatar": db[i].avatar, "blocks": db[i].blocks, "keys": db[i].keys}
	write_db(raw_db)
