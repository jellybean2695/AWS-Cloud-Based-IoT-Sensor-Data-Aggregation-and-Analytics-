import pandas as pd
import joblib
import numpy as np
import boto3
import Adafruit_DHT
import RPi.GPIO as GPIO

# Load trained model
model_path = "/home/pi/sensor2_model.pkl"
model = joblib.load(model_path)

# AWS SNS Configuration
sns_client = boto3.client('sns', region_name='ap-south-1')
sns_topic_arn = "arn:aws:sns:ap-south-1:043309341643:PlantWateringAlerts123"  # Your SNS Topic ARN

# Define GPIO pins for sensors
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
SOIL_MOISTURE_PIN = 27
LDR_PIN = 17

# Read temperature & humidity from DHT11
humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

# Read soil moisture (0 = Dry, 1 = Wet)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
soil_moisture = GPIO.input(SOIL_MOISTURE_PIN)

# Read light intensity (0 = Night, 1 = Day)
GPIO.setup(LDR_PIN, GPIO.IN)
light = GPIO.input(LDR_PIN)

# Prepare real-time sensor data
real_time_data = {
    'temperature': [temperature],
    'humidity': [humidity],
    'soil_moisture': [soil_moisture],
    'light_intensity': [150.0]  # Replace with actual LDR sensor reading if available
}

# Convert to DataFrame
input_df = pd.DataFrame(real_time_data)
print("Sensor Data:\n", input_df)

# Predict time until next watering
predicted_hours = model.predict(input_df)
predicted_time = np.round(predicted_hours[0], 2)

# Prepare Email message
message = f"""🚨 *Plant Watering Alert* 🚨

🌡 *Temperature:* {temperature}°C  
💧 *Humidity:* {humidity}%  
🌱 *Soil Moisture:* {'Wet' if soil_moisture else 'Dry'}  
🔆 *Light Intensity:* {'Day' if light else 'Night'}  

📢 *Predicted Time Until Next Watering:* {predicted_time} hours  

💡 Ensure your plant stays healthy! 🌿💦
"""

# Send Email Notification
response = sns_client.publish(
    TopicArn=sns_topic_arn,
    Message=message,
    Subject="Plant Watering Alert"
)

print("Email Notification Sent:", response)

# Cleanup GPIO setup
GPIO.cleanup()