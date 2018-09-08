''' retrieves the table of contents. Currently only operates by passing in the isbn number ''' 
import urllib
from bs4 import BeautifulSoup as bs
import requests
import cleaner

def get_toc( isbn ):
	
	found = False
	
	url_search = "http://www.worldcat.org/search?qt=worldcat_org_all&q=" + isbn 
	source_search = requests.get(url_search)
	table = bs(source_search.text).find("table" , {"class" , "table-results"})
	
	if(table is None): # no results were found, ie it was not found
		return None, url_search
		
	for table_row in table.find_all("tr" , {"class" , "menuElem"}):
		link = table_row.find("a")
		url_book = link.get("href")

		url_book = "http://www.worldcat.org/" + url_book
		source_book = requests.get(url_book)
		source_soup = bs(source_book.text)
		
		content_row = source_soup.find(id = "details-Nielsencontents") 
		if(content_row is None):
			content_row = source_soup.find(id = "details-contents")
			
		try:
			content = content_row.find("td")	
		except AttributeError: # continue checking the entries until all are exhausted
			
			continue
			
		
		content = cleaner.clean_contents(str(content))
		content = content.replace("\n" , " ")
		
		found = True
		break

	if(found):
		return content , url_book
		
	else: # The book was not to be found
		return "" , url_search
	print ""
