import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
from datetime import datetime

# Sensor pins
DHT_PIN = 4  # Temperature and Humidity Sensor
SOIL_MOISTURE_PIN = 27  # Soil Moisture Sensor
LDR_PIN = 17  # Light Sensor

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)

# AWS IoT setup
iot_client = AWSIoTMQTTClient("RaspberryPiThing")
iot_client.configureEndpoint("a37tpftlj81mcz-ats.iot.ap-south-1.amazonaws.com", 8883)
iot_client.configureCredentials(
    "/home/pi/root-CA.pem",
    "/home/pi/private.pem.key",
    "/home/pi/certificate.pem.crt",
)

# Configure MQTT client
iot_client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
iot_client.configureDrainingFrequency(2)  # Draining: 2 Hz
iot_client.configureConnectDisconnectTimeout(10)  # 10 seconds
iot_client.configureMQTTOperationTimeout(5)  # 5 seconds

# S3 setup
s3_client = boto3.client("s3")
bucket_name = "iot--data--storage"  # Your S3 bucket name

# Connect to AWS IoT Core
try:
    print("Connecting to AWS IoT...")
    iot_client.connect()
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)  # Only exit if there's a connection failure

# Function to publish data to AWS IoT Core
def publish_data_to_iot(data):
    try:
        print(f"Publishing data to IoT Core: {data}")
        iot_client.publish("RaspberryPiThing/data", json.dumps(data))
    except Exception as e:
        print(f"Error while publishing to IoT Core: {e}")

# Function to upload data to S3
def upload_data_to_s3(data):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"sensor_data_{timestamp}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        print(f"Data successfully uploaded to S3 as {file_name}")
    except Exception as e:
        print(f"Error while uploading to S3: {e}")

# Function to gather and process sensor data
def gather_and_process_data():
    try:
        # Read data from DHT sensor
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_PIN)
        
        # Read data from soil moisture sensor and LDR
        soil_moisture = GPIO.input(SOIL_MOISTURE_PIN)
        light = GPIO.input(LDR_PIN)

        # Debugging: Print sensor values
        print(f"DEBUG - Soil Moisture: {soil_moisture}, Light: {light}")

        if humidity is not None and temperature is not None:
            # Prepare the data payload
            data = {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "soil_moisture": soil_moisture,
                "light": light,
                "timestamp": datetime.now().isoformat(),
            }
            return data
        else:
            print("Failed to read from DHT sensor!")
            return None
    except Exception as e:
        print(f"Error while gathering sensor data: {e}")
        return None

# Main loop
try:
    while True:
        sensor_data = gather_and_process_data()
        if sensor_data:
            publish_data_to_iot(sensor_data)  # Publish data to AWS IoT Core
            upload_data_to_s3(sensor_data)  # Upload data to S3
        time.sleep(10)  # Publish data every 10 seconds
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    GPIO.cleanup()