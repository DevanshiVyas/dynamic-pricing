from scipy.stats import bernoulli
import db as d
import json
import ast
import time
from datetime import datetime
import rethinkdb as r


timezone=time.strftime("%z")
tz=r.make_timezone(timezone[:3] + ":" + timezone[3:])
Date=datetime.now(tz)
timestamp=time.mktime(Date.timetuple())
json_date=Date.isoformat()

def to_JSON(object):
        return json.dumps(object, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)

class bids:
    # cur
    # tot
    total=0

    'Common base class for all bids'
   

    def __init__(self, cur, tot,id):
        self.cur = cur
        self.tot = tot
        self.id=id
        self.created_at=0
        self.updated_at=0
        bids.total += 1
   
    def displayCurrent(self):
        print "Current number of bids %d" % self.cur

    def displayTotBids(self):
        print "Total number of allowed bids %d" % self.tot

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)


class inventory:
    # cur 
    # maxi
    # t0
    total=0

    'Common base class for all inventory'


    def __init__(self, cur, maxi,t0,id):
        self.id=id
        self.cur = cur
        self.maxi = maxi
        self.t0 = t0
        self.created_at=0
        self.updated_at=0
        inventory.total += 1
       
    def displayCurrent(self):
        print "Current inventory %d" % self.cur

    def displayMax(self):
        print "Maximum inventory %d" % self.maxi

    def displayt0(self):
        print "Inventory at t0 %d" % self.t0

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)


class revenue:
    # dp
    # cp
    total=0


    'Common base class for all revenue'


    def __init__(self, dp, cp,id):
        self.dp = dp
        self.cp = cp
        self.id=id
        self.created_at=0
        self.updated_at=0
        revenue.total += 1

    def displayCurrent(self):
        print "Revenue generated from dynamic pricing strategy %d" % self.dp
    
    def display(self):
        print "Revenue generated from dynamic pricing strategy %d" % self.dp

    def displayMax(self):
        print "Revenue generated from classic pricing strategy %d" % self.cp

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)

    def getTime(self):
        time = r.epoch_time((self.updated_at['epoch_time'])).run()
        return time


class price:
    # cost
    # bid_min
    # bid_max
    # selling
    

    'Common base class for all price'

    def __init__(self, cost, bid_min,bid_max,selling,id):
        self.cost = cost
        self.bid_min = bid_min
        self.bid_max = bid_max
        self.created_at=0
        self.updated_at=0        
        self.selling = selling
        self.id=id
        #price.empCount += 1
       
    def displayCostprice(self):
        print "Cost Price %d" % self.cost
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
         sort_keys=True, indent=4)


class product:
    id=1

    'Common base class for all bids'
   

    def __init__(self):
        self.inventory=inventory(0,0,0,product.id)
        self.revenue=revenue(120,70,product.id)
        self.price=price(0,0,0,0,product.id)
        self.bids=bids(0,0,product.id)
        # timezone=time.strftime("%z")
        # tz=r.make_timezone(timezone[:3] + ":" + timezone[3:])
        # Date=datetime.now(tz)
        # timestamp=time.mktime(Date.timetuple())
        # json_date=Date.isoformat()
        #self.timestamp=timestamp
        self.created_at=0
        self.updated_at=0
        product.id += 1

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)



def selection(inventory,revenue):
    "Takes in the item and time and checks its corresponding inventory"
    
    if(inventory.cur<inventory.maxi):
        decision=0
        number_items_dp=0

    else:# add item to selection with some probability 
        
        # Commpute the probability 
        prob=(float)(revenue.dp/(revenue.dp+revenue.cp))
            
        # make a Bernoulli draw with probability "prob"
        decision=bernoulli.rvs(prob,loc=0,size=1) # part of scipy
        number_items_dp=inventory.cur-inventory.maxi
        
    
    return (decision,number_items_dp)


def pricing_range(item,profit_margin,inventory,price):
    
    alpha_control = 0.4# SET some value between (0,1)
    market_trend = price.cost*(bids.cur/bids.tot)
    
    price.bid_min=price.cost+market_trend
    price.bid_max=(1+profit_margin/100)*price.bid_min
    return  

def compute():
    
    # inventory={'curr':0,'max':0,'t0':0}
    # #revenue={}
    # #price={}
    # #bids={}
    # revenue = {'dp':0 ,'cp':0 }
    # price = {'cost':0, 'bid_min':0,'bid_max':0,'selling':0}
    # bids = {'curr':0,'tot':0}

        
    # inventory=inventory(0,0,0)
    # revenue=revenue(120,70)
    # price=price(0,0,0,0)
    # bids=bids(0,0)
    p=product()

    p.inventory.cur=370       # call to database to get inventory for this product at this time
    p.inventory.maxi=150      # call to database to get max inventory capacity of this product
    
    p.revenue.dp=120           # call to databse to get revenue under dynamic pricing for this product
    p.revenue.cp=70         # call to databse to get revenue under regular pricing for this product
    p.price.cost=900         # call to database to get cost price of this item
    
    p.bids.cur=0         # call to database for number of bids made so far for this item
    p.bids.tot=2# call to database for total number of bids made
    
    p.inventory.t0=50# call to database to get inventory for this item at the beginning of the day
    
    decision,number_items_dp=selection(p.inventory,p.revenue)
    
    #price.bid_min, price.bid_max = pricing_range(item, profit_margin, customer_loyality)

    #print (decision[0],number_items_dp)

    #t=d.table_create('test1','DP')
    #d.insert(t,inventory.to_JSON(),revenue.to_JSON(),price.to_JSON(),bids.to_JSON(),decision,number_items_dp)
    
    
    #Inserting into the db
    
    # print d.insert('test1','revenue',p.revenue.to_JSON())
    # print d.insert('test1','price',p.price.to_JSON())
    # print d.insert('test1','bids',p.bids.to_JSON())
    #print d.insert('test1','product',p.to_JSON())    
   
    #Update
    #print d.replace('test1','inventory',p.inventory.to_JSON(),p.id-1)

    #update with time
    #print d.update_with_date('test1','revenue',p.revenue.to_JSON(),1)    
    
    #retrieving data
    #q=product()
    #print q.revenue.to_JSON()
    #w=revenue(0,0,0)
    q=type('revenue', (object,), json.loads(d.display('test1','revenue',1)))
    #q.revenue=type('revenue()', (revenue(0,0,0),), json.loads(d.display('test1','revenue',1)))
    
    #Display time
    #print r.epoch_time((q.updated_at['epoch_time'])).run()
    
    return
compute()    

    


