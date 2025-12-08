#!/usr/bin/env python3
"""
ROS2 Basic Publisher Node Example
Physical AI & Humanoid Robotics Textbook

This example demonstrates a basic ROS2 publisher node that
publishes String messages to a topic at a fixed rate.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class BasicPublisher(Node):
    """
    A simple ROS2 publisher node.

    This node publishes String messages to the 'basic_topic' topic
    at a rate of 1 Hz (once per second).
    """

    def __init__(self):
        # Initialize the node with a name
        super().__init__('basic_publisher')

        # Create a publisher
        # - Message type: String
        # - Topic name: 'basic_topic'
        # - Queue size: 10
        self.publisher_ = self.create_publisher(String, 'basic_topic', 10)

        # Create a timer that calls the callback every 1 second
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Counter to track number of messages published
        self.count = 0

        self.get_logger().info('Basic Publisher node has been started')

    def timer_callback(self):
        """
        Timer callback function.

        This function is called periodically by the timer.
        It creates a message, populates it with data, and publishes it.
        """
        # Create a String message
        msg = String()
        msg.data = f'Hello, ROS2! Message #{self.count}'

        # Publish the message
        self.publisher_.publish(msg)

        # Log the published message
        self.get_logger().info(f'Publishing: "{msg.data}"')

        # Increment the counter
        self.count += 1


def main(args=None):
    """
    Main entry point for the node.
    """
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)

    # Create an instance of the publisher node
    node = BasicPublisher()

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
