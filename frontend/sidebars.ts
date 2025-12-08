import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Module 1: ROS2 Fundamentals',
      items: [
        'module-1/week-1-intro',
        'module-1/week-2-nodes-topics',
        'module-1/week-3-services-actions',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Robot Perception',
      items: [
        'module-2/week-4-sensors',
        'module-2/week-5-computer-vision',
        'module-2/week-6-slam',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Motion and Control',
      items: [
        'module-3/week-7-kinematics',
        'module-3/week-8-motion-planning',
        'module-3/week-9-control',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Integration & AI',
      items: [
        'module-4/week-10-reinforcement-learning',
        'module-4/week-11-integration',
        'module-4/week-12-advanced',
        'module-4/week-13-final-project',
      ],
    },
  ],
};

export default sidebars;
