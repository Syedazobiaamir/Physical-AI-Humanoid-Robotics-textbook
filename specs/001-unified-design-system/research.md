# Research: Unified UI/UX + Chatbot Design System

**Feature**: 001-unified-design-system
**Date**: 2025-12-13
**Status**: Complete

## Overview

This document captures research findings for technology choices, integration patterns, and best practices for the Unified Design System feature.

---

## 1. Frontend Framework: Docusaurus 3.x

### Decision
Use Docusaurus 3.x with React 18 for the frontend, leveraging its built-in MDX support and documentation-focused features.

### Rationale
- Native MDX support for interactive course content
- Built-in search, navigation, and versioning
- React 18 compatibility enables modern hooks and concurrent features
- Strong community and Vercel deployment support
- Theming system supports custom design tokens

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Next.js | More complex setup for documentation-style content; Docusaurus optimized for this use case |
| Gatsby | Slower build times; less active maintenance |
| Astro | Less mature MDX ecosystem; fewer documentation-specific features |

### Integration Notes
- Custom React components in `src/components/` integrate seamlessly with MDX
- CSS variables for design tokens in `src/css/custom.css`
- Swizzle navbar/footer for custom implementations

---

## 2. Animation Library: Framer Motion

### Decision
Use Framer Motion for all UI animations (hover effects, page transitions, timeline animations).

### Rationale
- Declarative API integrates well with React components
- Hardware-accelerated animations for smooth 60fps performance
- Built-in gesture support for hover, tap, drag
- Layout animations for card hover lift effects
- SSR-compatible for Docusaurus static generation

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| CSS Animations | Limited for complex sequences; harder to coordinate |
| React Spring | Steeper learning curve; less intuitive API |
| GSAP | Larger bundle size; licensing considerations |

### Implementation Pattern
```tsx
// Example: Knowledge Card hover animation
<motion.div
  whileHover={{ y: -8, boxShadow: "0 8px 30px rgba(0, 229, 255, 0.3)" }}
  transition={{ type: "spring", stiffness: 300 }}
>
  <KnowledgeCard />
</motion.div>
```

---

## 3. Styling Approach: CSS Variables + Tailwind

### Decision
Use CSS custom properties (variables) for design tokens with Tailwind CSS for utility classes.

### Rationale
- CSS variables enable runtime theme switching
- Tailwind provides consistent spacing, typography utilities
- Smaller bundle than full component libraries
- Easy to enforce design system consistency

### Design Tokens Structure
```css
:root {
  /* Colors */
  --color-deep-space-blue: #0B1020;
  --color-neural-indigo: #1E2A78;
  --color-electric-cyan: #00E5FF;
  --color-soft-ai-violet: #7C7CFF;
  --color-text-primary: #EAEAF0;
  --color-text-muted: #9AA4BF;
  --color-card-bg: #121830;
  --color-divider: #1F2A44;

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
}
```

---

## 4. RAG Backend: FastAPI + Qdrant + Gemini

### Decision
Use FastAPI for API endpoints, Qdrant for vector storage/search, and Google Gemini for response generation.

### Rationale
- **FastAPI**: Async-native, automatic OpenAPI docs, Python ecosystem
- **Qdrant**: Purpose-built for vector search, free cloud tier, REST API
- **Gemini**: Strong reasoning for educational content, competitive pricing

### Alternatives Considered
| Component | Alternative | Reason Not Chosen |
|-----------|-------------|-------------------|
| Backend | Express.js | Python preferred for AI/ML integrations |
| Vectors | Pinecone | Higher cost; Qdrant free tier sufficient |
| LLM | OpenAI GPT-4 | Gemini specified in requirements; cost-effective |

### RAG Pipeline Architecture
```
User Query → Embedding (text-embedding-004) → Qdrant Search →
Context Retrieval → Gemini Prompt → Response Generation
```

### Embedding Strategy
- Chunk course content by section (~500 tokens)
- Store chapter metadata with vectors
- Use cosine similarity for retrieval (top-k=5)

---

## 5. Authentication: Better-Auth

### Decision
Use Better-Auth for authentication with session-based tokens stored in Neon Postgres.

### Rationale
- Simple integration with Next.js/React
- Built-in session management
- Supports email/password auth
- Easy to extend for profile collection

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Auth0 | Higher cost for scale; overkill for MVP |
| Clerk | Additional dependency; Better-Auth specified in requirements |
| NextAuth.js | Better-Auth provides similar features with simpler setup |

### Profile Collection Flow
1. Initial signup (email, password)
2. Post-signup redirect to profile setup
3. Collect: software background, hardware background, skill level, language preference
4. Store in Neon Postgres `user_profiles` table

---

## 6. Database: Neon Serverless Postgres

### Decision
Use Neon Serverless Postgres for user profiles, preferences, and chat session metadata.

### Rationale
- Serverless scales to zero (cost-effective)
- PostgreSQL compatibility (standard SQL)
- Built-in connection pooling
- Free tier sufficient for ~100 concurrent users

### Schema Overview
```sql
-- Users table (Better-Auth managed)
users (id, email, password_hash, created_at, updated_at)

-- Profile extension
user_profiles (
  user_id FK,
  software_background TEXT,
  hardware_background TEXT,
  skill_level ENUM('beginner', 'intermediate', 'advanced'),
  language_preference ENUM('en', 'ur'),
  created_at, updated_at
)

-- Chat sessions
chat_sessions (
  id, user_id FK, chapter_id,
  created_at, updated_at
)

-- Chat messages
chat_messages (
  id, session_id FK,
  role ENUM('user', 'assistant'),
  content TEXT,
  selected_context TEXT NULL,
  created_at
)
```

---

## 7. Deployment: Vercel + Alternative Backend

### Decision
Deploy frontend to Vercel; backend to Render or Railway as serverless functions.

### Rationale
- **Vercel**: Optimized for React/Next.js/Docusaurus, automatic CI/CD
- **Render/Railway**: Python-native, simpler FastAPI deployment than Vercel serverless

### Alternatives Considered
| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Vercel Serverless (Python) | Cold start issues; limited Python support |
| AWS Lambda | More complex setup; overkill for MVP |
| Fly.io | Good option; Render preferred for simplicity |

### Environment Variables
```
# Frontend (Vercel)
NEXT_PUBLIC_API_URL=https://api.example.com

# Backend (Render/Railway)
GEMINI_API_KEY=...
QDRANT_API_KEY=...
QDRANT_URL=https://xxx.qdrant.io
NEON_POSTGRES_URL=postgres://...
BETTER_AUTH_SECRET=...
```

---

## 8. AI Agents Architecture

### Decision
Implement agents as Python classes with a common base interface, each with specific skills.

### Rationale
- Single responsibility per agent
- Skills are composable functions
- Easy to test and extend
- Consistent prompt engineering patterns

### Agent-Skill Mapping
| Agent | Primary Skills | Use Case |
|-------|---------------|----------|
| PhysicalAIInstructor | real_world_robot_example | General teaching |
| EmbodiedIntelligenceAgent | hardware_mapping | Sensors/actuators content |
| BeginnerSimplifierAgent | simplify_for_beginner | Beginner personalization |
| HardwareContextAgent | hardware_mapping | Hardware background users |
| UrduTranslationAgent | urdu_translate | Translation |

### Skill Interface
```python
class Skill:
    async def execute(self, content: str, context: dict) -> str:
        """Transform content based on skill logic."""
        pass
```

---

## 9. Text Selection & Context Capture

### Decision
Use browser Selection API with React hooks to capture selected text and trigger chatbot context.

### Rationale
- Native browser API (no dependencies)
- Works across all modern browsers
- Can capture surrounding context (paragraph, section)

### Implementation Pattern
```typescript
function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim()) {
        setSelectedText(selection.toString());
      }
    };
    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, []);

  return { selectedText, clearSelection: () => setSelectedText('') };
}
```

---

## 10. Performance Optimization

### Decision
Implement lazy loading, code splitting, and caching strategies to meet <3s load target.

### Strategies
| Strategy | Implementation |
|----------|----------------|
| Code Splitting | Dynamic imports for chatbot modal, auth modal |
| Image Optimization | Docusaurus built-in image optimization |
| Font Loading | `font-display: swap` for web fonts |
| API Caching | SWR/React Query for chat history, user profile |
| Animation | GPU-accelerated transforms only |

### Lighthouse Targets
- Performance: >90
- Accessibility: >95
- Best Practices: >90
- SEO: >90

---

## Summary

All technical decisions have been made with clear rationale. No NEEDS CLARIFICATION items remain. The stack is:

- **Frontend**: Docusaurus 3.x + React 18 + Framer Motion + Tailwind CSS
- **Backend**: FastAPI + Qdrant + Gemini API
- **Auth**: Better-Auth + Neon Postgres
- **Deployment**: Vercel (frontend) + Render/Railway (backend)
- **AI**: 5 agents + 6 reusable skills in Python

Ready to proceed to Phase 1: Design & Contracts.
