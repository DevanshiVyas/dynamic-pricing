from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/index.html")

@app.route("/product")
def product():
    return render_template("product/index.html")

@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form["username"] == "admin" and request.form["password"] == "admin":
			return redirect("dashboard")

	return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)