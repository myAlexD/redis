import unittest
from unittest.mock import patch, MagicMock
import json
import time
from consumer_group import process_message, consumer, monitor_processed_messages

class TestConsumerGroup(unittest.TestCase):

    @patch('consumer_group.redis.Redis')
    def test_process_message(self, MockRedis):
        message = {"data": json.dumps({"message_id": "test_id"})}
        consumer_id = "consumer_1"
        processed_message = process_message(message, consumer_id)
        
        self.assertIn(f"processed_by_{consumer_id}", processed_message)
        self.assertEqual(processed_message["message_id"], "test_id")

    @patch('consumer_group.redis.Redis')
    @patch('consumer_group.time.sleep', return_value=None)
    def test_consumer(self, mock_sleep, MockRedis):
        mock_redis = MockRedis.return_value
        mock_pubsub = mock_redis.pubsub.return_value
        mock_pubsub.get_message.side_effect = [
            {"type": "message", "data": json.dumps({"message_id": "test_id"})},
            None
        ]
        
        consumer_id = "consumer_1"

        # Run consumer directly
        consumer(consumer_id, test_mode=True)
        
        self.assertTrue(mock_redis.xadd.called, "xadd was not called")
        call_args_list = mock_redis.xadd.call_args_list
        self.assertTrue(any('messages:processed' in call_args[0] for call_args in call_args_list))

    @patch('consumer_group.redis.Redis')
    @patch('consumer_group.time.sleep', return_value=None)
    def test_monitor_processed_messages(self, mock_sleep, MockRedis):
        mock_redis = MockRedis.return_value
        mock_redis.xread.side_effect = [
            [("messages:processed", {"data": json.dumps({"message_id": "test_id"})})],
            []
        ]

        # Run monitor directly
        monitor_processed_messages(test_mode=True)
        
        self.assertTrue(mock_redis.xread.called, "xread was not called")
        call_args_list = mock_redis.xread.call_args_list
        self.assertTrue(any('messages:processed' in call_args[0] for call_args in call_args_list))

if __name__ == '__main__':
    unittest.main()
