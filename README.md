# Data_Streaming_with_Kafka
# *Overview*
Project repo to demonstrate data streaming & data consuming using Kafka. Data streaming is displayed into web in real time using Streamlit.
# *Project FLow*
1. Prequsition
   - kafka service active on localhost:9092, topic defined: new-events  # change with your topic
3. Data streamer
   - python3 code to autogenerate json data every 20 sec & stream into kafka-producer
5. Data displaying
   - streamlit code to consume data streaming from kafka into kafka-consumer, using pandas dataframe to create table to be displayed into web through streamlit
7. Fix the code following error messages
