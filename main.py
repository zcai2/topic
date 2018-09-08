import sqlite3 , os , time , datetime , signal , sys
from subprocess import call
from database_storing import storing_main
from lib import fill_tables
from lib import reset as purge
from lib import signals
from lib import save_model



os.chdir("./website/topicFinder")
signal.signal(signal.SIGINT , signals.signal_handler)
call( ['python' , 'manage.py' , 'runserver'] )


