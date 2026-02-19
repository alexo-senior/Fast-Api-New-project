import sqlite3
conn = sqlite3.connect(r'TodoApp\todosapp.db')
c = conn.cursor()
c.execute('SELECT id,title,description,priority,complete FROM todos')
print(c.fetchall())