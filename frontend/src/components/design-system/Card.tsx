import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import styles from './Card.module.css';

export type CardVariant = 'default' | 'elevated' | 'outlined' | 'glass';

export interface CardProps extends Omit<HTMLMotionProps<'div'>, 'children'> {
  children: React.ReactNode;
  variant?: CardVariant;
  hoverable?: boolean;
  glow?: boolean;
  glowColor?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  header?: React.ReactNode;
  footer?: React.ReactNode;
}

const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  hoverable = false,
  glow = false,
  glowColor = 'rgba(6, 182, 212, 0.3)',
  padding = 'md',
  header,
  footer,
  className = '',
  style,
  ...props
}) => {
  const cardClasses = [
    styles.card,
    styles[variant],
    styles[`padding-${padding}`],
    hoverable && styles.hoverable,
    glow && styles.glow,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const hoverAnimation = hoverable
    ? {
        whileHover: {
          y: -8,
          scale: 1.02,
          transition: { duration: 0.3, ease: 'easeOut' as const },
        },
      }
    : {};

  return (
    <motion.div
      className={cardClasses}
      style={{
        ...style,
        '--glow-color': glow ? glowColor : 'transparent',
      } as React.CSSProperties}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      {...hoverAnimation}
      {...props}
    >
      {header && <div className={styles.header}>{header}</div>}
      <div className={styles.content}>{children}</div>
      {footer && <div className={styles.footer}>{footer}</div>}
    </motion.div>
  );
};

export default Card;
