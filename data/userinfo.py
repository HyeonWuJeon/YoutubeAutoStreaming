import sqlite3
import simplejson as json
import datetime

conn = sqlite3.connect("C:/Users/tkawn/Desktop/section6/databases/sqlite1.db") #AutoCommit

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(id int PRIMARY KEY, name text, password text, email text)")



with open("H:/workspace/my_project/AutoYoutube/data/user.json", 'r',encoding='utf-8') as file:
    userData = []
    r = json.load(file)
    print(r)
    for users in r:
        t =  (users['name'], users['password'], users['email']) #튜플형식으로 변환
        userData.append(t)
        c.executemany("INSERT INTO users(name, password, email) VALUES(?,?,?)", tuple(userData))
        conn.commit()
