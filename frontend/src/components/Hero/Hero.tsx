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
  title = 'Learn Physical AI & Humanoid Robotics',
  tagline = 'An AI-native textbook for the future of intelligent machines. Master robotics with ROS2, simulation, and cutting-edge AI techniques.',
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
              viewBox="0 0 200 280"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className={styles.robotSvg}
            >
              {/* Glow effects */}
              <defs>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <linearGradient id="bodyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ffd700" stopOpacity="0.3"/>
                  <stop offset="100%" stopColor="#1a1a2e" stopOpacity="0.8"/>
                </linearGradient>
                <linearGradient id="accentGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#ffd700"/>
                  <stop offset="100%" stopColor="#ffa500"/>
                </linearGradient>
              </defs>

              {/* Head - Helmet style */}
              <ellipse cx="100" cy="45" rx="35" ry="40" fill="#252540" stroke="#ffd700" strokeWidth="2"/>
              <ellipse cx="100" cy="42" rx="30" ry="32" fill="#1a1a2e"/>

              {/* Visor/Face plate */}
              <path d="M70 35 Q100 25 130 35 L125 55 Q100 65 75 55 Z" fill="#0f0f1a" stroke="#ffd700" strokeWidth="1.5"/>

              {/* Eyes - glowing */}
              <ellipse cx="85" cy="42" rx="8" ry="5" fill="#ffd700" filter="url(#glow)" className={styles.eyeLeft}/>
              <ellipse cx="115" cy="42" rx="8" ry="5" fill="#ffd700" filter="url(#glow)" className={styles.eyeRight}/>

              {/* Antenna */}
              <line x1="100" y1="5" x2="100" y2="20" stroke="#ffd700" strokeWidth="2"/>
              <circle cx="100" cy="5" r="4" fill="#ffd700" filter="url(#glow)"/>

              {/* Neck */}
              <rect x="90" y="82" width="20" height="15" fill="#252540" stroke="#ffd700" strokeWidth="1"/>
              <line x1="95" y1="85" x2="95" y2="95" stroke="#ffd700" strokeWidth="1" opacity="0.5"/>
              <line x1="100" y1="85" x2="100" y2="95" stroke="#ffd700" strokeWidth="1" opacity="0.5"/>
              <line x1="105" y1="85" x2="105" y2="95" stroke="#ffd700" strokeWidth="1" opacity="0.5"/>

              {/* Torso - Chest plate */}
              <path d="M60 100 L140 100 L145 180 L55 180 Z" fill="#1a1a2e" stroke="#ffd700" strokeWidth="2"/>
              <path d="M70 105 L130 105 L135 170 L65 170 Z" fill="#252540"/>

              {/* Chest core - Arc reactor style */}
              <circle cx="100" cy="130" r="18" fill="#0f0f1a" stroke="#ffd700" strokeWidth="2"/>
              <circle cx="100" cy="130" r="12" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1"/>
              <circle cx="100" cy="130" r="6" fill="#ffd700" filter="url(#glow)" className={styles.core}/>

              {/* Chest details */}
              <line x1="75" y1="150" x2="90" y2="150" stroke="#ffd700" strokeWidth="1" opacity="0.6"/>
              <line x1="110" y1="150" x2="125" y2="150" stroke="#ffd700" strokeWidth="1" opacity="0.6"/>
              <line x1="75" y1="160" x2="85" y2="160" stroke="#ffd700" strokeWidth="1" opacity="0.4"/>
              <line x1="115" y1="160" x2="125" y2="160" stroke="#ffd700" strokeWidth="1" opacity="0.4"/>

              {/* Shoulders */}
              <ellipse cx="45" cy="110" rx="18" ry="12" fill="#252540" stroke="#ffd700" strokeWidth="2"/>
              <ellipse cx="155" cy="110" rx="18" ry="12" fill="#252540" stroke="#ffd700" strokeWidth="2"/>
              <circle cx="45" cy="110" r="5" fill="#ffd700" opacity="0.6"/>
              <circle cx="155" cy="110" r="5" fill="#ffd700" opacity="0.6"/>

              {/* Left Arm */}
              <rect x="25" y="115" width="18" height="45" rx="5" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1.5"/>
              <rect x="27" y="165" width="14" height="35" rx="4" fill="#252540" stroke="#ffd700" strokeWidth="1"/>
              <circle cx="34" cy="130" r="3" fill="#ffd700" opacity="0.5"/>

              {/* Left Hand */}
              <rect x="28" y="202" width="12" height="15" rx="3" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1"/>
              <line x1="31" y1="217" x2="31" y2="225" stroke="#ffd700" strokeWidth="2"/>
              <line x1="34" y1="217" x2="34" y2="227" stroke="#ffd700" strokeWidth="2"/>
              <line x1="37" y1="217" x2="37" y2="225" stroke="#ffd700" strokeWidth="2"/>

              {/* Right Arm */}
              <rect x="157" y="115" width="18" height="45" rx="5" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1.5"/>
              <rect x="159" y="165" width="14" height="35" rx="4" fill="#252540" stroke="#ffd700" strokeWidth="1"/>
              <circle cx="166" cy="130" r="3" fill="#ffd700" opacity="0.5"/>

              {/* Right Hand */}
              <rect x="160" y="202" width="12" height="15" rx="3" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1"/>
              <line x1="163" y1="217" x2="163" y2="225" stroke="#ffd700" strokeWidth="2"/>
              <line x1="166" y1="217" x2="166" y2="227" stroke="#ffd700" strokeWidth="2"/>
              <line x1="169" y1="217" x2="169" y2="225" stroke="#ffd700" strokeWidth="2"/>

              {/* Waist/Hip */}
              <rect x="65" y="180" width="70" height="20" rx="5" fill="#252540" stroke="#ffd700" strokeWidth="1.5"/>
              <circle cx="100" cy="190" r="4" fill="#ffd700" opacity="0.6"/>

              {/* Left Leg */}
              <rect x="68" y="200" width="22" height="50" rx="5" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1.5"/>
              <rect x="70" y="252" width="18" height="20" rx="3" fill="#252540" stroke="#ffd700" strokeWidth="1"/>
              <circle cx="79" cy="220" r="3" fill="#ffd700" opacity="0.4"/>

              {/* Left Foot */}
              <path d="M65 272 L93 272 L95 278 L63 278 Z" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1"/>

              {/* Right Leg */}
              <rect x="110" y="200" width="22" height="50" rx="5" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1.5"/>
              <rect x="112" y="252" width="18" height="20" rx="3" fill="#252540" stroke="#ffd700" strokeWidth="1"/>
              <circle cx="121" cy="220" r="3" fill="#ffd700" opacity="0.4"/>

              {/* Right Foot */}
              <path d="M107 272 L135 272 L137 278 L105 278 Z" fill="#1a1a2e" stroke="#ffd700" strokeWidth="1"/>

              {/* Circuit patterns on body */}
              <path d="M80 110 L80 120 L75 120" stroke="#ffd700" strokeWidth="0.5" opacity="0.4" fill="none"/>
              <path d="M120 110 L120 120 L125 120" stroke="#ffd700" strokeWidth="0.5" opacity="0.4" fill="none"/>
            </svg>
          </div>
        </div>
      </div>
    </header>
  );
}
