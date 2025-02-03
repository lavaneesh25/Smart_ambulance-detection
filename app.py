from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import subprocess
import psutil
import os
import signal

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lavaneesh@2516",  # Change to your MySQL password
    database="lavandb"   # Change to your MySQL database name
)
cursor = db.cursor()

detection_process = None  # Store the running detection process

# 🚀 Vehicle Registration Endpoint
@app.route('/register', methods=['POST'])
def register_vehicle():
    data = request.json
    vehicleNumber = data['vehicleNumber']
    ownerName = data['ownerName']
    vehicleType = data['vehicleType']
    imageUrl = data['imageUrl']

    sql = "INSERT INTO vehicles (vehicleNumber, ownerName, vehicleType, imageUrl) VALUES (%s, %s, %s, %s)"
    values = (vehicleNumber, ownerName, vehicleType, imageUrl)
    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "✅ Vehicle registered successfully!"})

# 🚀 Start Detection (Runs index.py)
@app.route('/detect', methods=['GET'])
def start_detection():
    global detection_process
    if detection_process is None:
        detection_process = subprocess.Popen(["python", "index.py"])
        return jsonify({"message": "🚀 Detection started!"})
    else:
        return jsonify({"message": "⚠️ Detection is already running!"})

# ⛔ Stop Detection
@app.route('/stop_detect', methods=['GET'])
def stop_detection():
    global detection_process
    if detection_process:
        detection_process.terminate()  # Kill the process
        detection_process = None
        return jsonify({"message": "⛔ Detection stopped!"})
    return jsonify({"message": "⚠️ No detection is running!"})

if __name__ == '__main__':
    app.run(debug=True)
