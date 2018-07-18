from pymongo import MongoClient
import json, time, sys

import numpy as np
import tensorflow as tf


print (__name__)

start_time = time.time()
client = MongoClient('mongodb://192.168.1.77:47017/')
print("--- %s seconds ---" % (time.time() - start_time))
db = client.sellbery
customers = db.customers

CUSTs=list(customers.find({} ))

print(sys.getsizeof(CUSTs))
print("--- %s seconds ---  users saved" % (time.time() - start_time))

mapping = db.mappings

MAPS=list(mapping.find({} ))
print("--- %s seconds ---  Mapping saved" % (time.time() - start_time))
print(MAPS)
EM=[]
SRC=[]
DST=[]

DUMP=[]

j=1
for ruls in MAPS:
	# print("-----",ruls["emitter"])
	if not ruls["emitter"] in EM:
		EM.append(ruls["emitter"])
	for rul in ruls["rules"]:
		# print(j,rul["rule"]["src"]," - ",rul["rule"]["dst"])
		DUMP.append((ruls["emitter"],rul["rule"]["src"],rul["rule"]["dst"]))
		if not rul["rule"]["src"] in SRC:
			SRC.append(rul["rule"]["src"])
		if not rul["rule"]["dst"] in DST:
			DST.append(rul["rule"]["dst"])
		j+=1

# print(EM,"\n-----\n",SRC,"\n-----\n",DST)
emitter = tf.feature_column.categorical_column_with_vocabulary_list('emitter',EM)
src = tf.feature_column.categorical_column_with_vocabulary_list('src',SRC)
dst = tf.feature_column.categorical_column_with_vocabulary_list('dst',DST)

INPUT_COLUMNS = [emitter,src]

src_string = tf.placeholder(
      shape=[None],
      dtype=tf.string,
  )

mapper = tf.parse_example(
	src_string,
	tf.feature_column.make_parse_example_spec(INPUT_COLUMNS))


dump_row = tf.placeholder(
  shape=[None],
  dtype=tf.string
)



sess = tf.Session()

W = tf.Variable([.3])
b = tf.Variable([-.3])
x = tf.placeholder(tf.float32)
linear_model = W *x + b
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(linear_model, {x:[1,2,3,2,1,0,7,7,7]}))
# print(DUMP)


# сохраняем граф по-умолчанию в переменную
# default_graph = tf.get_default_graph()
# # объявляем константу в графе по-умолчанию
# a = tf.constant(2.0, name="a")

# x = tf.Variable(initial_value=3.0, dtype=tf.float32)

# b = tf.placeholder(tf.float32, shape=[], name = "b")

# f = tf.add(tf.multiply(a,x),b)

# with tf.Session() as session:
# 	tf.global_variables_initializer().run()
# 	result_f, result_a, result_x, result_b = session.run([f,a,x,b], feed_dict={b: -5})

# 	print("f = %.1f * %.1f + %.1f = %.1f" % (result_a, result_x, result_b, result_f))
# 	print("a = %.1f" % a.eval())

# 	x = x.assign_add(1.0)
# 	print(x.eval(), f.eval(feed_dict={b: -5}))



# i=1
# for user in CUSTs:
# 	try: 
# 		print(i,". email: ",user["structure"]["email"],"")
# 		print("Name: ",user["structure"]["name"],"\n")
# 		i +=1
# 	except:
# 		print(user["uuid"]," has no email \n") 

# #print(len(CUSTs)
# print("\n------------------------\n")
# i=1
# for user in CUSTs:
# 	if "shirtee"  in user["structure"]["email"] or "CATEGORY"  in user["structure"]["email"]  : 
# 		print(i,". email: ",user["structure"]["email"],"")
# 		print("Name: ",user["structure"]["name"],"\n")
# 		i +=1
