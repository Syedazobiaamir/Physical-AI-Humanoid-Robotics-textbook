import React from 'react';
import Link from '@docusaurus/Link';
import styles from './Hero.module.css';

interface HeroProps {
  title?: string;
  tagline?: string;
  ctaText?: string;
  ctaLink?: string;
}

export default function Hero({
  title = 'Physical AI & Humanoid Robotics',
  tagline = 'Master robotics with ROS2, simulation, and AI-powered learning. An interactive textbook for the next generation of robotics engineers.',
  ctaText = 'Start Learning',
  ctaLink = '/docs/intro',
}: HeroProps): JSX.Element {
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>{title}</h1>
          <p className={styles.heroTagline}>{tagline}</p>
          <div className={styles.heroButtons}>
            <Link
              className={styles.heroCta}
              to={ctaLink}
            >
              {ctaText}
            </Link>
            <Link
              className={styles.heroSecondary}
              to="/docs/module-1/week-1-intro"
            >
              View Curriculum
            </Link>
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.robotIcon}>
            <svg
              viewBox="0 0 100 100"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className={styles.robotSvg}
            >
              <circle cx="50" cy="30" r="20" stroke="currentColor" strokeWidth="3" />
              <circle cx="43" cy="27" r="3" fill="currentColor" />
              <circle cx="57" cy="27" r="3" fill="currentColor" />
              <path d="M44 35 Q50 40 56 35" stroke="currentColor" strokeWidth="2" fill="none" />
              <rect x="35" y="52" width="30" height="35" rx="5" stroke="currentColor" strokeWidth="3" />
              <line x1="35" y1="60" x2="25" y2="75" stroke="currentColor" strokeWidth="3" />
              <line x1="65" y1="60" x2="75" y2="75" stroke="currentColor" strokeWidth="3" />
              <line x1="42" y1="87" x2="42" y2="98" stroke="currentColor" strokeWidth="3" />
              <line x1="58" y1="87" x2="58" y2="98" stroke="currentColor" strokeWidth="3" />
              <line x1="50" y1="10" x2="50" y2="0" stroke="currentColor" strokeWidth="2" />
              <circle cx="50" cy="0" r="3" fill="currentColor" />
            </svg>
          </div>
        </div>
      </div>
    </header>
  );
}
