# Imports
from configparser import ConfigParser
import sqlite3
import datetime

# Read config
config = ConfigParser()
config.read("sql.cfg")
sqlpath=config['sqlconfig']['sqlpath']

class ManageDatabase:
    def __init__(self,name:str):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
    def reconnect(self,name:str):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
    def query(self,sqlquery):
        return self.cursor.execute(sqlquery)
    def query_f(self,sqlquery,data):
        return self.cursor.executemany(sqlquery,data)
    def commit(self):
        return self.connection.commit()
    def fetchall(self,sqlquery):
        return self.cursor.execute(sqlquery).fetchall()
    def disconnect(self):
        self.cursor.close()
        self.connection.close()


MD = ManageDatabase(sqlpath)

initial = """
CREATE TABLE IF NOT EXISTS users(
    username varchar(50) NOT NULL PRIMARY KEY,
    password varchar(50) NOT NULL,
    registerdate DATE NOT NULL,
    accesslvl int(1) DEFAULT 1
);
"""

initial2 = """
CREATE TABLE IF NOT EXISTS messages(
    messageid INTEGER,
    role varchar(50) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    PRIMARY KEY (messageid AUTOINCREMENT) 
);"""

MD.query(initial)
MD.query(initial2)
MD.commit()
adminexists = False
for i in MD.fetchall("SELECT username FROM users"):
    if i[0] == "admin":
        adminexists = True

def reset_messages():
    MD.query("DROP TABLE messages")
    MD.commit()

if adminexists == False:
    MD.query_f("INSERT INTO users VALUES (?, ?, ?, ?)",[("admin","admin",str(datetime.datetime.utcnow()),3)])
    MD.commit()

def add_message(message_role,message_content):
    MD.query_f("INSERT INTO messages (role,content) VALUES (?, ?)",[(message_role,message_content)])
    MD.commit()

def get_messages():
    return MD.fetchall("SELECT * FROM messages")