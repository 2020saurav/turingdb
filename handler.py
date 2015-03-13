import socket
import sys
import time
s = socket.socket()
s.bind(("",8182))
s.listen(10)

while True:
	sc, address = s.accept()
	print address
	query = sc.recv(1024)
	query = query.split(" ")
	if query[0]=="INSERT":
		print "Query to insert",query[1],"key"
		sc.send("Your query is under process")
		# do computations
		time.sleep(1)
		# send back result
		sc.send("Inserted")
	else:
		print "Unknown Query"
	sc.close()
s.close()