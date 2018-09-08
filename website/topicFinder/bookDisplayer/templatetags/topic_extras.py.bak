from django import template
from bookDisplayer.models import TocBookTopic, BookTopicInfo , TocFreq , BookInfo , ClassInfo
import ast 
import operator
import random


register = template.Library()

@register.filter(name = "load_topics")
def load_topics(value,topic):
	filtered_out = topic.filter(id=value.id)

	if(filtered_out):
		return filtered_out
	else:
		return ["Not found"]


@register.filter(name = "load_books")
def load_books(value, book):
	filtered_out = book.filter(topic_id = value.id)

	if(filtered_out):
		return filtered_out

	else:
		return ["Not found"]

@register.filter(name = "load_freq")
def load_freq(value , freq):
	filtered_out = freq.filter(id = value.id)

	if(filtered_out):
		freq_dict = ast.literal_eval(filtered_out.values('frequency')[0]['frequency'])
		if len(freq_dict) == 0:
			return 'Not found'
		return sorted(freq_dict.items() , key = operator.itemgetter(1) , reverse = True)

	else:
		return 'Not found'

@register.filter(name = "get_value")
def get_value(dict_temp , key):
	return dict_temp[0][key]

@register.filter(name = "get_length")
def get_length(value):
	if (value != 'Not found'):
		return len(value)
	return 0

@register.filter(name = "get_title")
def get_title(value, info):
	query = info.filter(isbn = value.isbn)
	if(len(query)):
		return query[0]
	else:
		return ""

@register.filter(name = "get_name")
def get_names(value):
	return value.dept_course

@register.filter(name = "get_associated_books")
def get_associated_books(value):
	list_of_books = ast.literal_eval(value.associated_books)
	return list_of_books

@register.filter(name = "get_book_title")
def get_book_title(value):
	return value[0]

@register.filter(name = "get_descript_topics")
def get_descript_topics(value , books):
	return books.filter(isbn = value[1])

@register.filter(name = "get_toc_topics")
def get_toc_topics(value , books):
	return books.filter(isbn = value[1])

@register.filter(name = "get_toc_topics")
def get_toc_topics(value , books):
	return books.filter(isbn = value[1])

@register.filter(name = "add_counter")
def add_counter(value):
	return value+random.randint(0,9999)