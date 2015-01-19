# Servidor
from multiprocessing.connection import Listener
from array import array
address = ('localhost', 6000)
listener = Listener(address, authkey='secret password')
conn = listener.accept()
print 'connection accepted from', listener.last_accepted
while True:
    msg = conn.recv()
    if msg == 'close':
        conn.close()
        break
listener.close()
