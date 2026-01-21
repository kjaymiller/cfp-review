# CFP-Review

A Django-based application for managing Call for Papers (CFP) processes. This system facilitates the entire lifecycle of a conference session selection, from proposal submission to reviewing and community discussion.

## Features

Based on the project's [MERISE Analysis](MERISE_PLAN.md), the system includes:

*   **CFP Management**: Organizers can create and manage specific Call for Papers events with start and end dates.
*   **Proposal Submission**: Speakers can submit "Talk" or "Workshop" proposals, including abstracts.
*   **Review System**: Reviewers can evaluate proposals using a simple scoring system (-1, 0, +1).
*   **Community Interaction**:
    *   **Comments**: Users can discuss proposals.
    *   **Starring**: Users can "star" valuable comments.
*   **Advanced Features**:
    *   **Similarity Search**: Leveraging `pgvector`, the system supports finding similar proposals and comments based on content embeddings.
    *   **Moderation**: A reporting system allowing users to flag abusive proposals or comments.

## Data Model

The core entities defined in the system are:

*   **User**: Standard Django user extended to support roles like Speaker, Reviewer, and Organizer.
*   **CFP**: The event definition.
*   **Proposal**: Submissions linked to a Speaker and a CFP.
*   **Review**: Linked to a Proposal and a Reviewer.
*   **Comment**: Textual feedback on proposals.
*   **Report**: Polymorphic model to flag inappropriate content.

## Tech Stack

*   **Language**: Python
*   **Framework**: Django
*   **Database**: PostgreSQL
*   **Extensions**: `pgvector` (for vector similarity search)
*   **Package Manager**: `uv`

## Getting Started

### Prerequisites

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv)
*   PostgreSQL (with `vector` extension support)

### Installation

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

2.  **Database Setup:**
    Ensure your PostgreSQL database is running. You will likely need to create the database and enable the vector extension:
    ```sql
    CREATE DATABASE cfp_db;
    \c cfp_db
    CREATE EXTENSION vector;
    ```
    *(Note: Adjust your `settings.py` or `.env` to point to this database)*

3.  **Apply Migrations:**
    ```bash
    uv run python manage.py migrate
    ```

4.  **Create a Superuser:**
    ```bash
    uv run python manage.py createsuperuser
    ```

5.  **Run the Development Server:**
    ```bash
    uv run python manage.py runserver
    ```

## Development

See [MERISE_PLAN.md](MERISE_PLAN.md) for detailed documentation on the data dictionary, conceptual model (MCD), and logical model (MLD).
