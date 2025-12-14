"""
Real World Robot Example Skill

This skill enhances content with real-world robot examples and case studies,
connecting theoretical concepts to actual robot implementations.
"""

from typing import Optional, List
from ...llm.provider import llm_provider
from ...utils.logger import logger


# Database of real-world robot examples
ROBOT_EXAMPLES = {
    "humanoid": [
        {
            "name": "Boston Dynamics Atlas",
            "type": "Research Humanoid",
            "features": ["Dynamic balance", "Parkour capabilities", "Hydraulic actuation"],
            "ros_relevant": True
        },
        {
            "name": "Tesla Optimus",
            "type": "General Purpose Humanoid",
            "features": ["AI vision", "Dexterous manipulation", "Mass production focus"],
            "ros_relevant": False
        },
        {
            "name": "Unitree H1",
            "type": "Commercial Humanoid",
            "features": ["ROS2 compatible", "Open SDK", "Affordable research platform"],
            "ros_relevant": True
        },
        {
            "name": "Figure 01",
            "type": "Commercial Humanoid",
            "features": ["OpenAI integration", "Warehouse tasks", "Learning from demonstration"],
            "ros_relevant": True
        }
    ],
    "mobile": [
        {
            "name": "TurtleBot 4",
            "type": "Educational Mobile Robot",
            "features": ["ROS2 native", "iRobot Create 3 base", "SLAM capable"],
            "ros_relevant": True
        },
        {
            "name": "Clearpath Jackal",
            "type": "Research Mobile Platform",
            "features": ["All-terrain", "ROS2 support", "Modular payload"],
            "ros_relevant": True
        },
        {
            "name": "Boston Dynamics Spot",
            "type": "Quadruped Robot",
            "features": ["Autonomous navigation", "API access", "Industrial inspection"],
            "ros_relevant": True
        }
    ],
    "arm": [
        {
            "name": "Universal Robots UR5",
            "type": "Collaborative Robot Arm",
            "features": ["6 DOF", "Force sensing", "ROS2 driver"],
            "ros_relevant": True
        },
        {
            "name": "Franka Emika Panda",
            "type": "Research Robot Arm",
            "features": ["7 DOF", "Torque control", "libfranka + ROS2"],
            "ros_relevant": True
        },
        {
            "name": "xArm",
            "type": "Affordable Robot Arm",
            "features": ["ROS2 support", "Python SDK", "Education focused"],
            "ros_relevant": True
        }
    ],
    "autonomous_vehicle": [
        {
            "name": "Waymo Driver",
            "type": "Autonomous Vehicle System",
            "features": ["L4 autonomy", "Custom sensors", "ML perception"],
            "ros_relevant": False
        },
        {
            "name": "Autoware",
            "type": "Open Source AV Stack",
            "features": ["ROS2 based", "Full stack", "Research platform"],
            "ros_relevant": True
        }
    ]
}


EXAMPLE_PROMPT = """You are a robotics expert who connects theoretical concepts to real-world implementations.
Your task is to enhance the following content with relevant real-world robot examples.

For each major concept, provide:
1. A specific robot that uses this concept
2. How the robot implements it (sensors, algorithms, hardware)
3. Why this implementation works well (or challenges faced)
4. A "Try it yourself" suggestion using available platforms

Real-world robots you can reference:
{robot_context}

Original Content:
{content}

Enhanced content with real-world examples:"""


async def real_world_robot_example(
    content: str,
    robot_types: Optional[List[str]] = None,
    ros_only: bool = False
) -> dict:
    """
    Enhance content with real-world robot examples and case studies.

    Args:
        content: The content to enhance with examples
        robot_types: Types to focus on ("humanoid", "mobile", "arm", "autonomous_vehicle")
        ros_only: If True, only include ROS-compatible robots

    Returns:
        dict with:
            - enhanced: Content with real-world examples
            - robots_mentioned: List of robots referenced
            - try_it_suggestions: Practical suggestions for hands-on learning
            - success: Boolean indicating success
    """
    try:
        # Build robot context
        if robot_types is None:
            robot_types = list(ROBOT_EXAMPLES.keys())

        robots_to_include = []
        for rtype in robot_types:
            if rtype in ROBOT_EXAMPLES:
                for robot in ROBOT_EXAMPLES[rtype]:
                    if not ros_only or robot["ros_relevant"]:
                        robots_to_include.append(robot)

        robot_context = "\n".join([
            f"- {r['name']} ({r['type']}): {', '.join(r['features'])}"
            for r in robots_to_include
        ])

        prompt = EXAMPLE_PROMPT.format(
            robot_context=robot_context,
            content=content
        )

        result = await llm_provider.complete(
            prompt=prompt,
            system_prompt="You are a robotics engineer who has worked with many different robot platforms.",
            temperature=0.7,
            max_tokens=2000
        )

        if not result:
            return {
                "enhanced": content,
                "robots_mentioned": [],
                "try_it_suggestions": [],
                "success": False,
                "error": "LLM returned empty response"
            }

        # Extract mentioned robots
        robots_mentioned = []
        for robots in ROBOT_EXAMPLES.values():
            for robot in robots:
                if robot["name"].lower() in result.lower():
                    robots_mentioned.append(robot["name"])

        # Look for "try it" suggestions
        try_it = []
        if "turtlebot" in result.lower():
            try_it.append("Set up TurtleBot 4 in Gazebo simulation")
        if "gazebo" in result.lower():
            try_it.append("Create a custom robot in Gazebo")
        if "rviz" in result.lower():
            try_it.append("Visualize sensor data in RViz2")

        return {
            "enhanced": result,
            "robots_mentioned": list(set(robots_mentioned)),
            "try_it_suggestions": try_it,
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in real_world_robot_example: {str(e)}")
        return {
            "enhanced": content,
            "robots_mentioned": [],
            "try_it_suggestions": [],
            "success": False,
            "error": str(e)
        }
