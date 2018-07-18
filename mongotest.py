from pymongo import MongoClient
import json, time, sys

print (__name__)

start_time = time.time()
client = MongoClient('mongodb://1.1.1.1')
print("--- %s seconds ---" % (time.time() - start_time))
db = client.sellbery
print("--- %s seconds ---" % (time.time() - start_time))
customers = db.customers
print("--- %s seconds ---" % (time.time() - start_time))
print(sys.getsizeof(customers))

CUSTs=list(customers.find({} ))
print(sys.getsizeof(CUSTs))
print("--- %s seconds ---" % (time.time() - start_time))
i=1
for user in CUSTs:
	try: 
		print(i,". email: ",user["structure"]["email"],"")
		print("Name: ",user["structure"]["name"])
		print("Date: ",user["date"],"\n")
		i +=1
	except:
		print(user["uuid"]," has no email \n") 


# #print(len(CUSTs)
# print("\n------------------------\n")
# i=1
# for user in CUSTs:
# 	if "sellbery.com"  in user["structure"]["email"] or "stepcart"  in user["structure"]["email"]  : 
# 		print(i,". email: ",user["structure"]["email"],"")
# 		print("Name: ",user["structure"]["name"],"\n")
# 		i +=1

# mapping = db.mappings

# MAPS=list(mapping.find({} ))
# j=1
# for ruls in MAPS:
# 	print(ruls["emitter"])
# 	for rul in ruls["rules"]:
# 		print(j,rul["rule"]["src"]," - ",rul["rule"]["dst"])
# 		j+=1