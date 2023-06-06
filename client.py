# cliente.py
import socket
import json
from app import App

# Create a socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get a local machine name.
# IP server.
host = '127.0.0.1'
# Server PORT.
port = 9999

# Connection to hostname on the port.
s.connect((host, port))

# Create a App object.
clientApp = App()

# Collecting user data.
values = clientApp.collectUserData()

# Processing user data.
listData = clientApp.validateData(values)
finalData = clientApp.generateDict(listData)

# Serialising data.
# Pass the data to JSON.
data = json.dumps(finalData)

# Pass to bytes.
data = data.encode("ascii")

# Send data to server.
s.send(data)

# Recive no more than 1024 bytes.
# Pass to JSON.
response = s.recv(1024).decode()

# Pass to dict.
response = json.loads(response)

# Menu.
clientApp.menu(response)

# Close connection.
s.close()
