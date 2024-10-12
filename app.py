
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
mongo_client = MongoClient("mongodb+srv://MitchBresette:Fn01wIVmeFasZBes@cluster0.8sk8t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


db = mongo_client["shop_db"]
products_collection = db["products"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    products_list = products_collection.find()
    products_list = list(products_list)

    # Print the products_list to see what you are retrieving
    print(products_list)

    return render_template('products.html', products=products_list)

if __name__ == '__main__':
    app.run(debug=True)