#!/usr/bin/env python3
"""
ROS2 PID Controller Node Example
Physical AI & Humanoid Robotics Textbook

This example demonstrates a PID controller node for
robot joint position control.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import time


class PIDController(Node):
    """
    PID Controller for joint position control.

    This node implements a Proportional-Integral-Derivative (PID)
    controller for controlling robot joint positions.
    """

    def __init__(self):
        super().__init__('pid_controller')

        # Declare parameters with default values
        self.declare_parameter('kp', 10.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 1.0)
        self.declare_parameter('joint_name', 'joint_1')

        # Get parameter values
        self.kp = self.get_parameter('kp').value
        self.ki = self.get_parameter('ki').value
        self.kd = self.get_parameter('kd').value
        self.joint_name = self.get_parameter('joint_name').value

        # Controller state
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time.time()
        self.current_position = 0.0
        self.reference = 0.0

        # Anti-windup limits
        self.integral_max = 10.0
        self.integral_min = -10.0

        # Output limits
        self.output_max = 100.0
        self.output_min = -100.0

        # Publishers
        self.cmd_pub = self.create_publisher(
            Float64,
            'joint_command',
            10
        )

        # Subscribers
        self.state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.state_callback,
            10
        )

        self.ref_sub = self.create_subscription(
            Float64,
            'reference',
            self.reference_callback,
            10
        )

        # Control loop timer (100 Hz)
        self.timer = self.create_timer(0.01, self.control_loop)

        self.get_logger().info(
            f'PID Controller started: Kp={self.kp}, Ki={self.ki}, Kd={self.kd}'
        )

    def reference_callback(self, msg):
        """Update reference/setpoint value."""
        self.reference = msg.data
        self.get_logger().debug(f'Reference updated: {self.reference}')

    def state_callback(self, msg):
        """Update current joint position from state feedback."""
        try:
            idx = msg.name.index(self.joint_name)
            self.current_position = msg.position[idx]
        except (ValueError, IndexError):
            pass

    def control_loop(self):
        """
        Main PID control loop.

        Computes control output based on error between
        reference and current position.
        """
        current_time = time.time()
        dt = current_time - self.prev_time

        if dt <= 0:
            return

        # Compute error
        error = self.reference - self.current_position

        # Proportional term
        p_term = self.kp * error

        # Integral term with anti-windup
        self.integral += error * dt
        self.integral = max(
            self.integral_min,
            min(self.integral_max, self.integral)
        )
        i_term = self.ki * self.integral

        # Derivative term
        d_term = self.kd * (error - self.prev_error) / dt

        # Compute total output
        output = p_term + i_term + d_term

        # Apply output limits
        output = max(self.output_min, min(self.output_max, output))

        # Publish command
        cmd = Float64()
        cmd.data = output
        self.cmd_pub.publish(cmd)

        # Update state
        self.prev_error = error
        self.prev_time = current_time

        # Log debug info
        self.get_logger().debug(
            f'Error: {error:.4f}, Output: {output:.4f} '
            f'(P={p_term:.2f}, I={i_term:.2f}, D={d_term:.2f})'
        )

    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time.time()
        self.get_logger().info('Controller state reset')


def main(args=None):
    rclpy.init(args=args)
    node = PIDController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
