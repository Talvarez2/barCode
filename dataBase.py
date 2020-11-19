import openpyxl
import datetime

def get_database():

	database = {}
	previous_name = ""
	previous_comp = ""
	
	"""open the database"""
	excel_document = openpyxl.load_workbook('/Users/Millma/millma/barCode/InventarioMillma.xlsx', data_only=True)
	sheet = excel_document['General']
	
	"""read the database """
	for i in range(4, 1000):
		name =  sheet["D{}".format(str(i))].value
		if name == None:
			name =  sheet["C{}".format(str(i))].value
		if name == None:
			name = previous_name
		previous_name = name
		comp = sheet["E{}".format(str(i))].value
		if comp == None:
			comp = previous_comp
		previous_comp = comp
		"""saving to variable database"""
		if sheet["G{}".format(str(i))].value != None:
			color = sheet["G{}".format(str(i))].value
			price = sheet["AN{}".format(str(i))].value
			element = {'name': name, 
						'comp': comp,
						'color': color,
						'number' : i,
						'price': price}
			database[sheet["F{}".format(str(i))].value] = element
	
	return database

class dataBase():

	def __init__(self):

		self.excel_document = openpyxl.load_workbook('/Users/Millma/millma/barCode/InventarioMillma.xlsx')
		self.sheet = self.excel_document['General']

	def actualize_dataBase(self, id):
		column = self.get_column()
		cuantity = int(self.sheet[column + str(id)].value)
		self.sheet[column + str(id)] = cuantity + 1
	
	def save(self):	
		self.excel_document.save('InventarioMillma.xlsx')

	def get_column(self):
		month = datetime.datetime.today().month
		columns = {5:'T', 6:'U', 7:'V', 8:'W', 9:'X', 10:'Y', 11:'Z', 12:'AA'}
		return columns[month]

if __name__ == "__main__":
	database = get_database()
	print(database['LH AG 1'])
