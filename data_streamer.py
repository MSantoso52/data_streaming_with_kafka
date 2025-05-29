import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker

# --- Configuration ---
KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address
KAFKA_TOPIC = 'new-events'    # Replace with your desired Kafka topic name
INTERVAL_SECONDS = 20           # in seconds

# --- Helper data for generating names ---
fake = Faker()

def generate_customer_data():
    """
    Generates a dictionary containing customer data.
    """
    
    item_names = [
        "Pen", "Pencil", "Notebook", "Eraser", "Ruler", "Highliter",
        "Paperclip", "Stapler", "Sticky Notes", "Scissors", "Tape",
        "Correction Pen", "Binder", "Devider", "File Folder", "Drawing Pen",
        "Colored Pencils", "Marker", "Glue Stick", "Calculator"
    ]

    customer_id = random.randint(10000, 99999)
    full_name = fake.name() 
    bought_item = random.choice(item_names)
    qty_purchase = random.randint(1, 10)
    price_item = round(random.uniform(5.00, 500.00), 2)
    time_purchase = datetime.now().strftime("%Y-%m-%d") 

    data = {
        "customer_id": customer_id,
        "full_name": full_name,
        "bought_item": bought_item,
        "qty_purchase": qty_purchase,
        "price_item": price_item,
        "time_purchase": time_purchase
    }
    return data

def main():
    """
    Main function to initialize Kafka producer and stream data.
    """
    print(f"Attempting to connect to Kafka broker: {KAFKA_BROKER}")
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8') # Serialize dict to JSON bytes
        )
        print("Kafka Producer initialized successfully.")
    except Exception as e:
        print(f"Error initializing Kafka Producer: {e}")
        print("Please ensure your Kafka broker is running and accessible.")
        return

    print(f"Streaming data to Kafka topic: {KAFKA_TOPIC} every {INTERVAL_SECONDS} seconds...")

    while True:
        customer_data = generate_customer_data()
        json_data = json.dumps(customer_data) # Convert dictionary to JSON string

        try:
            # Send the JSON data to the Kafka topic
            future = producer.send(KAFKA_TOPIC, value=customer_data)
            record_metadata = future.get(timeout=10) # Block until a result is received, 10s timeout
            print(f"Sent: {json_data} to topic '{record_metadata.topic}' partition {record_metadata.partition} offset {record_metadata.offset}")
        except Exception as e:
            print(f"Error sending data to Kafka: {e}")
            print("Retrying in the next interval...")

        time.sleep(INTERVAL_SECONDS) # Wait for the specified interval

if __name__ == "__main__":
    main()

