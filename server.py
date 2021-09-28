# server.py
# importing required modules
import threading , socket , smtplib , string , random , sys , os

# email login
class Mail:
	def __init__(self,mail,passwd):
		self.mail = mail
		self.passwd = passwd
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(mail,passwd)
		self.server = server
	def send(self,recv,mess):
		try:
			self.server.sendmail(self.mail,recv,mess)
			return 1
		except smtplib.SMTPRecipientsRefused :
			return 0
# creating server
class Server:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating Socket
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connections = {}
		self.email = Mail(os.getenv("MAIL"),os.getenv("MAIL_PASSWORD")) # taking mail and password from system for loggin in
		self.ip = "127.0.0.1" # Local Ip
		self.sock.bind((self.ip,8080)) # Binding connection
		self.sock.listen(1)
		print("Server Created Successfully...")
	def  handler(self,c,a):
		while True:
			data = c.recv(1024)
			for connection in self.connections:
				if connection != c:
					connection.send(data)	
			if not data:
				print(self.connections[c] + " is disconnected")
				del self.connections[c]
				c.close()
				break
	def clock():
		time.sleep(60)
		if self.token != None:
			return

	def Run(self,c,a):
		self.Id = str(c.recv(7),"utf-8")
		# Generating Random Token
		key = ''.join([random.choice(string.ascii_letters + string.digits ) for n in range(random.randint(11,15))]) 
		print(key)
		# Sending Key to user mail , if the mail in incorrect then displaying error message to the user and close the connection
		mail_sent = self.email.send(self.Id+"@rguktn.ac.in",key)
		if not mail_sent:
			c.send(bytes("Invalid mail...","utf-8"))
			c.close()
			return
		c.send(bytes("Please Check Your Mail !...","utf-8")) 
		self.token = None # initially token is empty
		i = 0 # incorrect count
		Verified = False # initially Verified in False
		# if the user enters an incorrect token 3 times then displays an error message
		while ( i < 3 ):
			self.token = str(c.recv(100),"utf-8") # receiving token from user
			if (self.token == key): # checking if the received token is the generated key or not
				c.send(bytes("Verified","utf-8")) # Sending Verified message to the user
				Verified = True 
				break # back out from loop
			c.send(bytes("Incorrect","utf-8")) # Sending Incorrect message to client
			self.token = None
			i+=1
		if (Verified == False): # If the user is not Verified(i.e token is incorrect 3 times) then close the connection.
			c.close()
			return
		# Creating Threading for taking messages from users and sending it to remaining users 
		athread = threading.Thread(target = self.handler,args = (c,a))
		athread.daemon = True # background task
		athread.start() # Starting thread
		self.connections[c] = self.Id # adding user to connectoins list
		print( self.connections[c] + " is connected.")

	def run(self):
		while True:
			c,a = self.sock.accept() # accepting connections from user
			# Creating Threading for connecting multiple users at a time.
			bthread = threading.Thread(target= self.Run,args=(c,a))	
			bthread.daemon = True # background task
			bthread.start() # Starting Thread
# Starting Server 
S = Server()
S.run()
