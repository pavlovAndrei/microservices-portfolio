from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'order_created',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Notification service listening...")

for message in consumer:
    print("Notification received:", message.value)