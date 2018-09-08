import sqlite3 , os , shutil

def main():
	conn = sqlite3.connect("database")
	cursor = conn.cursor()

	timestamp =cursor.execute("select(timestamp) from model_info").fetchone()[0]

	if(not os.path.exists("./saved_models") ):
		os.makedirs("./saved_models")

	shutil.copy2("database" , "./saved_models/" + timestamp)

	conn.close()
	print("Model successfully saved as " + timestamp + " in the saved_models folder")


if __name__ == "__main__":
	main()
