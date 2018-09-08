import sqlite3



def main():
	conn = sqlite3.connect("database")
	cursor = conn.cursor()
	print("---Filling the book topics table first---")
	query = " Select * from book_info"
	book_list = cursor.execute(query).fetchall()
	for book in book_list:
		isbn = book[1]
		descript_topics = cursor.execute('''select COUNT(*) from descript_book_topics where isbn = ?;''' , (isbn,) ).fetchone()[0]
		toc_topics = cursor.execute('''select COUNT(*) from toc_book_topics where isbn = ?;''' , (isbn,) ).fetchone()[0]
		cursor.execute('''insert into book_topic_info(id , title, isbn, descript_topic_count , toc_topic_count) values(?,?,?,?,?);''' ,
		(book[0] , book[2] , isbn, descript_topics , toc_topics))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
