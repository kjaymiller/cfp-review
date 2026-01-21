# CFP-Review System Design Guide

## 1. System Overview
The **CFP-Review** system is a centralized portfolio for speakers to manage their talk proposals and receive feedback from a community of peers and mentors. Unlike conference-specific tools, this is a "sandbox" for refining ideas before they are submitted to real events.

The system is built with a strong focus on:
*   **Speaker Privacy**: Drafts are private until the speaker is ready for feedback.
*   **Mentorship**: A distinct "Reviewer" role allows experienced speakers to discover and critique proposals.
*   **Discovery**: Tagging system to help reviewers find topics they are qualified to critique.

## 2. User Flows

### Key Workflows
*   **Speaker (Author)**:
    1.  Creates a generic proposal (Title, Abstract).
    2.  Adds private notes (e.g., "Needs a better opening," "Target audience: Beginners").
    3.  Keeps it in **Draft** while working.
    4.  Changes status to **Review Requested** when ready for feedback.
    5.  Iterates on the content based on reviews.

*   **Reviewer (Mentor)**:
    1.  Browses the "Review Queue" (filtered by Tags).
    2.  Selects a proposal to review.
    3.  Reads the Abstract and Title.
    4.  Leaves constructive feedback and a sentiment score (Needs Work / Good / Excellent).

## 3. Database Schema (Normalized)

### Core Entities
*   **User**: Central authentication entity (Django User).
*   **Proposal**: The core content unit. Owned by one User. Can have multiple Tags.
*   **Review**: A feedback record linking a Reviewer to a Proposal.
*   **Tag**: A simple categorization label (e.g., "Python", "Soft Skills").

### Access Control Logic
*   **Reviewers**: Managed via a dedicated User Group. Permission: `can_review`.
*   **Authors**: Implicit role based on ownership of a Proposal record.

## 4. Visual & Interface Guidelines
*   **Dashboard-First Design**:
    *   **Speakers** see "My Proposals" (Drafts vs. In Review).
    *   **Reviewers** see "Needs Review" (a feed of open requests).
*   **Status Indicators**:
    *   "Draft" [Gray]: Private.
    *   "Review Requested" [Yellow]: Visible to reviewers.
    *   "Reviewed" [Green]: Has received feedback.
*   **Tagging UI**: Simple pill-based UI for adding/viewing tags.
