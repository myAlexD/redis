# Redis Consumer Group Application

This project simulates a scalable consumer group processing messages from a Redis Pub/Sub channel. The application includes a publisher that generates messages and a consumer group that processes these messages. 

## Table of Contents

- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Configuration](#configuration)
- [Notes](#notes)

## Technologies

- **Redis**: A distributed, in-memory key-value database.
- **Python**: The programming language used to implement the application.
- **Multiprocessing**: Used to simulate multiple consumers.

## Installation

### Prerequisites

1. **Redis Server**: Ensure you have Redis installed and running. You can download it from [Redis.io](https://redis.io/).
2. **Python 3.x**: Make sure you have Python installed. You can download it from [Python.org](https://www.python.org/downloads/).

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/myAlexD/redis.git
   cd redis
2. **Create a virtual environment**:

    ```sh
    python -m venv venv
3. **Activate the virtual environment:**:

    ```sh
    venv\Scripts\activate
4. **Install the required packages:**:
    ```sh
    pip install -r requirements.txt
5. **Start the Redis server:**:
    ```sh
    redis-server
## Usage

### Publisher

The publisher simulates the generation of messages.

Run the publisher script:
python publisher.py

### Consumer Group

The consumer group processes messages from the Redis Pub/Sub channel.

Run the consumer group with the desired number of consumers:
python consumer_group.py --group-size <number_of_consumers>
Replace <number_of_consumers> with the number of consumers you want to run.

## Testing

Unit tests are provided to ensure the functionality of the consumer group.

1. Run the tests:
   python -m unittest discover tests

### Example Test Output

You should see output indicating whether the tests passed or failed.

## Configuration

### Redis Connection

Ensure your Redis server details are correctly configured in the consumer_group.py and publisher.py scripts:
redis_host = "localhost"
redis_port = 6379
Modify these values if your Redis server is running on a different host or port.

### Consumer Group Size

The consumer group size can be configured using the --group-size argument when running the consumer_group.

    python consumer_group.py --group-size 3

## Notes

- This application is designed for educational purposes and simulates a distributed consumer group using Redis.
- Ensure your Redis server is running before starting the publisher or consumer group.
- Adjust the target_duration and batch_size in the publisher.py script to simulate different message loads.
