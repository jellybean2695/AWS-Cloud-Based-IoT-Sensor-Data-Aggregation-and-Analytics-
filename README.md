# AWS-Cloud-Based-IoT-Sensor-Data-Aggregation-and-Analytics-
The AWS Cloud-Based IoT Sensor Data Aggregation and Analytics is designed to monitor and analyze environmental parameters using IoT sensors and AWS cloud services. The system collects real-time data from soil moisture, temperature, and light sensors, transmitting it to AWS IoT Core for centralized processing. AWS QuickSight provides visual analytics, enabling users to track environmental trends effectively. Machine learning (ML) integration via AWS SageMaker enhances the system by predicting soil moisture retention, helping to optimize irrigation schedules for efficient water use.
Preliminary results indicate that real-time data collection and ML-driven predictions improve decision-making in agriculture. The implementation of AWS services such as Lambda, DynamoDB, and API Gateway ensures seamless data processing and storage, while WebSockets or AWS AppSync provide continuous real-time updates to a web platform. The system successfully delivers an interactive and user-friendly interface, allowing farmers, researchers, and agronomists to access critical insights for precision farming.In conclusion, the project demonstrates the potential of IoT and cloud-based analytics in transforming agricultural practices. By leveraging AWS infrastructure and machine learning, the solution optimizes water resource management and enhances agricultural productivity. 	
The steps for the project execution are as follows ;
1) Connect sensors to your raspberry pi.
2) Download the certificates from the AWS cloud and paste them in raspberry pi desktop.
3) Write a code to send the sensors data to the AWS cloud by acessing the the three certificates.
4) Store all the sensor data in AWS S3 cloud.
5) Collect the data from S3 preprocess the data and create a target variable in exel file.
6) Train the data with Random Forest Regression to predict time until watering.
7) Use AWS SNS to send the predicted time to your email or SMS. 
