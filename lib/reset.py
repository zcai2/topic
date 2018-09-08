import os , shutil

def main():
	try:
		print("\n")
		print("----------------------")
		print("Deleting database")
		os.remove("./database")
		print("Deleting datastore")
		shutil.rmtree("./topics/Datastore")
	except Exception as e:
		print("Unexpected error, please try again")
		print(("Error information : " + str(e)))


if __name__ == "__main__":
	main()
