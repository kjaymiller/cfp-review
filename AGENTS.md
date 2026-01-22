# Operational Modes

This document defines the operational modes for the agent working on this project.

## Documentation Compliance

The agent must adhere to the standards defined in the project documentation. Before planning or implementing changes, review the relevant documents:

*   **`SYSTEM_DESIGN.md`**: Consult for system architecture, data models, user flows, and backend technology standards (Python, Django, etc.).
*   **`FRONTEND_DESIGN.md`**: Consult for visual design, UI components, CSS rules, and frontend interactions (HTMX, Alpine.js).

## Current Mode: **BUILD**

## Mode Definitions

### 1. PLAN Mode
*   **Focus:** Architecture, Design, Documentation, Workflow verification.
*   **Allowed Actions:**
    *   Writing/Editing Documentation (`*.md`).
    *   Generating Diagrams (`*.svg`, `*.png`).
    *   Researching (Reading files, Searching).
    *   Asking clarifying questions.
*   **Prohibited Actions:**
    *   Writing Application Code (Python, HTML, JS, CSS).
    *   Running Migrations.
    *   Creating Django Apps.

### 2. BUILD Mode
*   **Focus:** Implementation, Refactoring, Testing.
*   **Allowed Actions:**
    *   All actions from PLAN mode.
    *   Generating/Editing Application Code.
    *   Executing Shell Commands for build/test (e.g., `uv`, `pytest`).
    *   Managing Git commits.

## Transition Protocol
The agent must strictly adhere to the **Current Mode**. Transitioning from **PLAN** to **BUILD** requires explicit user authorization.

**CRITICAL: The agent must NEVER switch modes autonomously. The agent must ALWAYS prompt the user and receive a specific command to switch modes.**
