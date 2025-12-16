# Research: AI-Native Technical Textbook Platform

**Feature**: 001-unified-design-system
**Date**: 2025-12-15 (Updated)
**Status**: Complete

## Overview

This document captures research findings for technology choices, integration patterns, and best practices for the AI-Native Technical Textbook Platform with unified Dark Blue + Yellow theme.

---

## 1. Frontend Architecture: Docusaurus + Next.js Components

### Decision
Use Docusaurus 3.x for the textbook with React 18 components shared with Next.js landing page.

### Rationale
- Docusaurus excels at documentation/textbook content with MDX
- React components can be shared between Docusaurus and landing page
- Unified theme system through shared CSS variables
- Both frameworks deploy seamlessly to Vercel

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Next.js only | Less optimized for documentation-heavy content |
| Gatsby | Slower builds, less active maintenance |
| Astro | Less mature MDX ecosystem for educational content |

### Integration Pattern
```text
frontend/
├── src/components/    # Shared React components (theme, chatbot)
├── src/theme/         # Docusaurus theme overrides
└── shared/theme-tokens.json  # CSS variables for both
```

---

## 2. Design System: Dark Blue + Yellow Theme

### Decision
Implement unified Dark Blue (#1a1a2e) + Yellow (#ffd700) brand across all components per Constitution Principle I.

### Rationale
- Consistent brand identity across Landing, Book, Auth, Chatbot
- High contrast for accessibility (WCAG 2.1 AA)
- Dark theme reduces eye strain for educational reading
- Yellow accents for call-to-action visibility

### Design Tokens Structure
```css
:root {
  /* Primary Colors */
  --color-primary-dark: #1a1a2e;      /* Dark Blue - backgrounds */
  --color-primary-accent: #ffd700;    /* Yellow - accents, CTAs */

  /* Supporting Colors */
  --color-background: #0f0f1a;        /* Darker background variant */
  --color-surface: #252540;           /* Card backgrounds */
  --color-text-primary: #ffffff;      /* Primary text */
  --color-text-secondary: #b0b0c0;    /* Muted text */

  /* Interactive States */
  --color-hover: #ffd700;             /* Yellow hover */
  --color-focus: rgba(255, 215, 0, 0.3); /* Yellow focus ring */

  /* Typography */
  --font-heading: 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-code: 'JetBrains Mono', monospace;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
}
```

---

## 3. Animation Library: Framer Motion

### Decision
Use Framer Motion for all UI animations (hover effects, page transitions, stats counters).

### Rationale
- Declarative API integrates well with React
- Hardware-accelerated for smooth 60fps
- Built-in gesture support for interactive elements
- SSR-compatible for Docusaurus static generation

### Key Animation Patterns
```tsx
// Stats card counter animation
<motion.span animate={{ opacity: 1 }} initial={{ opacity: 0 }}>
  {count.toLocaleString()}
</motion.span>

// Feature card hover
<motion.div whileHover={{ y: -8, boxShadow: "0 8px 30px rgba(255, 215, 0, 0.2)" }}>
  <FeatureCard />
</motion.div>
```

---

## 4. Authentication: Clerk

### Decision
Use Clerk for authentication per Constitution v4.0.0 Principle IV.

### Rationale
- Constitution mandates Clerk as auth provider
- Pre-built UI components match any theme
- Built-in session management with 7+ day persistence
- Easy to collect user background during signup

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Better-Auth | Constitution v4.0.0 specifies Clerk |
| Auth0 | Higher cost, more complex setup |
| Custom auth | Security risk, longer development |

### User Background Collection Flow
1. User clicks "Sign Up" → Clerk handles email/password
2. After signup, redirect to onboarding form
3. Collect: software_level, hardware_exposure, robotics_experience
4. Store in Neon Postgres linked to Clerk user_id

---

## 5. RAG Backend: FastAPI + Qdrant + Gemini

### Decision
Use FastAPI for API endpoints, Qdrant for vector search, and Gemini API for response generation.

### Rationale
- **FastAPI**: Async-native, automatic OpenAPI docs, Python AI/ML ecosystem
- **Qdrant**: Purpose-built for vectors, free cloud tier, REST API
- **Gemini**: Strong reasoning for educational content, specified in requirements

### RAG Pipeline
```
User Question → Text Embedding → Qdrant Search (top-5) →
Context Assembly → Gemini Prompt → Response with Sources
```

### Embedding Strategy
- Chunk textbook by section (~500 tokens)
- Include chapter/module metadata with vectors
- Cosine similarity search, k=5

---

## 6. AI Skills Architecture

### Decision
Implement AI features as modular skills per Constitution Principle II (no autonomous agents).

### Rationale
- Skills have defined inputs/outputs/errors
- Easy to test independently
- Predictable behavior for users
- Graceful degradation when services fail

### Skill Definitions
| Skill | Input | Output | Error Handling |
|-------|-------|--------|----------------|
| Book Content | question, user_profile | RAG response | Fallback to keyword search |
| Context Selection | question, selected_text | Scoped response | Show "select text" prompt |
| Personalization | content, profile | Adapted content | Return original content |
| Translation | content, target_lang | Translated content | Show original with error |

### Skill Interface
```python
class Skill(ABC):
    @abstractmethod
    async def execute(self, input: SkillInput) -> SkillOutput:
        pass

@dataclass
class SkillOutput:
    success: bool
    data: Optional[str]
    error: Optional[str]
```

---

## 7. Database: Neon Serverless Postgres

### Decision
Use Neon Serverless Postgres for user profiles, personalization preferences, and statistics.

### Rationale
- Serverless scales to zero (cost-effective)
- PostgreSQL standard (familiar SQL)
- Built-in connection pooling
- Free tier handles 100+ concurrent users

### Schema Updates
```sql
-- Users (linked to Clerk)
users (
  id VARCHAR PRIMARY KEY,        -- Clerk user_id
  email VARCHAR UNIQUE NOT NULL,
  name VARCHAR,
  software_level ENUM('beginner', 'intermediate', 'advanced'),
  hardware_exposure ENUM('none', 'some', 'extensive'),
  robotics_experience ENUM('none', 'some', 'extensive'),
  language_preference ENUM('en', 'ur') DEFAULT 'en',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)

-- Platform Statistics
platform_stats (
  id SERIAL PRIMARY KEY,
  books_count INT DEFAULT 1,
  active_users INT DEFAULT 0,
  ai_interactions INT DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
)

-- Translation Cache
translation_cache (
  id VARCHAR PRIMARY KEY,
  chapter_id VARCHAR NOT NULL,
  content_hash VARCHAR NOT NULL,
  urdu_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP
)
```

---

## 8. Deployment Strategy

### Decision
Deploy frontend to Vercel, backend to Vercel Serverless Functions or Railway.

### Rationale
- Vercel optimized for React/Docusaurus
- Automatic CI/CD from GitHub
- Railway provides simpler Python deployment if Vercel cold starts are problematic

### Environment Variables
```bash
# Frontend (Vercel)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...

# Backend (Vercel/Railway)
GEMINI_API_KEY=...
QDRANT_API_KEY=...
QDRANT_URL=https://xxx.qdrant.io
DATABASE_URL=postgres://...
CLERK_SECRET_KEY=sk_...
```

---

## 9. Text Selection for Context

### Decision
Use browser Selection API with React hooks for "Ask about selected text" feature.

### Rationale
- Native browser API (no dependencies)
- Works across all modern browsers
- Can include surrounding context for better responses

### Implementation
```typescript
function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection()?.toString().trim();
      if (selection) setSelectedText(selection);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return { selectedText, clearSelection: () => setSelectedText('') };
}
```

---

## 10. Performance Optimization

### Decision
Implement lazy loading, code splitting, and caching to meet <3s load target.

### Strategies
| Strategy | Implementation |
|----------|----------------|
| Code Splitting | Dynamic import for ChatWidget, AuthModal |
| Image Optimization | Docusaurus built-in + WebP format |
| Font Loading | `font-display: swap` for web fonts |
| API Caching | SWR for user profile, stats |
| Animation | GPU-accelerated transforms only |

### Performance Targets
- LCP (Largest Contentful Paint): <2.5s
- FID (First Input Delay): <100ms
- CLS (Cumulative Layout Shift): <0.1
- Lighthouse Performance: >90

---

## Summary

All technical decisions finalized. Key updates from previous research:

1. **Auth changed from Better-Auth to Clerk** per Constitution v4.0.0
2. **Theme updated to Dark Blue (#1a1a2e) + Yellow (#ffd700)** per Constitution Principle I
3. **Skills architecture confirmed** per Constitution Principle II

Stack summary:
- **Frontend**: Docusaurus 3.x + React 18 + Framer Motion + CSS Variables
- **Backend**: FastAPI + Qdrant + Gemini API
- **Auth**: Clerk
- **Database**: Neon Postgres
- **Deployment**: Vercel (frontend + backend functions)

Ready to proceed to Phase 1: Data Model & Contracts.
