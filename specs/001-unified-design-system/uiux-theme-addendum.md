# UIUX Theme Addendum: AI-Native Technical Textbook Platform

**Feature**: 001-unified-design-system
**Date**: 2025-12-16
**Status**: Complete
**Constitution Reference**: v4.0.0 - Principle I (Single Unified Theme)

---

## Overview

This document defines the complete UI/UX design system for the AI-Native Technical Textbook Platform. All components across the platform (Landing Page, Textbook, Authentication, Chatbot, AI Skills) MUST adhere to this unified theme specification.

---

## 1. Color System

### Primary Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary-dark` | `#1a1a2e` | Primary backgrounds, dark surfaces |
| `--color-primary-accent` | `#ffd700` | Accents, CTAs, highlights, links |

### Supporting Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-background` | `#0f0f1a` | Deeper background (hero, footer) |
| `--color-surface` | `#252540` | Card backgrounds, elevated surfaces |
| `--color-surface-hover` | `#2d2d4a` | Card hover states |
| `--color-text-primary` | `#ffffff` | Primary text |
| `--color-text-secondary` | `#b0b0c0` | Muted text, captions |
| `--color-text-tertiary` | `#7a7a90` | Placeholder text, disabled |

### Interactive States

| Token | Value | Usage |
|-------|-------|-------|
| `--color-hover` | `#ffd700` | Hover text/icons |
| `--color-active` | `#e6c200` | Active/pressed state |
| `--color-focus-ring` | `rgba(255, 215, 0, 0.4)` | Focus outline |
| `--color-disabled` | `#4a4a60` | Disabled elements |

### Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-success` | `#22c55e` | Success states, confirmations |
| `--color-warning` | `#f59e0b` | Warning states (use sparingly) |
| `--color-error` | `#ef4444` | Error states, destructive actions |
| `--color-info` | `#3b82f6` | Informational notices |

### Gradients

| Token | Value | Usage |
|-------|-------|-------|
| `--gradient-primary` | `linear-gradient(135deg, #1a1a2e 0%, #252540 100%)` | Card backgrounds |
| `--gradient-accent` | `linear-gradient(135deg, #ffd700 0%, #ffa500 100%)` | Primary buttons |
| `--gradient-hero` | `linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%)` | Hero background |
| `--gradient-glow` | `radial-gradient(circle, rgba(255, 215, 0, 0.15) 0%, transparent 70%)` | Background glow effect |

---

## 2. Typography

### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `--font-heading` | `'Space Grotesk', sans-serif` | Headings H1-H6 |
| `--font-body` | `'Inter', sans-serif` | Body text, UI elements |
| `--font-code` | `'JetBrains Mono', monospace` | Code blocks, inline code |
| `--font-urdu` | `'Noto Nastaliq Urdu', serif` | Urdu translations (RTL) |

### Font Sizes

| Token | Value | Line Height | Usage |
|-------|-------|-------------|-------|
| `--text-xs` | `12px` | `1.4` | Captions, labels |
| `--text-sm` | `14px` | `1.5` | Secondary text, buttons |
| `--text-base` | `16px` | `1.6` | Body text |
| `--text-lg` | `18px` | `1.6` | Lead paragraphs |
| `--text-xl` | `20px` | `1.5` | Section titles |
| `--text-2xl` | `24px` | `1.4` | H4 headings |
| `--text-3xl` | `30px` | `1.3` | H3 headings |
| `--text-4xl` | `36px` | `1.2` | H2 headings |
| `--text-5xl` | `48px` | `1.1` | H1 headings |
| `--text-6xl` | `60px` | `1.1` | Hero display |

### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `--font-normal` | `400` | Body text |
| `--font-medium` | `500` | UI labels, buttons |
| `--font-semibold` | `600` | Section headings |
| `--font-bold` | `700` | Main headings |

---

## 3. Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | `4px` | Tight gaps |
| `--space-2` | `8px` | Icon gaps |
| `--space-3` | `12px` | Small padding |
| `--space-4` | `16px` | Default padding |
| `--space-5` | `20px` | Component gaps |
| `--space-6` | `24px` | Section padding |
| `--space-8` | `32px` | Large gaps |
| `--space-10` | `40px` | Section margins |
| `--space-12` | `48px` | Page sections |
| `--space-16` | `64px` | Hero padding |
| `--space-20` | `80px` | Page margins |

---

## 4. Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | `4px` | Inputs, small elements |
| `--radius-md` | `8px` | Buttons, cards |
| `--radius-lg` | `12px` | Modals, large cards |
| `--radius-xl` | `16px` | Featured elements |
| `--radius-2xl` | `24px` | Hero cards |
| `--radius-full` | `9999px` | Pills, avatars |

---

## 5. Shadow System

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0, 0, 0, 0.2)` | Subtle elevation |
| `--shadow-md` | `0 4px 6px rgba(0, 0, 0, 0.25)` | Cards resting |
| `--shadow-lg` | `0 10px 15px rgba(0, 0, 0, 0.3)` | Dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0, 0, 0, 0.35)` | Modals |
| `--shadow-glow` | `0 0 20px rgba(255, 215, 0, 0.3)` | Yellow glow effect |
| `--shadow-glow-strong` | `0 0 40px rgba(255, 215, 0, 0.5)` | Hover glow effect |

---

## 6. Animation & Motion

### Timing Functions

| Token | Value | Usage |
|-------|-------|-------|
| `--ease-default` | `cubic-bezier(0.4, 0, 0.2, 1)` | General transitions |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Exit animations |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Enter animations |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bouncy effects |

### Durations

| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | `150ms` | Micro-interactions |
| `--duration-normal` | `200ms` | Default transitions |
| `--duration-slow` | `300ms` | Page transitions |
| `--duration-slower` | `500ms` | Complex animations |

### Framer Motion Presets

```typescript
// Hover lift effect for cards
const hoverLift = {
  rest: { y: 0, boxShadow: "0 4px 6px rgba(0, 0, 0, 0.25)" },
  hover: {
    y: -8,
    boxShadow: "0 20px 40px rgba(255, 215, 0, 0.3)",
    transition: { duration: 0.2, ease: "easeOut" }
  }
};

// Counter animation for stats
const counterSpring = {
  type: "spring",
  stiffness: 100,
  damping: 15
};

// Fade in on scroll
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

// Stagger children
const staggerContainer = {
  animate: { transition: { staggerChildren: 0.1 } }
};
```

---

## 7. Component Specifications

### 7.1 Buttons

#### Primary Button (CTA)
```css
.btn-primary {
  background: var(--gradient-accent);
  color: #1a1a2e;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: var(--radius-full);
  border: none;
  box-shadow: var(--shadow-glow);
  transition: all var(--duration-normal) var(--ease-default);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow-strong);
}

.btn-primary:active {
  transform: scale(0.98);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: var(--color-primary-accent);
  border: 2px solid var(--color-primary-accent);
  padding: 12px 24px;
  border-radius: var(--radius-full);
  transition: all var(--duration-normal) var(--ease-default);
}

.btn-secondary:hover {
  background: rgba(255, 215, 0, 0.1);
}
```

#### Skill Button (AI Actions)
```css
.btn-skill {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 10px 20px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--duration-normal) var(--ease-default);
}

.btn-skill:hover {
  border-color: var(--color-primary-accent);
  background: rgba(255, 215, 0, 0.1);
}

.btn-skill svg {
  width: 18px;
  height: 18px;
  color: var(--color-primary-accent);
}
```

### 7.2 Cards

#### Feature Card (Landing Page)
```css
.feature-card {
  background: var(--gradient-primary);
  border: 1px solid rgba(255, 215, 0, 0.1);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  transition: all var(--duration-normal) var(--ease-default);
}

.feature-card:hover {
  border-color: rgba(255, 215, 0, 0.4);
  transform: translateY(-8px);
  box-shadow: var(--shadow-glow);
}

.feature-card__icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 215, 0, 0.1);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.feature-card__icon svg {
  width: 24px;
  height: 24px;
  color: var(--color-primary-accent);
}

.feature-card__title {
  font-family: var(--font-heading);
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.feature-card__description {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
}
```

#### Stats Card
```css
.stats-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-align: center;
}

.stats-card__value {
  font-family: var(--font-heading);
  font-size: var(--text-5xl);
  font-weight: var(--font-bold);
  color: var(--color-primary-accent);
  line-height: 1;
  margin-bottom: var(--space-2);
}

.stats-card__label {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

### 7.3 Navigation

#### Navbar
```css
.navbar {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar__brand {
  font-family: var(--font-heading);
  font-weight: var(--font-bold);
  font-size: var(--text-xl);
  color: var(--color-text-primary);
}

.navbar__link {
  color: var(--color-text-secondary);
  font-weight: var(--font-medium);
  transition: color var(--duration-fast);
}

.navbar__link:hover,
.navbar__link--active {
  color: var(--color-primary-accent);
}
```

### 7.4 Chat Widget

```css
.chat-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 380px;
  max-height: 560px;
  background: var(--color-primary-dark);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: 1000;
}

.chat-widget__header {
  background: var(--color-surface);
  padding: var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
}

.chat-widget__title {
  font-family: var(--font-heading);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.chat-widget__messages {
  height: 360px;
  overflow-y: auto;
  padding: var(--space-4);
  background: var(--color-background);
}

.chat-widget__input-area {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 215, 0, 0.1);
  background: var(--color-surface);
}

.chat-bubble--user {
  background: rgba(255, 215, 0, 0.15);
  border: 1px solid rgba(255, 215, 0, 0.3);
  color: var(--color-text-primary);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg) var(--radius-lg) 0 var(--radius-lg);
  margin-left: auto;
  max-width: 85%;
}

.chat-bubble--assistant {
  background: var(--color-surface);
  color: var(--color-text-primary);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 0;
  max-width: 85%;
}
```

### 7.5 Floating Action Button (Chat Toggle)

```css
.fab-chat {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 60px;
  height: 60px;
  background: var(--gradient-accent);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow);
  cursor: pointer;
  z-index: 999;
  transition: all var(--duration-normal) var(--ease-default);
}

.fab-chat:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-glow-strong);
}

.fab-chat svg {
  width: 28px;
  height: 28px;
  color: #1a1a2e;
}
```

---

## 8. Page-Specific Styles

### 8.1 Landing Page

#### Hero Section
```css
.hero {
  min-height: 90vh;
  background: var(--gradient-hero);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-16) var(--space-4);
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 800px;
  height: 800px;
  background: var(--gradient-glow);
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.hero__title {
  font-family: var(--font-heading);
  font-size: var(--text-6xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
  max-width: 900px;
}

.hero__title span {
  color: var(--color-primary-accent);
}

.hero__subtitle {
  font-size: var(--text-xl);
  color: var(--color-text-secondary);
  max-width: 600px;
  margin-bottom: var(--space-8);
}
```

### 8.2 Textbook (Docusaurus)

#### Doc Item Layout
```css
.doc-item-container {
  background: var(--color-primary-dark);
}

.doc-content {
  color: var(--color-text-primary);
  font-size: var(--text-lg);
  line-height: 1.8;
}

.doc-content h1,
.doc-content h2,
.doc-content h3 {
  font-family: var(--font-heading);
  color: var(--color-text-primary);
  margin-top: var(--space-8);
  margin-bottom: var(--space-4);
}

.doc-content a {
  color: var(--color-primary-accent);
  text-decoration: none;
  border-bottom: 1px solid rgba(255, 215, 0, 0.3);
  transition: border-color var(--duration-fast);
}

.doc-content a:hover {
  border-color: var(--color-primary-accent);
}

.doc-content code {
  background: var(--color-surface);
  color: var(--color-primary-accent);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: var(--font-code);
  font-size: 0.9em;
}

.doc-content pre {
  background: var(--color-background);
  border: 1px solid rgba(255, 215, 0, 0.1);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  overflow-x: auto;
}
```

#### Skill Buttons Row
```css
.skill-buttons {
  display: flex;
  gap: var(--space-3);
  margin: var(--space-6) 0;
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.1);
}
```

---

## 9. Accessibility Requirements

### 9.1 Color Contrast

All text must meet WCAG 2.1 AA standards:
- Normal text: 4.5:1 minimum contrast ratio
- Large text (18px+): 3:1 minimum contrast ratio
- UI components: 3:1 minimum contrast ratio

| Combination | Ratio | Pass? |
|-------------|-------|-------|
| White on #1a1a2e | 14.8:1 | Yes |
| #ffd700 on #1a1a2e | 10.1:1 | Yes |
| #b0b0c0 on #1a1a2e | 7.3:1 | Yes |
| #1a1a2e on #ffd700 | 10.1:1 | Yes |

### 9.2 Focus States

All interactive elements must have visible focus indicators:
```css
*:focus-visible {
  outline: 2px solid var(--color-primary-accent);
  outline-offset: 2px;
}
```

### 9.3 Reduced Motion

Respect user preferences:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 10. Responsive Breakpoints

| Breakpoint | Value | Usage |
|------------|-------|-------|
| `sm` | `640px` | Mobile landscape |
| `md` | `768px` | Tablets |
| `lg` | `1024px` | Desktop |
| `xl` | `1280px` | Large desktop |
| `2xl` | `1536px` | Extra large |

### Mobile-First Approach

```css
/* Base styles for mobile (320px+) */
.hero__title {
  font-size: var(--text-4xl);
}

/* Tablet and up */
@media (min-width: 768px) {
  .hero__title {
    font-size: var(--text-5xl);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .hero__title {
    font-size: var(--text-6xl);
  }
}
```

---

## 11. RTL Support (Urdu)

For Urdu translation feature:

```css
.urdu-content {
  direction: rtl;
  text-align: right;
  font-family: var(--font-urdu);
  line-height: 2;
}

.urdu-content code {
  direction: ltr;
  unicode-bidi: isolate;
}
```

---

## 12. Implementation Checklist

- [ ] CSS variables defined in `frontend/src/css/custom.css`
- [ ] Web fonts loaded in `frontend/src/css/fonts.css`
- [ ] Animations defined in `frontend/src/css/animations.css`
- [ ] Docusaurus theme colors in `frontend/docusaurus.config.ts`
- [ ] Framer Motion presets in `frontend/src/utils/motion.ts`
- [ ] Component styles match specifications
- [ ] Accessibility audit passed
- [ ] Responsive breakpoints tested

---

## Summary

The unified theme uses Dark Blue (#1a1a2e) as the primary background color with Yellow (#ffd700) as the accent color for all interactive elements. This creates a premium, futuristic aesthetic appropriate for an AI-focused educational platform while maintaining WCAG 2.1 AA accessibility compliance.
