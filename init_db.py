#!/usr/bin/python
import sqlite3
conn = sqlite3.connect('prueba.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
           (symbol text, last real, date text, change text, high real, low real, vol real, send integer)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

