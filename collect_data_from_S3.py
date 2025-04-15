import boto3
import pandas as pd
import json

# AWS S3 Configuration
s3 = boto3.client('s3')
bucket_name = 'iot--data--storage'  

# List all JSON files
response = s3.list_objects_v2(Bucket=bucket_name)
json_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.json')]

# Collect all sensor data
all_data = []
for file_key in json_files:
    file_response = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = file_response['Body'].read().decode('utf-8')

    try:
        json_data = json.loads(data)
        if isinstance(json_data, dict):
            json_data = [json_data]  
        all_data.extend(json_data)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_key}")

# Convert to Pandas DataFrame
df_s3 = pd.DataFrame(all_data)

# Handle missing values
df_s3 = df_s3.fillna(0)  # Replace NaNs with 0 (change if needed)

# Show info
print(f"Total rows: {len(df_s3)}")
print(df_s3.head(10))

# Save cleaned data
df_s3.to_csv("sensor_data_cleaned.csv", index=False)
print("Cleaned data saved as sensor_data_cleaned.csv.")