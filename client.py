# importing required modules
import threading , socket , os
class Client:
	# Creating Socket
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendmess(self): # Sending Message
		while True:
			data = input("You    : ")
			self.sock.send(bytes(self.Id.upper() +": "+ data,"utf-8"))
	def recvmess(self): # Receiving message
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			print("\b\b\b\b\b\b\b\b\b" + str(data,"utf-8") + "\n" + "You    : ",end="")
	def __init__(self):
		# Local Ip
		self.ip = "127.0.0.1"
		try:
			# Connect to Server
			self.sock.connect((self.ip,8080))
		except:
			print("Server not Established.") # If there is an error in the connection , then displaying error message
			exit(0)
		# Taking Id from user , based on Id the token is generated and send token to user mail
		self.Id = input("Id: ")
		# sending Id to server
		self.sock.send(bytes(self.Id,"utf-8"))
		# Receiving message from server
		print(str(self.sock.recv(100),"utf-8"))
		# incorrect count
		i = 1
		Verified = False
		while True: # infinite loop until the break statement
			token = input("Enter Key: ") # taking token from user which is sent to mail
			self.sock.send(bytes(token,"utf-8")) # sending token to server
			signal = str(self.sock.recv(100),"utf-8")
			if i == 3:
				break
			if (signal == "Incorrect"): # if the user enters incorrect password in 3 times.
				print("Wrong Key.Try again...")
				i += 1
				continue
			Verified = True
			break
		if Verified==False:
			print("S0rry 7ry 4g41n La73r !!!!!!!!!!!!!!!!!!!...")
			exit(0)

		print("\t\t\tLogediIn Successfully...!")
		# Creating threads
		bthread = threading.Thread(target = self.sendmess)
		bthread.daemon = True
		bthread.start()
		cthread = threading.Thread(target = self.recvmess)
		cthread.start()
# Creating Client Object
client = Client()
