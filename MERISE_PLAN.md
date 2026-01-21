# MERISE Analysis for CFP-Reviews

## 1. Dictionary of Data
- **User**: Name, Email, Bio, Password
- **CFP**: Title, Description, Dates, Active Status
- **Proposal**: Title, Abstract, Type, Status, Timestamp
- **Review**: Score (-1, 0, +1), Timestamp
- **Comment**: Text, Timestamp, Embedding
- **Proposal**: ..., Embedding
- **Report**: Reason, Timestamp
- **Star**: Timestamp

## 2. Conceptual Data Model (MCD)

### Entities
*   **USER**: Person interacting with the system.
    *   *Speaker Role*: Submits proposals.
    *   *Reviewer Role*: Evaluates proposals.
    *   *Organizer Role*: Manages CFPs and final decisions.
*   **CFP**: The event or call for papers instance.
*   **PROPOSAL**: A talk or session submitted by a Speaker for a specific CFP.
*   **REVIEW**: An evaluation of a Proposal by a Reviewer.
*   **COMMENT**: A message posted on a Proposal (e.g., for discussion among reviewers).
*   **REPORT**: A flag raised by a user regarding abusive content (Proposals or Comments).

### Relationships
*   **SUBMITS**: **USER** (0,n) ─── (1,1) **PROPOSAL**
*   **MANAGES**: **USER** (0,n) ─── (0,n) **CFP**
*   **HOSTS**: **CFP** (0,n) ─── (1,1) **PROPOSAL**
*   **WRITES**: **USER** (0,n) ─── (1,1) **REVIEW**
*   **TARGETS**: **PROPOSAL** (0,n) ─── (1,1) **REVIEW**
*   **POSTS**: **USER** (0,n) ─── (1,1) **COMMENT**
*   **DISCUSSES**: **PROPOSAL** (0,n) ─── (1,1) **COMMENT**
*   **FILES**: **USER** (0,n) ─── (1,1) **REPORT**
*   **FLAGS**: **REPORT** (1,1) ─── (0,n) **PROPOSAL** or **COMMENT** (Polymorphic)
*   **STARS**: **USER** (0,n) ─── (0,n) **COMMENT**

## 3. Logical Data Model (MLD) / Relational Schema

### Users
*Utilizing Standard Django User model + potential Profile extension*
- `id` (PK)
- `username`
- `email`
- `groups` (Used for "Reviewer" and "Organizer" role designations)

### CFP
- `id` (PK)
- `title` (VarChar)
- `description` (Text)
- `start_date` (Date)
- `end_date` (Date)

### Proposal
- `id` (PK)
- `cfp_id` (FK -> CFP)
- `speaker_id` (FK -> User)
- `title` (VarChar)
- `abstract` (Text)
- `abstract_vector` (Vector - for similarity search)
- `proposal_type` (Enum: Talk, Workshop)
- `status` (Enum: Draft, Submitted, Accepted, Rejected)
- `created_at` (DateTime)

### Review
- `id` (PK)
- `proposal_id` (FK -> Proposal)
- `reviewer_id` (FK -> User)
- `score` (Integer: -1, 0, 1)
- `created_at` (DateTime)

### Comment
- `id` (PK)
- `proposal_id` (FK -> Proposal)
- `author_id` (FK -> User)
- `text` (Text)
- `text_vector` (Vector - for similarity search)
- `created_at` (DateTime)

### Report
- `id` (PK)
- `reporter_id` (FK -> User)
- `content_type` (FK -> Django ContentType)
- `object_id` (Integer)
- `reason` (Text)
- `created_at` (DateTime)

### CommentStar
- `id` (PK)
- `user_id` (FK -> User)
- `comment_id` (FK -> Comment)
- `created_at` (DateTime)

## 4. Implementation Notes
- **User Roles**: 
    - **Speakers** are implicitly defined by having created a Proposal.
    - **Reviewers** should be an explicit Group or permission flag to allow access to the review dashboard.
    - **Organizers** should be an explicit Group allowing creation/editing of CFPs and viewing all reviews.
    - **Multiple Roles**: A user can hold multiple roles simultaneously (e.g., a Speaker at one event can be an Organizer for another).
    - **Stars**: Any authenticated user (Speaker or Reviewer) can star any comment, including their own.
- **Extensions**:
    - **pgvector**: Enable PostgreSQL `pgvector` extension to store embeddings for `Proposal.abstract` and `Comment.text` to support "Similar Talks" and related discussions features.
- **Constraints**: 
    - A reviewer cannot review their own proposal.
    - Unique constraint on (proposal_id, reviewer_id) to prevent duplicate reviews.
