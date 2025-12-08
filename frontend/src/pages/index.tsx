import React from 'react';
import Layout from '@theme/Layout';
import Hero from '../components/Hero';
import ModuleCard, {
  ModuleData,
  ROS2Icon,
  SimulationIcon,
  IsaacIcon,
  VLAIcon,
  CapstoneIcon,
} from '../components/ModuleCard';
import styles from './index.module.css';

const modules: ModuleData[] = [
  {
    id: 'module-1',
    title: 'ROS2 Fundamentals',
    description:
      'Learn the Robot Operating System 2 from basics to advanced topics including nodes, topics, services, and actions.',
    weeks: 'Weeks 1-3',
    icon: <ROS2Icon />,
    link: '/docs/module-1/week-1-intro',
    color: '#3B82F6',
  },
  {
    id: 'module-2',
    title: 'Gazebo & Unity Simulation',
    description:
      'Master robot simulation with Gazebo and Unity, including physics simulation, sensor modeling, and environment design.',
    weeks: 'Weeks 4-6',
    icon: <SimulationIcon />,
    link: '/docs/module-2/week-4-sensors',
    color: '#8B5CF6',
  },
  {
    id: 'module-3',
    title: 'Isaac Platform',
    description:
      'Explore NVIDIA Isaac for AI-powered robotics including perception, navigation, and manipulation pipelines.',
    weeks: 'Weeks 7-9',
    icon: <IsaacIcon />,
    link: '/docs/module-3/week-7-kinematics',
    color: '#EC4899',
  },
  {
    id: 'module-4',
    title: 'Vision-Language-Action Models',
    description:
      'Implement cutting-edge VLA models for robot learning, combining vision, language understanding, and action generation.',
    weeks: 'Weeks 10-12',
    icon: <VLAIcon />,
    link: '/docs/module-4/week-10-reinforcement-learning',
    color: '#F59E0B',
  },
  {
    id: 'capstone',
    title: 'Capstone Project',
    description:
      'Apply your knowledge to build a complete humanoid robot application integrating all modules and deploying to real hardware.',
    weeks: 'Week 13',
    icon: <CapstoneIcon />,
    link: '/docs/module-4/week-13-final-project',
    color: '#10B981',
  },
];

function Features(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className={styles.container}>
        <h2 className={styles.sectionTitle}>Platform Features</h2>
        <div className={styles.featureGrid}>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>💬</div>
            <h3>AI-Powered ChatBot</h3>
            <p>
              Ask questions about any chapter content. Select text for focused
              answers or use context mode for broader explanations.
            </p>
          </div>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>🎯</div>
            <h3>Personalized Learning</h3>
            <p>
              Adapt content to your skill level. Choose beginner, intermediate,
              or advanced variants for each chapter.
            </p>
          </div>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>🌐</div>
            <h3>Urdu Translation</h3>
            <p>
              Access content in Urdu with preserved formatting. Technical terms
              are transliterated with glossary support.
            </p>
          </div>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>📝</div>
            <h3>Interactive Quizzes</h3>
            <p>
              Test your understanding with 5 multiple-choice questions per
              chapter. Get instant feedback on your answers.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="An AI-native textbook for mastering robotics with ROS2, simulation, and modern AI techniques"
    >
      <Hero />
      <main>
        <section className={styles.modules}>
          <div className={styles.container}>
            <h2 className={styles.sectionTitle}>Course Modules</h2>
            <p className={styles.sectionSubtitle}>
              A comprehensive 13-week curriculum covering everything from ROS2
              fundamentals to cutting-edge VLA models
            </p>
            <div className={styles.moduleGrid}>
              {modules.map((module) => (
                <ModuleCard key={module.id} module={module} />
              ))}
            </div>
          </div>
        </section>
        <Features />
      </main>
    </Layout>
  );
}
