import csv,re, sqlite3 , os ,ast  # pymongo
import csv
# client = pymongo.MongoClient()
# db = client['datastore-db']
# books = db.books



# assumes database is created...

def format_file(filename):

	DATABASE_DIR = str(os.path.abspath(os.getcwd()))

	# building sqlite pipe
	conn = sqlite3.connect(DATABASE_DIR + '/database')
	cursor = conn.cursor()

	conn.row_factory = sqlite3.Row
	conn.text_factory = str
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	course_id = 1
	book_id = 1
	counter = 0

	with open(BASE_DIR + "/" + filename, 'r', encoding='mac_roman', newline='') as f:
		reader =csv.DictReader(f)
		for row in reader:
			#if counter == 5:
			#	break

			author = row['author']

			if( author == "" or author =="Author" or re.search(r"^[^0-9a-zA-Z]*$",author) is not None):
				continue

			title = row['title']
			isbn = row['isbn']
			dept_course = [ row['dept_course'] ]
			# section = row[4]

			#### Book checking ####
			# book checking
			isbn = re.sub(r"[^0-9]*" , "" , isbn)
			cursor.execute(''' SELECT COUNT(*) from book_info where isbn = ? ''' , (isbn,) )
			(number_of_rows,)=cursor.fetchone()

			# book not found
			if number_of_rows == 0:
				cursor.execute(''' insert into book_info(id , isbn , title, author ,dept_course) values (? , ? , ? ,? ,?)''' , (book_id , isbn , title , author , str(dept_course) ))
				book_id += 1
			# book found
			else:
				dept_course_db= cursor.execute('''select * from book_info where isbn = ?; ''' , (isbn, )).fetchone()
				try:

					temp = ast.literal_eval(dept_course_db[4])
					if dept_course[0] not in temp:
						temp.append(dept_course[0])
					cursor.execute('''update book_info set dept_course = ? where isbn = ?;''' , (str(temp), isbn,))
				except Exception as e:
					eval(input(e))
					eval(input(dept_course_db))

			#### Course checking ####
			cursor.execute(''' SELECT COUNT(*) from class_info where dept_course = ? ''' , (dept_course[0],) )
			(number_of_rows,)=cursor.fetchone()

			# course not found
			if number_of_rows == 0:
				cursor.execute(''' insert into class_info(id , dept_course , associated_books) values (? , ? , ?)''' , (course_id , dept_course[0] , str([ (title,isbn) ]) ))
				course_id += 1
			# course found
			else:
				dept_course_db= cursor.execute('''select * from class_info where dept_course = ?; ''' , (dept_course[0], )).fetchone()
				try:

					temp = ast.literal_eval(dept_course_db[2])
					if (title,isbn) not in temp:
						temp.append((title,isbn))
					cursor.execute('''update class_info set associated_books = ? where dept_course = ?;''' , (str(temp), dept_course[0],))
				except Exception as e:
					eval(input(e))
					eval(input(dept_course_db))
			counter += 1

		conn.commit()



