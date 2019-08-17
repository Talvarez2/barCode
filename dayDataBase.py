import json
from datetime import datetime

def reset_json():
	dataBase = {}
	dataBase['total'] = 0
	dataBase['transactions'] = {}

	with open('dataBase.json', 'w') as outfile:
		json.dump(dataBase, outfile, indent = 4)

def read_json():
	with open('dataBase.json') as json_file:
		dataBase = json.load(json_file)
		return dataBase

def Mail():
	dataBase = read_json()
	return json.dumps(dataBase, indent = 4)

def add_transaction(transaction):
	""" this function recives a dict type transaction """
	dataBase = read_json()
	dataBase['total'] += transaction['total']
	dataBase['transactions'][str(datetime.now())] = transaction
	with open('dataBase.json', 'w') as outfile:
		json.dump(dataBase, outfile, indent = 4)


if __name__ == "__main__":
	reset_json()
	dataBase = read_json()
	print(dataBase)
	# add_transaction({'total': 1000, 'otras cosas': []})
