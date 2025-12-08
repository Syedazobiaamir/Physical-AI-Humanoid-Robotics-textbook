#!/usr/bin/env python3
"""
ROS2 Basic Subscriber Node Example
Physical AI & Humanoid Robotics Textbook

This example demonstrates a basic ROS2 subscriber node that
listens to String messages on a topic.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class BasicSubscriber(Node):
    """
    A simple ROS2 subscriber node.

    This node subscribes to the 'basic_topic' topic and
    logs received messages.
    """

    def __init__(self):
        # Initialize the node with a name
        super().__init__('basic_subscriber')

        # Create a subscription
        # - Message type: String
        # - Topic name: 'basic_topic'
        # - Callback function: listener_callback
        # - Queue size: 10
        self.subscription = self.create_subscription(
            String,
            'basic_topic',
            self.listener_callback,
            10
        )

        # Prevent unused variable warning
        self.subscription

        self.get_logger().info('Basic Subscriber node has been started')

    def listener_callback(self, msg):
        """
        Callback function for received messages.

        This function is called whenever a message is received
        on the subscribed topic.

        Args:
            msg: The received String message
        """
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    """
    Main entry point for the node.
    """
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)

    # Create an instance of the subscriber node
    node = BasicSubscriber()

    try:
        # Spin the node to process callbacks
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
