#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response

app = Flask(__name__)

products = [
    {
        'id': 1,
        'name': u'Iphone',
        'inventory': 100,
        'revenue_dp': 80,
        'costprice': 100,
        'revenue_cp': 50,
        'num_bids_item': 8,
        'num_bids_total': 7,
        'inventory': 5,
        'max_inventory': 10
    },
    {
        'id': 2,
        'name': u'Nexus',
        'inventory': 90,
        'revenue_dp': 80,
        'costprice': 100,
        'revenue_cp': 50,
        'num_bids_item': 8,
        'num_bids_total': 7,
        'inventory': 5,
        'max_inventory': 10
    }
]

#list all products - just for Blahh
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products})

#Return if customers bidding price is accepted or not: 1 accepted, 0 not accepted
@app.route('/products/bidstatus/<int:prod_id>,<int:bidding_price>,<int:loyalty_level>', methods=['GET'])
def get_bidstatus(prod_id,bidding_price,loyalty_level):
    product = [product for product in products if product['id'] == prod_id]
    #Placeholder
    #product = Dbsearch(prod_id)
    global bidstatus
    print bidding_price, loyalty_level

    Optimal_bid_price = 27
    #Placeholder
    #if Optimal_bid_price == compute_opt_bid(loyalty_level, prod_id) :
    #	return jsonify({'Bid Status': 1})
    #else:
    #	jsonify({'Bid Status': 0})

    if Optimal_bid_price == bidding_price:
    	bidstatus = 1
    else:
    	bidstatus = 0

    if len(product) == 0:
        abort(404)
    return jsonify({'Bid Status': bidstatus})

#Return payment status : 1 for success, 0 for failure
@app.route('/products/payment/<int:prod_id>,<int:cust_payment_info>,<int:bidding_price>', methods=['GET'])
def get_paymentStatus(prod_id,cust_payment_info,bidding_price):
    product = [product for product in products if product['id'] == prod_id]
    #Placeholder
    #product = Dbsearch(prod_id)
    print cust_payment_info, bidding_price

    #Placeholder
    #if(Payment_gateway(cust_payment_info,cust_bid_price)==1):
	#	UpdateDB(prod_id, cust_bid_price, 1)
	#	return jsonify({'Payment status': 1})
	#else:
	#	return jsonify({'Payment status': 0})

    if len(product) == 0:
        abort(404)
    return jsonify({'Payment status': 1})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)