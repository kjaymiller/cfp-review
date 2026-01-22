# MERISE Analysis for CFP-Review (Speaker Portfolio Edition)

## Project Rationale
Unlike standard conference management tools, this system acts as a **Speaker Portfolio**. It is a centralized hub for speakers to refine proposals (Drafts), request feedback from Mentors (Reviewers), and be discovered by Organizers.

## 1. Dictionary of Data
- **User**: Name, Email, Bio, Password, Roles (Speaker, Reviewer, Organizer)
- **Proposal**: Title, Abstract, Notes (Private), Status (Draft, Review Requested, Archived), Tags, Timestamp
- **Review**: Score (-1, 0, +1), Feedback (Text), Timestamp
- **Tag**: Name (e.g., Python, DevOps, Leadership)
- **Selection**: Timestamp, Note (e.g., "Potential Keynote")

## 2. Conceptual Data Model (MCD)

### Entities
*   **USER**: Person interacting with the system.
    *   *Speaker Role*: Owns the proposals.
    *   *Reviewer Role*: Provides feedback/mentoring.
    *   *Organizer Role*: Scouts and shortlists talks.
*   **PROPOSAL**: A talk idea or abstract created by a Speaker.
*   **REVIEW**: An evaluation/feedback record for a Proposal.
*   **TAG**: A category label for a Proposal.
*   **SELECTION**: A private bookmark/shortlist of a proposal by an organizer.

### Relationships
*   **OWNS**: **USER** (0,n) ─── (1,1) **PROPOSAL**
*   **EVALUATES**: **USER** (0,n) ─── (1,1) **REVIEW**
*   **TARGETS**: **PROPOSAL** (0,n) ─── (1,1) **REVIEW**
*   **CATEGORIZES**: **PROPOSAL** (0,n) ─── (0,n) **TAG**
*   **SELECTS**: **USER** (Organizer) (0,n) ─── (0,n) **PROPOSAL**

## 3. Logical Data Model (MLD) / Relational Schema

### Users
*Utilizing Standard Django User model*
- `id` (PK)
- `username`
- `email`
- `groups` ("Reviewer", "Organizer")

### Tag
- `id` (PK)
- `name` (VarChar, Unique)

### Proposal
- `id` (PK)
- `author_id` (FK -> User)
- `title` (VarChar)
- `abstract` (Text) - *The public description*
- `private_notes` (Text) - *Notes for the speaker (outlines, etc)*
- `status` (Enum: Draft, Review Requested, Archived) - *Indexed for performance*
- `created_at` (DateTime)
- `updated_at` (DateTime)
*Many-to-Many relationship with Tag*

### Review
- `id` (PK)
- `proposal_id` (FK -> Proposal)
- `reviewer_id` (FK -> User)
- `score` (Integer: -1, 0, 1)
- `feedback` (Text)
- `created_at` (DateTime)

### Selection
*Represents an Organizer shortlisting a talk*
- `id` (PK)
- `organizer_id` (FK -> User)
- `proposal_id` (FK -> Proposal)
- `created_at` (DateTime)

## 4. Business Rules
- **Privacy**: `Draft` proposals are visible ONLY to the Author.
- **Discovery**: `Review Requested` proposals are visible to Authors, Reviewers, and Organizers.
- **Reviewing**: A user cannot review their own proposal.
- **Organizers**: Can see `Review Requested` proposals and existing reviews. Can "Select" (bookmark) proposals. Can also submit Reviews (same as Reviewers).

## 5. Physical Data Model & Optimization

### Indexing Strategy
To ensure performant queries for the primary user flows (Reviewers and Organizers filtering proposals), the following indexes should be applied:

*   **`Proposal.status`**: A standard B-Tree index is required. This field is the primary filter for Reviewers (finding "Review Requested" talks) and Organizers (scouting).
*   **`Proposal.author_id`**: Foreign key index for retrieving a user's portfolio.
*   **`Review.proposal_id`**: Foreign key index for aggregating reviews on a proposal.
*   **`Selection.organizer_id`**: Foreign key index for retrieving an organizer's shortlist.

