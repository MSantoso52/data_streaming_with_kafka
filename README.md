# Data_Streaming_with_Kafka
# *Overview*
Project repo to demonstrate data streaming & data consuming using Kafka. Data streaming is displayed into web in real time using Streamlit.
# *Project FLow*
1. Prequsition
   - kafka service active on localhost:9092, topic defined: new-events  # change with your topic
     ```bash
     sudo systemctl status kafka
3. Data streamer
   - python3 code to autogenerate json data every 20 sec & stream into kafka-producer
     ```bash
     python3 datastreamer.py
     ```
     ```python3
     # import necesary library
     import json
     import time
     import random
     from datetime import datetime
     from kafka import KafkaProducer
     from faker import Faker
     ```
     ```python3
     # --- Configuration ---
      KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address
      KAFKA_TOPIC = 'new-events'    # Replace with your desired Kafka topic name
      INTERVAL_SECONDS = 20           # in seconds
     ```
     ```python3
     # Connect to kafka broker
     producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8') # Serialize dict to JSON bytes
        )
     ```
5. Data displaying
   - streamlit code to consume data streaming from kafka into kafka-consumer,
   - using pandas dataframe to create table to be displayed into web through streamlit
7. Fix the code following error messages
