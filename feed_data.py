from scipy.stats import bernoulli
import db as d
import json
import ast
import time
import random
from datetime import datetime
import rethinkdb as r
from main import product as product

r.db_create('test3').run()

timezone=time.strftime("%z")
tz=r.make_timezone(timezone[:3] + ":" + timezone[3:])
Date=datetime.now(tz)
timestamp=time.mktime(Date.timetuple())
json_date=Date.isoformat()


def compute():

    for x in xrange(200):

        p=product()
        
        random.normalvariate(random.randrange(500,1050,100),random.randrange(50,105,10))

        # call to database to get inventory for this product at this time
        p.inventory.cur=random.randrange(random.randrange(1+(x%20),10+(x%20),2),random.randrange(22+(x%20),500+(x%20),7), random.randrange(1,3,1))       
        
        # call to database to get max inventory capacity of this product
        p.inventory.maxi=random.randrange(random.randrange(1+(x%20),10+(x%20),2),random.randrange(22+(x%20),500+(x%20),7), random.randrange(1,3,1))      
        
        # call to databse to get revenue under dynamic pricing for this product
        p.revenue.dp=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))           
        
        # call to databse to get revenue under regular pricing for this product
        p.revenue.cp=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))         
        
        # call to database to get cost price of this item
        p.price.cost=random.normalvariate(random.randrange(500+(x%20),1550+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))         
        
        # call to database to get cost price of this item
        p.price.selling=random.normalvariate(random.randrange(600+(x%20),1650+(x%20),30),random.randrange(50+(x%20),105+(x%20),10))         
        
        # call to database for number of bids made so far for this item
        p.bids.cur=random.randrange(0,5)         

        # call to database for total number of bids made
        p.bids.tot=p.bids.cur+random.randrange(0,5)

        # call to database to get inventory for this item at the beginning of the day
        p.inventory.t0=p.inventory.cur + random.randrange(random.randrange(1+(x%20),10+(x%20),2),random.randrange(22+(x%20),500+(x%20),7), random.randrange(1,3,1))
        
        #Inserting into the db
    
        print d.insert('test3','revenue',p.revenue.to_JSON())
        print d.insert('test3','price',p.price.to_JSON())
        print d.insert('test3','bids',p.bids.to_JSON())
        print d.insert('test3','product',p.to_JSON())    

        print d.update_with_date_random('test3','revenue',p.revenue.to_JSON(),p.id-1)    
        print d.update_with_date_random('test3','price',p.price.to_JSON(),p.id-1)    
        print d.update_with_date_random('test3','bids',p.bids.to_JSON(),p.id-1)    
        print d.update_with_date_random('test3','product',p.to_JSON(),p.id-1)    
     
    
    return
compute()    

    


