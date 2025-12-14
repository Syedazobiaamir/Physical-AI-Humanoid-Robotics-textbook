import { useState, useEffect, useCallback } from 'react';

interface ScrollPosition {
  x: number;
  y: number;
}

interface UseScrollPositionOptions {
  /** Throttle scroll events by this many milliseconds */
  throttle?: number;
  /** Initial scroll position (useful for SSR) */
  initialPosition?: ScrollPosition;
}

/**
 * Hook to track scroll position with throttling
 *
 * @example
 * ```tsx
 * const { y } = useScrollPosition();
 * const isScrolled = y > 100;
 * ```
 */
export function useScrollPosition(options: UseScrollPositionOptions = {}): ScrollPosition {
  const { throttle = 16, initialPosition = { x: 0, y: 0 } } = options;

  const [position, setPosition] = useState<ScrollPosition>(initialPosition);

  const handleScroll = useCallback(() => {
    setPosition({
      x: window.scrollX,
      y: window.scrollY,
    });
  }, []);

  useEffect(() => {
    // Set initial position
    if (typeof window !== 'undefined') {
      setPosition({
        x: window.scrollX,
        y: window.scrollY,
      });
    }

    // Throttled scroll handler
    let timeoutId: ReturnType<typeof setTimeout> | null = null;
    let lastScrollTime = 0;

    const throttledHandler = () => {
      const now = Date.now();
      const timeSinceLastScroll = now - lastScrollTime;

      if (timeSinceLastScroll >= throttle) {
        handleScroll();
        lastScrollTime = now;
      } else if (!timeoutId) {
        timeoutId = setTimeout(() => {
          handleScroll();
          lastScrollTime = Date.now();
          timeoutId = null;
        }, throttle - timeSinceLastScroll);
      }
    };

    window.addEventListener('scroll', throttledHandler, { passive: true });

    return () => {
      window.removeEventListener('scroll', throttledHandler);
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [handleScroll, throttle]);

  return position;
}

/**
 * Hook to detect if page has scrolled past a threshold
 *
 * @example
 * ```tsx
 * const isScrolled = useIsScrolled(100);
 * // Returns true when scrolled more than 100px
 * ```
 */
export function useIsScrolled(threshold: number = 50): boolean {
  const { y } = useScrollPosition();
  return y > threshold;
}

/**
 * Hook to get scroll direction
 *
 * @example
 * ```tsx
 * const direction = useScrollDirection();
 * // Returns 'up', 'down', or null
 * ```
 */
export function useScrollDirection(): 'up' | 'down' | null {
  const [direction, setDirection] = useState<'up' | 'down' | null>(null);
  const [lastY, setLastY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentY = window.scrollY;

      if (currentY > lastY && currentY > 50) {
        setDirection('down');
      } else if (currentY < lastY) {
        setDirection('up');
      }

      setLastY(currentY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastY]);

  return direction;
}

/**
 * Hook to calculate scroll progress (0 to 1)
 *
 * @example
 * ```tsx
 * const progress = useScrollProgress();
 * // Returns a value between 0 and 1 representing scroll progress
 * ```
 */
export function useScrollProgress(): number {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      const scrollY = window.scrollY;

      const scrollableHeight = documentHeight - windowHeight;
      const currentProgress = scrollableHeight > 0 ? scrollY / scrollableHeight : 0;

      setProgress(Math.min(1, Math.max(0, currentProgress)));
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Initial calculation

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return progress;
}

export default useScrollPosition;
