from pymongo import MongoClient
import logging
import sys

client = MongoClient()
db = client['datastore-db']
books = db.books
descript_not_found = db.descript_not_found
logging.basicConfig(filename="unfound.log" , level=logging.INFO)


def store_desc():
	num_not_found = 0
	current_number = 1
	for book in books.find():
		isbn = book['isbn']
		sys.stdout.write(str(current_number) + "/" + str(books.count())+"\r")
		sys.stdout.flush()			

		current_number += 1
		try:
			
			summary = descript.get_descript(isbn)
			
		except Exception as e:
			print("not found")
			num_not_found += 1
			not_found_id = descript_not_found.insert(book)
			logging.warning("Unable to find description for this entry: " + book['title'] + " , " + isbn +". "+ "The database id is : " + str(not_found_id))
			logging.warning("Precise error is found here: " + str(e))
			continue
		
		
		db.books.update( {"isbn" : isbn}, 
					{"$set": { "description.raw" : summary } } )

	sys.stdout.flush()
				
	print(("Found: " + str( books.count() - num_not_found )))
	print(("Not Found: " + str( num_not_found)))
	print("")
