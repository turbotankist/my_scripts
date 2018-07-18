#!/usr/bin/env python
import random, string, time
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

start_time = time.time()

class Address(object):

    def __init__(self, street, zipcode):
        self.street = street
        self.zipcode = zipcode

def main():
    print("--- %s seconds --- START" % (time.time() - start_time))
    cluster = Cluster(['192.168.1.141'], port=30054)
    session = cluster.connect()
    print("--- %s seconds ---CONNECTED" % (time.time() - start_time))
    try: 
    	session.set_keyspace('mykeyspace')   
    except:
    	session.execute(""" CREATE KEYSPACE mykeyspace
    		 WITH REPLICATION = { 
		   'class' : 'SimpleStrategy', 
		   'replication_factor' : 1 
		  };""")
    	session.set_keyspace('mykeyspace')

   # session.execute("CREATE TYPE  address (street text, zipcode int)")
   # session.execute("CREATE TABLE  users (id int PRIMARY KEY, location address)")
    cluster.register_user_type('mykeyspace', 'address', Address)
	# insert a row using an instance of Address 
    for  item  in range(10):
        ADDRR = "".join( [random.choice(string.letters) for i in xrange(10)] )
        session.execute("INSERT INTO users (id, location) VALUES (%s, %s)",
	                         (item, Address("123 Main St."+ ADDRR, random.randint(1,99999))))
	# results will include Address instances
    print("--- %s seconds ---INSERTED" % (time.time() - start_time))
    results = session.execute("SELECT * FROM users")
    for row in sorted(results, key=lambda person: person[0]):
    	print row.id, row.location.street, row.location.zipcode


if __name__ == "__main__":
    main()