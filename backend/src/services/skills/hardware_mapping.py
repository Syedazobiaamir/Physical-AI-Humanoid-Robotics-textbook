"""
Hardware Mapping Skill

This skill maps software concepts to their hardware implementations,
helping students with hardware backgrounds understand the practical
applications of robotics software concepts.
"""

from typing import Optional, List
from ...llm.provider import llm_provider
from ...utils.logger import logger


HARDWARE_MAPPING_PROMPT = """You are a robotics engineer who excels at bridging software and hardware concepts.
Your task is to take software-focused robotics content and add hardware context.

For each concept, explain:
1. What physical hardware component(s) implement this concept
2. How the software interfaces with the hardware (sensors, actuators, controllers)
3. Real circuit/wiring considerations (voltage, protocols like I2C, SPI, CAN)
4. Common hardware platforms where this is used (Arduino, Raspberry Pi, industrial PLCs)
5. Practical troubleshooting tips from a hardware perspective

Technical level: Intermediate hardware engineer familiar with electronics but new to ROS2

Original Software Content:
{content}

Hardware-enhanced version with physical implementation details:"""


# Common hardware mappings for quick reference
HARDWARE_MAPPINGS = {
    "node": {
        "hardware": "Microcontroller or Single Board Computer (SBC)",
        "examples": ["Arduino", "Raspberry Pi", "NVIDIA Jetson", "ESP32"],
        "protocols": ["USB", "UART", "Ethernet"]
    },
    "topic": {
        "hardware": "Sensor data streams, actuator commands",
        "examples": ["IMU readings", "motor velocities", "camera frames"],
        "protocols": ["I2C", "SPI", "CAN bus", "Ethernet"]
    },
    "service": {
        "hardware": "Request-response hardware operations",
        "examples": ["Calibration routines", "configuration changes", "status queries"],
        "protocols": ["Serial commands", "Modbus"]
    },
    "action": {
        "hardware": "Long-running physical operations",
        "examples": ["Arm movements", "navigation goals", "homing sequences"],
        "protocols": ["EtherCAT", "CAN", "Servo protocols"]
    },
    "lidar": {
        "hardware": "Rotating laser scanner or solid-state LiDAR",
        "examples": ["Velodyne", "SICK", "RPLIDAR", "Intel RealSense"],
        "protocols": ["Ethernet", "USB", "UART"]
    },
    "camera": {
        "hardware": "CMOS/CCD image sensor with lens",
        "examples": ["USB webcam", "Intel RealSense", "ZED stereo", "industrial GigE cameras"],
        "protocols": ["USB 3.0", "MIPI CSI", "GigE Vision"]
    },
    "imu": {
        "hardware": "Inertial Measurement Unit (accelerometer + gyroscope + magnetometer)",
        "examples": ["MPU6050", "BNO055", "VectorNav", "Xsens"],
        "protocols": ["I2C", "SPI", "RS-422"]
    },
    "motor": {
        "hardware": "DC/Brushless motor with encoder and driver",
        "examples": ["Dynamixel", "ODrive", "Maxon", "stepper motors"],
        "protocols": ["PWM", "CAN", "EtherCAT", "RS-485"]
    }
}


async def hardware_mapping(
    content: str,
    focus_topics: Optional[List[str]] = None,
    detail_level: str = "intermediate"
) -> dict:
    """
    Add hardware context and implementation details to software content.

    Args:
        content: The software-focused content to enhance
        focus_topics: Optional list of specific topics to focus on
        detail_level: "basic", "intermediate", or "advanced"

    Returns:
        dict with:
            - enhanced: Content with hardware mapping added
            - hardware_refs: List of hardware components mentioned
            - protocols_mentioned: Communication protocols referenced
            - success: Boolean indicating if transformation succeeded
    """
    try:
        # Build context from known mappings
        relevant_mappings = []
        for keyword, mapping in HARDWARE_MAPPINGS.items():
            if keyword.lower() in content.lower():
                relevant_mappings.append(f"- {keyword.upper()}: {mapping['hardware']} (e.g., {', '.join(mapping['examples'][:3])})")

        context = ""
        if relevant_mappings:
            context = "Relevant hardware mappings to incorporate:\n" + "\n".join(relevant_mappings) + "\n\n"

        prompt = context + HARDWARE_MAPPING_PROMPT.format(content=content)

        if focus_topics:
            prompt += f"\n\nFocus especially on these topics: {', '.join(focus_topics)}"

        if detail_level == "basic":
            prompt += "\n\nKeep hardware details simple - focus on concepts over specifications."
        elif detail_level == "advanced":
            prompt += "\n\nInclude detailed specifications, timing requirements, and industrial considerations."

        result = await llm_provider.complete(
            prompt=prompt,
            system_prompt="You are a hardware engineer who helps software developers understand physical robotics systems.",
            temperature=0.7,
            max_tokens=2500
        )

        if not result:
            return {
                "enhanced": content,
                "hardware_refs": [],
                "protocols_mentioned": [],
                "success": False,
                "error": "LLM returned empty response"
            }

        # Extract hardware references
        hardware_refs = []
        all_protocols = ["I2C", "SPI", "UART", "CAN", "USB", "Ethernet", "PWM", "EtherCAT", "RS-485", "MIPI"]

        for hw in HARDWARE_MAPPINGS.values():
            for example in hw["examples"]:
                if example.lower() in result.lower():
                    hardware_refs.append(example)

        protocols_found = [p for p in all_protocols if p in result]

        return {
            "enhanced": result,
            "hardware_refs": list(set(hardware_refs)),
            "protocols_mentioned": protocols_found,
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in hardware_mapping: {str(e)}")
        return {
            "enhanced": content,
            "hardware_refs": [],
            "protocols_mentioned": [],
            "success": False,
            "error": str(e)
        }
