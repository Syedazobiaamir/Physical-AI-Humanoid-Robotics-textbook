/**
 * Design System Tokens
 * Based on the Physical AI & Humanoid Robotics Textbook design system
 */

// Color tokens
export interface ColorTokens {
  // Primary colors
  primary: {
    main: string;
    light: string;
    dark: string;
    contrastText: string;
  };
  // Secondary colors
  secondary: {
    main: string;
    light: string;
    dark: string;
    contrastText: string;
  };
  // Accent colors
  accent: {
    cyan: string;
    purple: string;
    pink: string;
    amber: string;
    emerald: string;
  };
  // Background colors
  background: {
    primary: string;
    secondary: string;
    tertiary: string;
    surface: string;
  };
  // Text colors
  text: {
    primary: string;
    secondary: string;
    muted: string;
    inverse: string;
  };
  // Status colors
  status: {
    success: string;
    warning: string;
    error: string;
    info: string;
  };
}

// Typography tokens
export interface TypographyTokens {
  fontFamily: {
    heading: string;
    body: string;
    mono: string;
  };
  fontSize: {
    xs: string;
    sm: string;
    base: string;
    lg: string;
    xl: string;
    '2xl': string;
    '3xl': string;
    '4xl': string;
    '5xl': string;
  };
  fontWeight: {
    normal: number;
    medium: number;
    semibold: number;
    bold: number;
  };
  lineHeight: {
    tight: number;
    normal: number;
    relaxed: number;
  };
}

// Spacing tokens
export interface SpacingTokens {
  0: string;
  1: string;
  2: string;
  3: string;
  4: string;
  5: string;
  6: string;
  8: string;
  10: string;
  12: string;
  16: string;
  20: string;
  24: string;
}

// Border radius tokens
export interface BorderRadiusTokens {
  none: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
  full: string;
}

// Shadow tokens
export interface ShadowTokens {
  sm: string;
  md: string;
  lg: string;
  xl: string;
  glow: string;
}

// Animation tokens
export interface AnimationTokens {
  duration: {
    fast: string;
    normal: string;
    slow: string;
  };
  easing: {
    default: string;
    ease: string;
    spring: string;
  };
}

// Complete design tokens interface
export interface DesignTokens {
  colors: ColorTokens;
  typography: TypographyTokens;
  spacing: SpacingTokens;
  borderRadius: BorderRadiusTokens;
  shadows: ShadowTokens;
  animation: AnimationTokens;
}

// Default design tokens
export const designTokens: DesignTokens = {
  colors: {
    primary: {
      main: '#2e8555',
      light: '#3cad6e',
      dark: '#205d3b',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#25c2a0',
      light: '#4fddbf',
      dark: '#1a8870',
      contrastText: '#ffffff',
    },
    accent: {
      cyan: '#06b6d4',
      purple: '#8b5cf6',
      pink: '#ec4899',
      amber: '#f59e0b',
      emerald: '#10b981',
    },
    background: {
      primary: '#0f172a',
      secondary: '#1e293b',
      tertiary: '#334155',
      surface: '#ffffff',
    },
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
      muted: '#64748b',
      inverse: '#0f172a',
    },
    status: {
      success: '#22c55e',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
  },
  typography: {
    fontFamily: {
      heading: "'Space Grotesk', sans-serif",
      body: "'Inter', sans-serif",
      mono: "'JetBrains Mono', monospace",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  spacing: {
    0: '0',
    1: '0.25rem',
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
    5: '1.25rem',
    6: '1.5rem',
    8: '2rem',
    10: '2.5rem',
    12: '3rem',
    16: '4rem',
    20: '5rem',
    24: '6rem',
  },
  borderRadius: {
    none: '0',
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    glow: '0 0 20px rgba(6, 182, 212, 0.3)',
  },
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      ease: 'ease-in-out',
      spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    },
  },
};

export default designTokens;
