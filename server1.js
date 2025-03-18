const mqtt = require('mqtt');
require('dotenv').config(); // Load environment variables from .env file

// MQTT Broker Configuration (Replace with your HiveMQ details)
const MQTT_BROKER = "mqtt://c29162f3d8f24ad1ae54157ddb08596c.s1.eu.hivemq.cloud";
const MQTT_PORT = 8883; // Secure MQTT port
const MQTT_TOPIC = "sensors/data"; // Topic to subscribe to
const MQTT_USERNAME = process.env.HIVE_USERNAME; // Replace with your HiveMQ username
const MQTT_PASSWORD = process.env.HIVE_PASSWORD; // Replace with your HiveMQ password

// Configure MQTT client
const options = {
    port: MQTT_PORT,
    username: MQTT_USERNAME,
    password: MQTT_PASSWORD,
    protocol: 'mqtts', // Use secure MQTT protocol
    rejectUnauthorized: true, // Enable SSL/TLS certificate verification
};

// Create MQTT client
const client = mqtt.connect(MQTT_BROKER, options);

// Handle MQTT connection events
client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client.subscribe(MQTT_TOPIC, (err) => {
        if (!err) {
            console.log(`Subscribed to topic: ${MQTT_TOPIC}`);
        } else {
            console.error(`Failed to subscribe to topic: ${MQTT_TOPIC}`, err);
        }
    });
});

// Handle incoming MQTT messages
client.on('message', (topic, message) => {
    const data = message.toString();
    console.log(`Received message on topic '${topic}': ${data}`);
});

// Handle MQTT errors
client.on('error', (err) => {
    console.error('MQTT client error:', err);
});