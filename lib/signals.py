import signal,sys

def signal_handler(singal , frame):
	print("\n")
	print("Exited Django server")
	input("Program ended successfully, Thank you!! (Press any key to exit)")
	sys.exit(0)

