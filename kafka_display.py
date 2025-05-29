import streamlit as st
import json
from kafka import KafkaConsumer
import pandas as pd
import time

# --- Configuration (matching data_streaming.py) ---
KAFKA_BROKER = 'localhost:9092'  # Ensure this matches your Kafka broker address
KAFKA_TOPIC = 'new-events'    # Ensure this matches the topic from data_streaming.py

# --- Streamlit Application ---
st.set_page_config(page_title="Kafka Real-time Data Stream", layout="wide")
st.title("Kafka Real-time Customer Purchase Data Stream")
st.markdown("This application displays data streamed from the Kafka topic `new-events`.")

# Initialize an empty list to store incoming data
all_data = []

# Create a Streamlit placeholder for the data table
data_placeholder = st.empty()

# Create a Streamlit placeholder for the raw JSON messages
raw_json_placeholder = st.empty()


def consume_kafka_messages():
    """
    Consumes messages from Kafka and updates the Streamlit display.
    """
    st.info(f"Attempting to connect to Kafka broker: {KAFKA_BROKER} and topic: {KAFKA_TOPIC}")
    try:
        # Initialize Kafka Consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='latest',  # Start consuming from the latest message
            enable_auto_commit=True,
            group_id='streamlit-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        st.success("Successfully connected to Kafka!")
        st.write("Waiting for messages...")

        # Loop to continuously consume messages
        for message in consumer:
            # Extract the value (which is already deserialized by value_deserializer)
            customer_data = message.value

            # Append new data to the list
            all_data.append(customer_data)

            # Keep only the last 100 messages to prevent memory issues
            if len(all_data) > 100:
                all_data.pop(0)

            # Convert the list of dictionaries to a Pandas DataFrame for better display
            df = pd.DataFrame(all_data)

            # Update the data table placeholder
            with data_placeholder.container():
                st.subheader("Customer Purchase Records")
                st.dataframe(df, use_container_width=True)

            # Update the raw JSON messages placeholder
            with raw_json_placeholder.container():
                st.subheader("Raw JSON Messages (Latest 5)")
                # Display the last few raw JSON messages
                for i in range(max(0, len(all_data) - 5), len(all_data)):
                    st.json(all_data[i])

            # Optional: Add a small delay to control update frequency
            time.sleep(0.1)

    except Exception as e:
        st.error(f"Error connecting to or consuming from Kafka: {e}")
        st.warning("Please ensure your Kafka broker is running and accessible.")
        st.warning(f"Also, make sure the Kafka topic '{KAFKA_TOPIC}' exists and 'data_streaming.py' is sending data to it.")

# Run the consumer in a separate thread or directly if not using threading
if __name__ == "__main__":
    consume_kafka_messages()

