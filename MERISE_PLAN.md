# MERISE Analysis for CFP-Review (Speaker Portfolio Edition)

## 1. Dictionary of Data
- **User**: Name, Email, Bio, Password, Roles (Speaker, Reviewer)
- **Proposal**: Title, Abstract, Notes (Private), Status (Draft, Review Requested, Archived), Tags, Timestamp
- **Review**: Score (-1, 0, +1), Feedback (Text), Timestamp
- **Tag**: Name (e.g., Python, DevOps, Leadership)

## 2. Conceptual Data Model (MCD)

### Entities
*   **USER**: Person interacting with the system.
    *   *Speaker Role*: Owns the proposals.
    *   *Reviewer Role*: Provides feedback/mentoring.
*   **PROPOSAL**: A talk idea or abstract created by a Speaker.
*   **REVIEW**: An evaluation/feedback record for a Proposal.
*   **TAG**: A category label for a Proposal.

### Relationships
*   **OWNS**: **USER** (0,n) ─── (1,1) **PROPOSAL**
*   **EVALUATES**: **USER** (0,n) ─── (1,1) **REVIEW**
*   **TARGETS**: **PROPOSAL** (0,n) ─── (1,1) **REVIEW**
*   **CATEGORIZES**: **PROPOSAL** (0,n) ─── (0,n) **TAG**

## 3. Logical Data Model (MLD) / Relational Schema

### Users
*Utilizing Standard Django User model*
- `id` (PK)
- `username`
- `email`
- `groups` (Used for "Reviewer" role designation)

### Tag
- `id` (PK)
- `name` (VarChar, Unique)

### Proposal
- `id` (PK)
- `author_id` (FK -> User)
- `title` (VarChar)
- `abstract` (Text) - *The public description*
- `private_notes` (Text) - *Notes for the speaker (outlines, etc)*
- `status` (Enum: Draft, Review Requested, Archived)
- `created_at` (DateTime)
- `updated_at` (DateTime)
*Many-to-Many relationship with Tag*

### Review
- `id` (PK)
- `proposal_id` (FK -> Proposal)
- `reviewer_id` (FK -> User)
- `score` (Integer: -1, 0, 1) - *Optional sentiment*
- `feedback` (Text) - *Detailed comments*
- `created_at` (DateTime)

## 4. Business Rules
- **Privacy**: `Draft` proposals are visible ONLY to the Author.
- **Discovery**: `Review Requested` proposals are visible to Authors and anyone in the `Reviewers` group.
- **Reviewing**: A user cannot review their own proposal.
- **Editability**: Reviews are generally final, but authors can update proposals based on feedback.
