from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape_info():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()
    mars = mongo.db.mars

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

