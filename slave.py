#!/usr/bin/python
import argparse
import zmq
import urllib2
import sqlite3
#import msgpack
conn = sqlite3.connect('prueba.db')
import cPickle

parser = argparse.ArgumentParser(description='zeromq cliente/servidor')
parser.add_argument('--bar')
args = parser.parse_args()
if args.bar:
    # cliente
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://compute-0-1:5555')
    socket.send(args.bar)
    msg = cPickle.loads(socket.recv())
    c = conn.cursor()
    
    query = 'INSERT INTO stocks (symbol, last, date, change, high, low, vol, send) VALUES (:symbol, :last, :date, :change, :high, :low, :vol, 1);'
    
    #query = 'INSERT INTO stocks (%s) VALUES (%s)' % (columns, placeholders)
    
    # Insert a row of data
    c.execute(query, msg)  
    c.execute('SELECT * FROM stocks')
    print c.fetchall()
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
else:
    # servidor
    def getYahooStockQuote(symbol):
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1c1hgv" % symbol
        f = urllib2.urlopen(url)
        s = f.read()
        f.close()
        s = s.strip()
        L = s.split(',')
        D = {}
        D['symbol'] = L[0].replace('"','')
        D['last'] = L[1]
        D['date'] = L[2]
        D['change'] = L[3]
        D['high'] = L[4]
        D['low'] = L[5]
        D['vol'] = L[6]
        return D

    #print getYahooStockQuote('GOOG')
    
    valores=getYahooStockQuote('GOOG')
    
    c = conn.cursor()
    
    query = 'INSERT INTO stocks (symbol, last, date, change, high, low, vol, send) VALUES (:symbol, :last, :date, :change, :high, :low, :vol, 0);'
    
    #query = 'INSERT INTO stocks (%s) VALUES (%s)' % (columns, placeholders)
    print query
    
    # Insert a row of data
    c.execute(query, valores)
    
    c.execute('SELECT * FROM stocks')
    print c.fetchall()
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://0.0.0.0:5555')
    
    while True:
        msg = socket.recv()
        if msg == 'zeromq':
            packed = cPickle.dumps(valores)
            socket.send(packed)
        else:
            socket.send('...prueba de nuevo')
