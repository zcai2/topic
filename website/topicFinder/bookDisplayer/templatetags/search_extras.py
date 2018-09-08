from django import template
from bookDisplayer.models import TocBookTopic, BookTopicInfo , TocFreq , BookInfo , ClassInfo
import ast 
import operator

register = template.Library()

@register.filter(name = "get_courses")
def get_courses(value,courses):
	return courses.filter(dept_course__contains = value)

@register.filter(name = "get_books")
def get_books(value):
	return ast.literal_eval(value)

@register.filter(name = "title")
def title(value):
	return value[0]

@register.filter(name = "isbn")
def isbn(value):
	return value[1]

@register.filter(name = "get_descript_topics")
def get_descript_topics(value , books):
	return books.filter(isbn = value[1])

@register.filter(name = "get_toc_topics")
def get_toc_topics(value , books):
	return books.filter(isbn = value[1])

@register.filter(name = "get_toc_topics_2")
def get_toc_topics_2(value , books):
	return books.filter(isbn = value.isbn)

@register.filter(name="get_num_books_toc")
def get_num_books_toc(value , books):
	return books.filter(isbn=value.isbn)[0].toc_topic_count

@register.filter(name="get_num_books_descript_2")
def get_num_books_descript_2(value , books):
	results = books.filter(isbn=value[1])[0].descript_topic_count
	return results

@register.filter(name="get_num_books_toc_2")
def get_num_books_toc_2(value , books):
	results = books.filter(isbn=value[1])[0].toc_topic_count
	return results

@register.filter(name="get_descript_num")
def get_descript_num(value , books):
	results = books.filter(isbn=value.isbn)[0].descript_topic_count
	return results