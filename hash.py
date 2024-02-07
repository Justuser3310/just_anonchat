import hashlib

def hash(string):
	string = str(string)
	hashed = hashlib.sha256(str.encode(string)).hexdigest()
	return hashed
