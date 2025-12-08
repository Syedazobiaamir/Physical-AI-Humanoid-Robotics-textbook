import React from 'react';
import Link from '@docusaurus/Link';
import styles from './ModuleCard.module.css';

export interface ModuleData {
  id: string;
  title: string;
  description: string;
  weeks: string;
  icon: React.ReactNode;
  link: string;
  color?: string;
}

interface ModuleCardProps {
  module: ModuleData;
}

export default function ModuleCard({ module }: ModuleCardProps): JSX.Element {
  return (
    <Link to={module.link} className={styles.card}>
      <div
        className={styles.cardIcon}
        style={{ backgroundColor: module.color || '#25c2a0' }}
      >
        {module.icon}
      </div>
      <div className={styles.cardContent}>
        <h3 className={styles.cardTitle}>{module.title}</h3>
        <p className={styles.cardDescription}>{module.description}</p>
        <span className={styles.cardWeeks}>{module.weeks}</span>
      </div>
      <div className={styles.cardArrow}>
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </div>
    </Link>
  );
}

// Module icons as SVG components
export const ROS2Icon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
  </svg>
);

export const SimulationIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
    <path d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zM9 8h2v8H9zm4 4h2v4h-2zm-8 2h2v2H5z" />
  </svg>
);

export const IsaacIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
    <path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71L12 2z" />
  </svg>
);

export const VLAIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
    <path d="M12 3c-4.97 0-9 4.03-9 9v7c0 1.1.9 2 2 2h4v-8H5v-1c0-3.87 3.13-7 7-7s7 3.13 7 7v1h-4v8h4c1.1 0 2-.9 2-2v-7c0-4.97-4.03-9-9-9z" />
  </svg>
);

export const CapstoneIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z" />
  </svg>
);
