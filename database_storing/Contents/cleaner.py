''' cleaner: cleans the format of the table of contents provided '''

import re
import string


'''
	Standardizes the contents format
	The reason for the complications is to ensure uniformality.
	Alot of the formats differ and to ensure that a majority of formats work
	the regular expressions have to be somewhat complicated
	Will look into simplifying this way at a later date
'''

def clean_contents (contents):

	re.purge()

	expression = re.compile("<[\/]*[^>]*[\/]*>", re.MULTILINE) # removes all html tags
	contents = re.sub(expression,"",contents)

	expression = re.compile("[^0-9a-zA-Z]*\n" , re.MULTILINE) # remove all trailing nonalphanumeric characters
	contents = re.sub(expression, "\n", contents)

	re.purge()

	contents = contents.replace("; "  , "\n") # some time the formatting is seperated by ; so need to replace those with newlines

	expression = re.compile("^[a-zA-Z][a-zA-Z]*[^0-9a-zA-Z] " , re.MULTILINE) # remove all ch. or c.
	contents = re.sub(expression,"" , contents)

	expression = re.compile("([pP][aA][Rr][tT])*[ ]*[0-9]." , re.MULTILINE)
	contents = re.sub(expression,"",contents)

	re.purge()

	expression = re.compile("\." , re.MULTILINE) # at this point, if there are any periods, they are likely to be there to seperate chapters
	contents = re.sub(expression , "\n" , contents) # so now each chapter is on a new line

	re.purge()

	expression = re.compile(" [pP][aA][rR][tT]", re.MULTILINE)
	contents = re.sub(expression , "\n" , contents)

	expression = re.compile(" [cC][hH][aA][pP][tT][eE][rR]" , re.MULTILINE)
	contents = re.sub(expression, "\n",contents)

	re.purge()

	expression = re.compile(" [Aa][pP][pP][eE][nN][Dd][iI][xX] [a-zA-Z]:", re.MULTILINE) # replace the appendix some letter : with newlines
	contents = re.sub(expression,"\n",contents)

	expression = re.compile("^[pP][aA][rR][tT]",re.MULTILINE) # any new
	contents = re.sub(expression, "" , contents)

	re.purge()

	expression = re.compile("^[^0-9a-zA-Z]*[\s]*" , re.MULTILINE) # remove any whitespace in the beginning of each chapter
	contents = re.sub(expression , "" , contents)

	expression = re.compile("(^[A-Z ]*-[ ]*)|(^[.0-9a-zA-Z]*:)|(^[a-zA-Z]* [A-Z]*:) |((^[a-zA-Z]* [a-z]*:))" , re.MULTILINE) # remove any words like Chapter: Unit I: Unit ii: etc.
	contents = re.sub(expression , "", contents)

	re.purge()

	expression = re.compile("^[^0-9a-zA-Z]*", re.MULTILINE) # remove anything in the beginning that is no alphanumeric
	contents = re.sub(expression, "" , contents)

	expression = re.compile("^[IiVvXxLlcCdDmM]*$" , re.MULTILINE) # removes any roman numerials involved
	contents = re.sub(expression , "" , contents)

	re.purge()

	expression = re.compile("^[a-zA-Z]$" , re.MULTILINE)
	contents = re.sub(expression , "", contents)

	expression = re.compile("^[aA][pP][pP][eE][nN][dD][iI][xX] .*$" , re.MULTILINE)
	contents = re.sub(expression , "" , contents)

	return contents

