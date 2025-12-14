"""
Reusable AI Skills for Content Personalization

Skills are modular, reusable functions that can be composed by agents
to perform specific content transformation tasks.
"""

from .simplify_for_beginner import simplify_for_beginner
from .hardware_mapping import hardware_mapping
from .real_world_robot_example import real_world_robot_example
from .exam_ready_summary import exam_ready_summary

__all__ = [
    'simplify_for_beginner',
    'hardware_mapping',
    'real_world_robot_example',
    'exam_ready_summary',
]
