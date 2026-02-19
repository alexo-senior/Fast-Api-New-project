import sqlite3
conn=sqlite3.connect('TodoApp/todosapp.db')
c=conn.cursor()
c.execute('SELECT id,username,email,hashed_password FROM Users')
print(c.fetchall())