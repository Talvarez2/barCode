from dataBase import get_database
from interface import init_interface

if __name__ == "__main__":
	print("getting database")
	database = get_database()
	print('initialising interface')
	init_interface(database)
