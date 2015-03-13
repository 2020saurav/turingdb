import socket
import sys

# this file wont be there. 
#handler.py of some other server will call the handler of other
s = socket.socket()
s.connect(("172.24.128.203", 8182))
s.send("INSERT 0.04515")
response = s.recv(1024)
print response
response = s.recv(1024)
print response
s.close()