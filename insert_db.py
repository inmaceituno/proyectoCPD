#!/usr/bin/python
import sqlite3
conn = sqlite3.connect('prueba.db')

c = conn.cursor()

#Create table
#c.execute('''CREATE TABLE stocks
#            (value text, send integer)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('Hola mundo2','0')")


c.execute('SELECT * FROM stocks')
print c.fetchall()

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

