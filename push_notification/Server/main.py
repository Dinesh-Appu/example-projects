# system package
import sys


# Custom Package
from package.OpenNotify import Server, MessageModel 


class Message(MessageModel):

	id:str
	to_id:str
	body:str
	icon:str

ip = '127.0.0.1'
port = 200

server = Server(ip, port)

server.setModel(Message)
#server.generateID('PushNoti')
server.start()

