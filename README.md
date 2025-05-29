# data_streaming_with_kafka
Data streaming with Kafka &amp; display into web real time with Streamlit
1. Prequsition -- kafka service active on localhost:9092, topic defined: new-events  # change with your topic
2. Data streamer -- python3 code to autogenerate json data every 20 sec & stream into kafka-producer
3. Data displaying -- streamlit code to consume data streaming from kafka into kafka-consumer, using pandas dataframe to create table to be displayed into web through streamlit
4. Fix the code following error message
