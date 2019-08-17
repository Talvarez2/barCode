import sys
import dayDataBase

from datetime import date
from mail import enviarMail
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QAction, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QAction, QListWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QSpinBox


class CentralWidget(QWidget):
	"""
	en esta ventana esta todo lo que pasa en el centro de la interfaz
	"""

	def __init__(self, database, *args, **kwargs):
		super().__init__()
		self.database = database
		self.init_GUI()

	def init_GUI(self):
		"""
		este metodo inicializa el main widget y sus elementos
		"""
		self.labels = []
		self.buttons = []

		self.labels.append(QLabel('Codigo', self))
		self.labels.append(QLabel('total:', self))
		self.labels.append(QLabel(
		'{: <33} {: <32} {: >13} {: >54}'.format(
		' Nombre', 'Composición', 'Color', 'Precio')))
		self.labels[2].setFont(QFont("Monospace"))
		
		self.buttons.append(QPushButton('&Agregar', self))
		self.buttons.append(QPushButton('&Devolucion', self))
		self.buttons.append(QPushButton('&Borrar', self))
		self.buttons.append(QPushButton('&Fin Venta', self))
		
		self.buttons[0].clicked.connect(self.buy)
		self.buttons[1].clicked.connect(self.give_back)
		self.buttons[2].clicked.connect(self.delete)
		self.buttons[3].clicked.connect(self.end_transaction)

		self.edit = QLineEdit('', self)

		self.list = QListWidget(self)
		self.list.setFont(QFont("Monospace"))

		self.sp = QSpinBox()
		self.sp.setMinimum(1)

		"""
		Ordenamos cada cosa en su lugar
		"""

		vbox = QVBoxLayout()
		hbox = QHBoxLayout()
		hbox.addWidget(self.labels[0])
		hbox.addStretch(1)
		hbox.addWidget(self.sp)

		vbox.addLayout(hbox)

		hbox = QHBoxLayout()
		hbox.addWidget(self.edit)
		hbox.addWidget(self.buttons[0])
		
		vbox.addLayout(hbox)

		vbox.addWidget(self.labels[2])

		hbox = QHBoxLayout()
		hbox.addWidget(self.list)

		vbox_buttons = QVBoxLayout()
		vbox_buttons.addStretch(1)
		vbox_buttons.addWidget(self.buttons[1])
		vbox_buttons.addWidget(self.buttons[2])
		vbox_buttons.addWidget(self.buttons[3])

		hbox.addLayout(vbox_buttons)
		
		vbox.addLayout(hbox)

		vbox.addWidget(self.labels[1])

		"""
		seteamos el Layout
		"""
		self.setLayout(vbox)

	def delete(self):
		item = self.list.currentItem()
		row = self.list.row(item)
		self.list.takeItem(row)
		self.status_bar.emit("borrando item N°{}".format(row + 1))
		self.update_total()

	def buy(self):
		self.add_item()

	def add_item(self, buy=True):
		item = self.edit.text()  # agregar función
		"""
		agregar al total
		manejar errores
		"""
		if buy:
			sign = 1
		else:
			sign = -1
		if item in self.database:
			for i in range(self.sp.value()):
				self.list.addItem('{: <32} {: <32} {: >13} {: >54}'.format(
				str(self.database[item]['name']),
				str(self.database[item]['comp']),
				str(self.database[item]['color']), 
				str(sign * self.database[item]['price']))) 
		else:
			self.status_bar.emit("item not in database")
			print("item not in database")

		self.edit.clear()
		self.sp.setValue(1)
		self.update_total()

	def give_back(self):
		self.add_item(False)

	def end_transaction(self):
		# pop up
		if self.list.count() > 0:
			self.endTransactionPopup = endTransactionPopup(self)
			self.endTransactionPopup.setGeometry(550, 350, 100, 100)
			self.endTransactionPopup.show()
		else:
			self.status_bar.emit("list empty")

	
	def after_popup(self):
		total = 0
		items = []
		for item in range(self.list.count()):
			price = float(self.list.item(item).text()[-10:].strip())
			total += price
			if price > 0:
				items.append(('compra', self.list.item(item).text()))
			else:
				items.append(('devolució',self.list.item(item).text()))

		dayDataBase.add_transaction({'total': total, 'items': items})
		for item in range(self.list.count()):
			self.list.takeItem(0)
		self.update_total()

	def end_day(self):
		enviarMail(str(date.today()), self.redactar_mail())
		dayDataBase.reset_json()
		sys.exit()

	def redactar_mail(self):
		# Redactar el Mail
		return dayDataBase.Mail()

	def keyPressEvent(self, event):
		"""
		Este método maneja el evento que se produce al presionar las teclas.
		"""
		if event.key() == 16777220:
			self.buy()

	def update_total(self):
		total = 0
		for item in range(self.list.count()):
			total += float(self.list.item(item).text()[-10:].strip())
		self.labels[1].setText("total: {}".format(total))

	def load_status_bar(self, signal):
		"""
		este metodo recibira permitira hacer cambios al status bar
		"""
		self.status_bar = signal


class MainWindow(QMainWindow):

	"""
	Esta señal permite comunacar la bara de estados con el resto de los widgets
	en el formulario, inluido el central widget.	
	"""
	onchange_statusbar = pyqtSignal(str)

	def __init__(self, database, *args, **kwargs):
		super().__init__()
		
		"""configuramos la geometría de la ventan"""
		self.setWindowTitle('Milma Hilados')
		self.setGeometry(100, 100, 1100, 600)
		
		"""configuramos las acciones"""

		special = QAction(QIcon(None), '&Manejo Inventario', self)
		special.setStatusTip('Manejo Para gerentes')
		special.triggered.connect(self.manejo_inventario)

		exit = QAction(QIcon(None), '&Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		exit.triggered.connect(self.exit_app)

		"""Creamos la barra de menu."""
		menubar = self.menuBar()
		options = menubar.addMenu('&Opciones')  # primer menu
		options.addAction(special)
		options.addAction(exit)

		"""
		Incluimos la Barra de estado
		"""
		self.statusBar().showMessage('Listo')
		self.onchange_statusbar.connect(self.update_status_bar)

		"""
		Incluimos el central widget
		"""
		self.form = CentralWidget(database)
		self.setCentralWidget(self.form)
		self.form.load_status_bar(self.onchange_statusbar)

	def update_status_bar(self, msg):
		self.statusBar().showMessage('Updated. {}'.format(msg))

	def manejo_inventario(self):
		self.statusBar().showMessage('modificando inventario')
		clave = CodeWindow(self)
		clave.show()

	def exit_app(self):
		"""
		Agregar acciones previas a la salida de la aplicacion
		"""
		self.endDayPopup = endDayPopup(self.form)
		self.endDayPopup.setGeometry(550, 350, 100, 100)
		self.endDayPopup.show()


class CodeWindow(QDialog):

	def __init__(self, *args, **kwargs):
		"""
		Este método inicializa la ventana.
		"""
		super().__init__(*args, **kwargs)
		self.init_GUI()
	
	def init_GUI(self):
		"""
		Este método configura la interfaz y todos sus widgets,
		posterior a __init__().
		"""
		self.label = QLabel('Clave:', self)
		self.edit = QLineEdit('', self)
		self.button = QPushButton('&Ingresar', self)

		# Ajustamos la geometria de la ventana
		self.setGeometry(300, 300, 300, 100)
		self.setWindowTitle('Igrese Clave')
		
		vbox = QVBoxLayout()
		vbox.addWidget(self.label)

		hbox = QHBoxLayout()
		hbox.addWidget(self.edit)
		hbox.addWidget(self.button)

		vbox.addLayout(hbox)

		"""
		adding Layout
		"""
		self.setLayout(vbox)

class endTransactionPopup(QWidget):
	def __init__(self, parent, *args, **kargs):
		super().__init__()
		
		self.name = "Precio Final"
		
		self.parent = parent

		self.initGUI()
	
	def initGUI(self):
		self.label = QLabel(self.name, self)
		
		self.buttons = []

		self.buttons.append(QPushButton('&Volver', self))
		self.buttons.append(QPushButton('&Finalizar', self))
		
		self.buttons[0].clicked.connect(self.goBack)
		self.buttons[1].clicked.connect(self.End)

		vbox = QVBoxLayout()
		vbox.addWidget(self.label)

		hbox = QHBoxLayout()
		hbox.addWidget(self.buttons[0])
		hbox.addWidget(self.buttons[1])

		vbox.addLayout(hbox)

		"""
		adding Layout
		"""
		self.setLayout(vbox)


	def End(self):
		self.parent.after_popup()
		self.close()
	
	def goBack(self):
		self.close()

class endDayPopup(QWidget):
	def __init__(self, parent, *args, **kargs):
		super().__init__()
		
		self.name = "¿Desea cerrar elD ía?"
		
		self.parent = parent

		self.initGUI()
	
	def initGUI(self):
		self.label = QLabel(self.name, self)
		
		self.buttons = []

		self.buttons.append(QPushButton('&Si', self))
		self.buttons.append(QPushButton('&No', self))
		
		self.buttons[0].clicked.connect(self.End)
		self.buttons[1].clicked.connect(self.goBack)

		vbox = QVBoxLayout()
		vbox.addWidget(self.label)

		hbox = QHBoxLayout()
		hbox.addWidget(self.buttons[0])
		hbox.addWidget(self.buttons[1])

		vbox.addLayout(hbox)

		"""
		adding Layout
		"""
		self.setLayout(vbox)


	def End(self):
		self.parent.end_day()
		self.close()
	
	def goBack(self):
		self.close()


def init_interface(dataBase):
	app = QApplication([])
	form = MainWindow(dataBase)
	form.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	app = QApplication([])
	form = MainWindow()
	form.show()
	sys.exit(app.exec_())
