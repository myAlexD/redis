import argparse
import json
import random
import time
import uuid
from datetime import datetime
from multiprocessing import Process
import redis

# Redis connection details
redis_host = "localhost"
redis_port = 6379

def process_message(message, consumer_id):
    message_data = json.loads(message["data"])
    message_data[f"processed_by_{consumer_id}"] = str(uuid.uuid4())
    return message_data

def consumer(consumer_id, stop_event=None, test_mode=False):
    try:
        connection = redis.Redis(host=redis_host, port=redis_port)
        pubsub = connection.pubsub()
        pubsub.subscribe("messages:published")

        while not (stop_event and stop_event.is_set()):
            message = pubsub.get_message()
            if message and message["type"] == "message":
                processed_message = process_message(message, consumer_id)
                connection.xadd("messages:processed", {"data": json.dumps(processed_message)})
            if test_mode:
                break
            time.sleep(0.01)
    except redis.ConnectionError:
        print(f"Error: Failed to connect to Redis server as consumer {consumer_id}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")

def monitor_processed_messages(stop_event=None, test_mode=False):
    connection = redis.Redis(host=redis_host, port=redis_port)
    start_time = datetime.now()
    processed_messages_count = 0

    while not (stop_event and stop_event.is_set()):
        current_time = datetime.now()
        messages = connection.xread({"messages:processed": "0-0"}, block=1000, count=1000)
        processed_messages_count += len(messages)

        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time > 0:
            print(f"Messages processed per second: {processed_messages_count / elapsed_time:.2f}")
        if test_mode:
            break
        time.sleep(3)

def main(group_size):
    connection = redis.Redis(host=redis_host, port=redis_port)
    connection.delete("consumer:ids")

    consumer_ids = [f"consumer_{i}" for i in range(group_size)]
    consumer_processes = []

    for consumer_id in consumer_ids:
        connection.rpush("consumer:ids", consumer_id)
        consumer_process = Process(target=consumer, args=(consumer_id,))
        consumer_process.start()
        consumer_processes.append(consumer_process)

    monitor_process = Process(target=monitor_processed_messages)
    monitor_process.start()

    for consumer_process in consumer_processes:
        consumer_process.join()
    monitor_process.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redis Consumer Group")
    parser.add_argument("--group-size", type=int, required=True, help="Number of consumers in the group")
    args = parser.parse_args()
    main(args.group_size)
