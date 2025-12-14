import React from 'react';
import { motion } from 'framer-motion';
import Link from '@docusaurus/Link';
import styles from './CourseRoadmap.module.css';

interface RoadmapItem {
  id: string;
  week: string;
  title: string;
  description: string;
  topics: string[];
  link: string;
  color: string;
  icon: React.ReactNode;
}

const roadmapData: RoadmapItem[] = [
  {
    id: 'week-1-3',
    week: 'Weeks 1-3',
    title: 'ROS2 Fundamentals',
    description: 'Master the Robot Operating System 2 architecture, nodes, topics, services, and actions.',
    topics: ['ROS2 Architecture', 'Nodes & Topics', 'Services & Actions', 'Launch Files'],
    link: '/docs/module-1/week-1-intro',
    color: '#3B82F6',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    ),
  },
  {
    id: 'week-4-6',
    week: 'Weeks 4-6',
    title: 'Simulation Mastery',
    description: 'Build and test robots in virtual environments with Gazebo and Unity.',
    topics: ['Gazebo Physics', 'URDF/SDF Models', 'Sensor Simulation', 'Unity Integration'],
    link: '/docs/module-2/week-4-sensors',
    color: '#8B5CF6',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <line x1="8" y1="21" x2="16" y2="21" />
        <line x1="12" y1="17" x2="12" y2="21" />
      </svg>
    ),
  },
  {
    id: 'week-7-9',
    week: 'Weeks 7-9',
    title: 'NVIDIA Isaac Platform',
    description: 'Leverage AI-powered robotics tools for perception, navigation, and manipulation.',
    topics: ['Isaac Sim', 'Perception Pipelines', 'Navigation Stack', 'Isaac ROS'],
    link: '/docs/module-3/week-7-kinematics',
    color: '#EC4899',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polygon points="12 2 2 7 12 12 22 7 12 2" />
        <polyline points="2 17 12 22 22 17" />
        <polyline points="2 12 12 17 22 12" />
      </svg>
    ),
  },
  {
    id: 'week-10-12',
    week: 'Weeks 10-12',
    title: 'Vision-Language-Action Models',
    description: 'Implement cutting-edge VLA models combining vision, language, and action.',
    topics: ['VLA Architecture', 'Multi-modal Learning', 'Robot Learning', 'Deployment'],
    link: '/docs/module-4/week-10-reinforcement-learning',
    color: '#F59E0B',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
      </svg>
    ),
  },
  {
    id: 'week-13',
    week: 'Week 13',
    title: 'Capstone Project',
    description: 'Integrate everything into a complete humanoid robot application.',
    topics: ['System Integration', 'Real Hardware', 'Performance Tuning', 'Demo'],
    link: '/docs/module-4/week-13-final-project',
    color: '#10B981',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
        <path d="M19 6v12c0 1-1 2-2 2H7c-1 0-2-1-2-2V6c0-1 1-2 2-2h10c1 0 2 1 2 2Z" />
        <path d="M12 2v2" />
        <path d="M12 20v2" />
      </svg>
    ),
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -50 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.5,
      ease: 'easeOut' as const,
    },
  },
};

const CourseRoadmap: React.FC = () => {
  return (
    <section className={styles.roadmap}>
      <div className={styles.container}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <h2 className={styles.title}>Your Learning Journey</h2>
          <p className={styles.subtitle}>
            A structured 13-week curriculum taking you from ROS2 basics to advanced VLA models
          </p>
        </motion.div>

        <motion.div
          className={styles.timeline}
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
        >
          {/* Timeline line */}
          <div className={styles.timelineLine} />

          {roadmapData.map((item, index) => (
            <motion.div
              key={item.id}
              className={`${styles.timelineItem} ${index % 2 === 0 ? styles.left : styles.right}`}
              variants={itemVariants}
            >
              {/* Timeline dot */}
              <motion.div
                className={styles.timelineDot}
                style={{ backgroundColor: item.color }}
                whileHover={{ scale: 1.3 }}
                transition={{ duration: 0.2 }}
              />

              {/* Content card */}
              <Link to={item.link} className={styles.cardLink}>
                <motion.div
                  className={styles.card}
                  whileHover={{
                    y: -5,
                    boxShadow: `0 10px 40px ${item.color}40`,
                  }}
                  transition={{ duration: 0.3 }}
                >
                  <div className={styles.cardHeader}>
                    <div
                      className={styles.iconWrapper}
                      style={{ backgroundColor: `${item.color}20`, color: item.color }}
                    >
                      {item.icon}
                    </div>
                    <span className={styles.week} style={{ color: item.color }}>
                      {item.week}
                    </span>
                  </div>
                  <h3 className={styles.cardTitle}>{item.title}</h3>
                  <p className={styles.cardDescription}>{item.description}</p>
                  <div className={styles.topics}>
                    {item.topics.map((topic) => (
                      <span
                        key={topic}
                        className={styles.topic}
                        style={{ borderColor: `${item.color}40`, color: item.color }}
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </motion.div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default CourseRoadmap;
