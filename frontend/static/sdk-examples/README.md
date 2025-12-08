# SDK Code Examples

This directory contains runnable code examples for the Physical AI & Humanoid Robotics textbook.

## Directory Structure

```
sdk-examples/
├── ros2-basics/           # ROS2 fundamentals
│   ├── publisher_node.py  # Basic publisher example
│   └── subscriber_node.py # Basic subscriber example
├── perception/            # Computer vision and sensing
│   └── object_detector.py # Object detection with ROS2
├── control/               # Control systems
│   └── pid_controller.py  # PID controller implementation
└── README.md
```

## Usage

### Prerequisites

- ROS2 Humble or later installed
- Python 3.10+
- OpenCV for perception examples

### Running Examples

1. Source your ROS2 installation:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

2. Run a publisher example:
   ```bash
   python3 sdk-examples/ros2-basics/publisher_node.py
   ```

3. In a new terminal, run the subscriber:
   ```bash
   python3 sdk-examples/ros2-basics/subscriber_node.py
   ```

## Chapter Mapping

| Chapter | Examples |
|---------|----------|
| Week 1: Introduction to ROS2 | ros2-basics/publisher_node.py, subscriber_node.py |
| Week 5: Computer Vision | perception/object_detector.py |
| Week 9: Robot Control | control/pid_controller.py |
