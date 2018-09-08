import sqlite3
import csv

# set up the sqlite3 pipe
conn = sqlite3.connect('database')
cursor = conn.cursor()
conn.text_factory = str


# add the csv values to the database in book_topics
cursor.executescript('drop table if exists toc_freq;')
cursor.execute('''Create table toc_freq(id integer,title,isbn,freq);''')
with open('freq.csv' , 'rb') as f:

        dr = csv.DictReader(f)
        for entry in dr:
		
                isbn = entry['isbn']
                book_num = entry['id']
                title = entry['title']
		counts = entry['frequency']
               	cursor.execute('''insert into toc_freq values (?,?,?,?)''', (book_num,isbn, title, str(counts)) )

conn.commit()
conn.close()
