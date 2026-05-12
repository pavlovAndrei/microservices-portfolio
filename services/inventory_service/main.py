from kafka import KafkaConsumer
import json
import time


def main():

    print("INVENTORY SERVICE STARTED", flush=True)

    while True:

        try:

            consumer = KafkaConsumer(
                'order_created',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='inventory-service',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                enable_auto_commit=True
            )

            print("Connected to Kafka", flush=True)

            while True:

                message_batch = consumer.poll(timeout_ms=1000)

                for topic_partition, messages in message_batch.items():

                    for message in messages:

                        print(
                            "Inventory received:",
                            message.value,
                            flush=True
                        )

        except Exception as e:

            print(f"Consumer error: {e}", flush=True)

            time.sleep(5)


if __name__ == "__main__":
    main()