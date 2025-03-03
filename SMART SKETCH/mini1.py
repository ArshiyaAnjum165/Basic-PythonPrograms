from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import gridfs
from bson import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
db = client["house_design_db"]
users_collection = db["users"]
designs_collection = db["designs"]
fs = gridfs.GridFS(db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials, please try again."

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/designs')
def get_designs():
    designs = list(designs_collection.find())
    return jsonify(designs)

@app.route('/save_design', methods=['POST'])
def save_design():
    design_name = request.form['design_name']
    design_data = request.files['design_image'].read()
    
    # Save image in GridFS
    file_id = fs.put(design_data, filename=design_name)
    
    # Save design details in MongoDB
    designs_collection.insert_one({
        "name": design_name,
        "image_id": file_id,
    })
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
