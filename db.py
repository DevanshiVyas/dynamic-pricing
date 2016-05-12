import rethinkdb as r
import ast
import time
import json
from datetime import datetime
import random


timezone=time.strftime("%z")
tz=r.make_timezone(timezone[:3] + ":" + timezone[3:])
Date=datetime.now(tz)
timestamp=time.mktime(Date.timetuple())
json_date=Date.isoformat()



r.connect('localhost', 28015).repl()

def table_create(db_name,tbl_name):
	r.db(db_name).table_create(tbl_name,primary_key='id').run()
	return r.db(db_name).table(tbl_name)

def table_return(db_name,tbl_name):
	return r.db(db_name).table(tbl_name)

#def insert(t,inventory,revenue,price,bids,decision,no_of_items):
def insert(db_name,tbl_name,obj):
	#return t.insert({ast.literal_eval(inventory)},{ast.literal_eval(revenue)},{ast.literal_eval(price)},{ast.literal_eval(bids)}).run()	
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.insert(ast.literal_eval(obj)).run()	
	
	
def replace(db_name,tbl_name,obj,key):
	#print r.db(db_name).table_list().contains(tbl_name).run()
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.get(key).replace(ast.literal_eval(obj)).run()	

#deleting an entry with primary key
def delete(db_name,tbl_name,obj,key):
	#print r.db(db_name).table_list().contains(tbl_name).run()
	if (r.db(db_name).table_list().contains(tbl_name).run()):
		t=table_return(db_name,tbl_name)
	else:
		t=table_create(db_name,tbl_name)

	return t.get(key).replace(None).run()	

def display(db_name,tbl_name,key):
	#return r.db(db_name).table(tbl_name).get(key).run()
	return r.db(db_name).table(tbl_name).get(key).coerce_to('string').run()

def displayTime(db_name,tbl_name,key):
	#return r.db(db_name).table(tbl_name).get(key).run()
	return r.db(db_name).table(tbl_name).get(key).run()

def update_with_date(db_name,tbl_name, user_object,id):
    return r.db(db_name).table(tbl_name).get(id).replace(
        lambda doc: r.branch(
            (doc == None),
            doc.merge(doc).merge({'updated_at': r.now()}),
            doc.merge(doc).merge({'created_at': r.now()},{'updated_at': r.now()}))).run()

def update_with_date_random(db_name,tbl_name, user_object,id):
    return r.db(db_name).table(tbl_name).get(id).replace(
        lambda doc: r.branch(
            (doc == None),
            doc.merge(doc).merge({'created_at': r.time(random.randrange(1995,2015,1), random.randrange(1,12,1), random.randrange(1,30,1), 'Z')}),
            doc.merge(doc).merge({'created_at': r.time(random.randrange(1995,2015,1), random.randrange(1,12,1), random.randrange(1,30,1), 'Z')},{'updated_at': r.now()}))).run()


# #(doc['created_at']==0),
#         (doc['created_at']==0)
#         #r.expr(ast.literal_eval(user_object)).merge({'id': id, 'created_at': r.now()}),
#         doc.merge(doc).merge({'created_at': r.now()}),
#         doc.merge(doc).merge({'updated_at': r.now()}),)).run()