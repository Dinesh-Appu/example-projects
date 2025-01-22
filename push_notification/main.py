# Additional Packages
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

# system Packages
import sys
import os
import json

# Custom packages
from Server.package.OpenNotify import Client, MessageModel

# Start Time -> 21-01.2025 6.00 PM :: 9.54 PM
# Start Time -> 22-01.2025 1.30 PM :: 2.50 PM


class Message(MessageModel):

	id:str
	to_id:str 
	body:str 
	icon:str



class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		# Constant Variabels
		self.WIDTH = 500
		self.HEIGHT = 500
		self.NAME:str
		self.ID:str 
		self.TOKEN:str 
		self.TO:str = ""
		self.APPNAME:str
		self.APPID:str 
		self.IP:str = '127.0.0.1'
		self.PORT:int = 200
		self.DATAFILE = os.getcwd()+"./src/data.json"

		# Customization
		self.resize(self.WIDTH, self.HEIGHT)
		self.setStyleSheet(open('./src/style.qcc', 'r').read())
		self.setGeometry( 1200 , 200, self.WIDTH, self.HEIGHT)
		self.setMinimumHeight(self.HEIGHT-100)
		self.setMinimumWidth(self.WIDTH)


		# Main Objects
		self.client = Client(self.IP, self.PORT)
		self.login = Login(self)

		  # labels	
		self.message_label = QLabel()
		self.name_label = QLabel()

		  # line edit
		self.user_edit = QLineEdit()
		self.message_edit = QLineEdit()

		  # push button
		self.send_btn = QPushButton()

		  # layout
		self.main_layout = QVBoxLayout()
		self.top_layout = QHBoxLayout()
		self.bottom_layout = QHBoxLayout()

		self.load_data()

		self.initUI()

		if self.ID == None:
			self.login.show()
		else:
			self.startup()



	def initUI(self):
		centran_widget = QWidget()
		self.setCentralWidget(centran_widget)

		self.message_edit.setMaximumHeight(30)
		self.send_btn.setMaximumHeight(30)
		self.name_label.setMinimumWidth(180)

		self.name_label.setAlignment(Qt.AlignCenter)
		self.message_label.setAlignment(Qt.AlignTop)

		self.name_label.setText(self.ID)
		self.user_edit.setText(self.TO)

		self.name_label.setObjectName('name')

		# signal
		self.send_btn.clicked.connect(self.send_msg)
		self.message_edit.returnPressed.connect(self.send_msg)

		self.top_layout.addWidget(self.name_label)
		self.top_layout.addWidget(self.user_edit)

		self.bottom_layout.addWidget(self.message_edit)
		self.bottom_layout.addWidget(self.send_btn)

		self.main_layout.addLayout(self.top_layout)
		self.main_layout.addWidget(self.message_label)
		self.main_layout.addLayout(self.bottom_layout)

		centran_widget.setLayout(self.main_layout)


	def load_data(self) -> None:

		try:
			with open(self.DATAFILE, 'r') as file:
				data = json.load(file)
				self.NAME = data['name']
				self.ID = data['id']
				self.TOKEN = data['token']
				self.APPNAME= data['app_name']
				self.APPID = data['app_id']

		except FileNotFoundError:
			with open(self.DATAFILE, 'w') as file:
				data = {
					'name' : None,
					'id' : None,
					'token' : None,
					'app_name' : 'PushNoti',
					'app_id' : '5753ad83-2a11-4911-b865-73223849d04b'
				}

				json.dump(data, file, indent= 4)

			self.load_data()

	def load_message(self, message:Message) -> None:
		oldText = self.message_label.text()
		text = f"\n {message.id} -> {message.body}"
		self.message_label.setText(oldText+text)

	def send_msg(self) -> None:
		self.TO = self.user_edit.text()
		message = Message()

		if self.TO == "":
			print("To id None")
			return

		message.id = self.ID
		message.to_id = self.TO
		message.body = self.message_edit.text()

		#self.client.sendMessage("hi")
		self.client.sendMessage(message)


		oldText = self.message_label.text()
		text = f"\n {self.ID} -> {self.message_edit.text()}"
		self.message_label.setText(oldText+text)

		self.message_edit.setText("")


	def startup(self) -> None:

		self.client.setAppId(self.APPID)
		self.client.setAppName(self.APPNAME)
		self.client.setId(self.ID)
		self.client.setModel(Message)
		self.client.receiver.connect(self.load_message)
		
		try:
			self.client.start()
		except ConnectionRefusedError as e:
			print(e)
			sys.exit()



class Login(QDialog):

	def __init__(self, parrent):
		super().__init__()
		self.ID:str
		self.PASSWORD:str
		self.parrent = parrent
		print(self.parrent.geometry())

		self.setGeometry(1300, 400, 300, 150)
		self.setStyleSheet(open(os.getcwd()+'./src/style.qcc').read())

		self.main_layout = QGridLayout(self)
		self.id_edit = QLineEdit()
		self.Pass_edit = QLineEdit()
		self.label = QLabel("Result....")
		self.btn = QPushButton('Login')

		self.initUI()

	def initUI(self):
		#centran_widget = QWidget()
		#self.setCentralWidget(centran_widget)

		self.btn.clicked.connect(self.login)

		self.main_layout.addWidget(self.id_edit, 0,1)
		self.main_layout.addWidget(self.Pass_edit, 1, 1)
		self.main_layout.addWidget(self.btn, 2, 1)
		self.main_layout.addWidget(self.label, 2,2)


	def login(self)-> bool:
		text = self.id_edit.text()
		password = self.id_edit.text()
		text.replace(" ", "")
		password.replace(" ", "")
		if text == "":
			self.label.setText("Id is Empty")
			return False
		if password == "":
			self.label.setText("Password is Empty")
			return False
		#text = '@'+text
		self.parrent.ID = text
		self.parrent.startup()
		with open(self.parrent.DATAFILE, 'r') as file:
			data = json.load(file)
			data['id'] = text

			with open(self.parrent.DATAFILE, 'w') as f:
				json.dump(data, f, indent= 4)

		self.close()
		return True




if __name__ == "__main__":
	app = QApplication([])

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())






