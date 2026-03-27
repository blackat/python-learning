---
title: Python Learning Journal
description: A structured, test-driven approach to learning Python.
template: splash
hero:
  tagline: Theory notes, runnable examples, and exercises that go from 🔴 to 🟢.
  actions:
    - text: Start with OOP
      link: /ch01_oop/foundation/
      icon: right-arrow
      variant: primary
---

## How it works

Each chapter follows the same flow:

```
read notes → run examples → fill in exercises → run tests
```

| What | Where | Purpose |
|------|-------|---------|
| 📖 Theory notes | `docs-site/src/content/docs/` | Concepts in my own words |
| 🐍 Examples | `src/exercises/chXX/examples.py` | Runnable snippets |
| ✏️ Exercises | `src/exercises/chXX/` | Stubs to fill in |
| ✅ Tests | `src/exercises/chXX/tests/` | Prove the solution works |

## Chapters

- [OOP — Foundation](/python-learning/ch01_oop/foundation/)
- [OOP — Properties](/python-learning/ch01_oop/properties/)
- [OOP — Advanced](/python-learning/ch01_oop/advanced/)
