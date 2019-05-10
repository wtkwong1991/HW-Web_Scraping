from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.produce


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars_dict = list(db.collection.find())
    print(mars_dict)

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_dict=mars_dict)



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
