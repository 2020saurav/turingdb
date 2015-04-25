from sys import call

if __name__=="__main__":
	n = input("Number of Data Servers: ")
	path = raw_input("Directory to deploy simulated DBPT: ")
	for i in range(1, n):
		pass
	# TODO 
	# 1. create needed directories : central, s01, s02, ...
	# 2. central : put central/* into this
	# 3. s.. : put bpt, client, handler, servermap there
	# 4. bpt : change line number 3 for each server
	# 5. handlers/clients : server ids change and port informations
	# 6. update port/ip/score etc info in servermap
	# dataserver servermaps have one extra entry about central server.
	# ^ can sync with central by putting storage limit of central as 0