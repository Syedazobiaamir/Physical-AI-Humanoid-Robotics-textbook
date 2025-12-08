#!/usr/bin/env python3
"""
ROS2 Object Detection Node Example
Physical AI & Humanoid Robotics Textbook

This example demonstrates a ROS2 node that performs
object detection on camera images.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import numpy as np
import json


class ObjectDetector(Node):
    """
    Object detection node using camera input.

    This node subscribes to camera images, performs object detection,
    and publishes detection results.
    """

    def __init__(self):
        super().__init__('object_detector')

        # CV Bridge for converting ROS images to OpenCV format
        self.bridge = CvBridge()

        # Subscribe to camera images
        self.image_sub = self.create_subscription(
            Image,
            'camera/color/image_raw',
            self.image_callback,
            10
        )

        # Publish detection results
        self.detection_pub = self.create_publisher(
            String,
            'detections',
            10
        )

        # Detection parameters
        self.confidence_threshold = 0.5

        self.get_logger().info('Object Detector node has been started')

    def image_callback(self, msg):
        """
        Process incoming camera images.

        Args:
            msg: sensor_msgs/Image message
        """
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Perform detection (placeholder - integrate with actual model)
            detections = self.detect_objects(cv_image)

            # Publish results
            result = {
                'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
                'detections': detections,
                'image_width': cv_image.shape[1],
                'image_height': cv_image.shape[0]
            }

            detection_msg = String()
            detection_msg.data = json.dumps(result)
            self.detection_pub.publish(detection_msg)

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def detect_objects(self, image: np.ndarray):
        """
        Perform object detection on an image.

        Args:
            image: OpenCV image (BGR format)

        Returns:
            List of detection dictionaries
        """
        # Placeholder detection logic
        # In practice, use YOLO, Detectron2, or other detection models

        detections = []

        # Example detection (simulated)
        # Replace with actual model inference
        height, width = image.shape[:2]

        # Simulated detection
        detection = {
            'class': 'object',
            'class_id': 0,
            'confidence': 0.95,
            'bbox': {
                'x': int(width * 0.3),
                'y': int(height * 0.3),
                'width': int(width * 0.4),
                'height': int(height * 0.4)
            }
        }

        if detection['confidence'] >= self.confidence_threshold:
            detections.append(detection)

        return detections

    def preprocess_image(self, image: np.ndarray, target_size=(640, 640)):
        """
        Preprocess image for detection model.

        Args:
            image: Input image
            target_size: Target size for model input

        Returns:
            Preprocessed image
        """
        import cv2

        # Resize while maintaining aspect ratio
        h, w = image.shape[:2]
        scale = min(target_size[0] / w, target_size[1] / h)
        new_w, new_h = int(w * scale), int(h * scale)

        resized = cv2.resize(image, (new_w, new_h))

        # Pad to target size
        padded = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
        pad_x = (target_size[0] - new_w) // 2
        pad_y = (target_size[1] - new_h) // 2
        padded[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = resized

        return padded, scale, (pad_x, pad_y)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetector()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
