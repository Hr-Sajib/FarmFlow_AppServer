from flask import Flask, jsonify
import random
import time
import paho.mqtt.client as mqtt
from threading import Thread
import certifi  # Import certifi for CA certificates
from dotenv import load_dotenv  # Import dotenv to load environment variables
import os  # Import os to access environment variables

# Load environment variables from .env file
load_dotenv()

# Configuration
HOST = '127.0.0.1'  # Flask server host
PORT = 5100         # Flask server port
UPDATE_INTERVAL = 3  # Update interval in seconds

# MQTT Broker Configuration (Load from environment variables)
MQTT_BROKER = "c29162f3d8f24ad1ae54157ddb08596c.s1.eu.hivemq.cloud"
MQTT_PORT = 8883                        # Secure MQTT port
MQTT_TOPIC = "sensors/data"             # Topic to publish sensor data
MQTT_USERNAME = os.getenv("HIVE_USERNAME")  # Load username from .env
MQTT_PASSWORD = os.getenv("HIVE_PASSWORD")  # Load password from .env

# Validate environment variables
if not MQTT_USERNAME or not MQTT_PASSWORD:
    raise ValueError("Missing MQTT credentials in .env file")

# Global variable to store the latest sensor values
latest_sensor_values = None

# Function to generate random sensor values
def generate_sensor_values():
    temperature = round(random.uniform(20.0, 35.0), 2)        # Random temperature (20.0°C to 35.0°C)
    humidity = round(random.uniform(40.0, 80.0), 2)           # Random humidity (40.0% to 80.0%)
    soil_moisture = round(random.uniform(0.0, 100.0), 2)      # Random soil moisture (0% to 100%)
    light_intensity = round(random.uniform(100.0, 1000.0), 2) # Random light intensity (100 lx to 1000 lx)
    return {
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
        "light_intensity": light_intensity
    }

# Function to update the sensor values and publish to MQTT
def update_and_publish_sensor_values():
    global latest_sensor_values

    # Initialize MQTT client
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Use certifi's CA certificates for SSL/TLS verification
    client.tls_set(ca_certs=certifi.where())  # Use the CA certificates from certifi
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    while True:
        latest_sensor_values = generate_sensor_values()
        print(f"Updated Sensor Values: {latest_sensor_values}")

        # Publish sensor data to MQTT broker
        client.publish(MQTT_TOPIC, str(latest_sensor_values))
        print(f"Published to MQTT topic '{MQTT_TOPIC}': {latest_sensor_values}")

        time.sleep(UPDATE_INTERVAL)

# Initialize Flask app
app = Flask(__name__)

# Route to fetch the latest sensor values as JSON (optional)
@app.route('/values/json', methods=['GET'])
def get_sensor_values_json():
    if latest_sensor_values is not None:
        return jsonify(latest_sensor_values)
    else:
        return {"error": "No data available"}, 404

# Run the Flask server
if __name__ == "__main__":
    # Start a background thread to update and publish sensor values
    update_thread = Thread(target=update_and_publish_sensor_values, daemon=True)
    update_thread.start()

    # Start the Flask server
    app.run(host=HOST, port=PORT)