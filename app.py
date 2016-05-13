from flask import Flask, render_template, request, redirect
app = Flask(__name__)
from datetime import datetime
from random import randrange

### HELPER METHODS ###

def get_profit_data():
	""" retrieve profit data from db """
	now = datetime.now()
	return [
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now()),
		(randrange(200, 1000), randrange(10, 60), datetime.now())
	]

def initial_dp_list():
	""" retrive product list set on DB from db """
	return [
		(10, "IPhone 5S", randrange(10, 150), randrange(300, 500)),
		(11, "Samsung Galaxy", randrange(10, 150), randrange(300, 500)),
		(12, "PlayStation 4", randrange(10, 150), randrange(300, 500)),
		(13, "XBox One", randrange(10, 150), randrange(300, 500)),
		(14, "Pebble Watch", randrange(10, 150), randrange(300, 500)),
		(15, "Apple watch", randrange(10, 150), randrange(300, 500)),
		(16, "Beats headphones", randrange(10, 150), randrange(300, 500)),
		(17, "Macbook Pro", randrange(10, 150), randrange(300, 500)),
		(18, "Alienware 4AG", randrange(10, 150), randrange(300, 500))
	]

def get_bids_data():
	""" retrieve bids data from db """
	return {
		"total": 345,
		"accepted": 133,
		"profit": 1456.33 
	}

#### ROUTES ####

@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form["username"] == "admin" and \
		request.form["password"] == "admin":
			return redirect("profits")
	return render_template("index.html")

@app.route("/profits", methods=["GET", "POST"])
def profit():
	if request.method == "POST":
		profit_margin = request.form["profit_input"]
		if not profit_margin:
			return "Error!"
		# input_profit_margin(profit_margin)
		return "Profit margin: {}. Saved! <a href='/dashboard'>Dashboard</a>".format(profit_margin)
	profit_data = get_profit_data()
	return render_template("profits.html", data=profit_data)

@app.route("/dashboard", methods=["GET", "POST"])
def recommended():
	if request.method == "POST":
		selected_ids = map(lambda x: int(x), request.form)
		print selected_ids
		# final_dp_list(selected_ids) 
		return "Your preferences have been saved! <a href='/dashboard'>Dashboard</a>" 
	products = initial_dp_list()
	return render_template("dashboard.html", data=products)
	
@app.route('/analytics')
def analytics():
	bids_data = get_bids_data()
	cust_data = [156, 51, 101]
	return render_template("analytics.html", 
							data=bids_data,
							cust_data=cust_data)

if __name__ == "__main__":
	app.run(debug=True)