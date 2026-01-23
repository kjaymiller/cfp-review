# CFP-Review Frontend Design Guide

## 1. Design Philosophy
**"The Green Room for the World Stage"**

The design aesthetic aims to balance the nervousness of public speaking with the warmth of a supportive community. It is **light-hearted and friendly** (to reduce anxiety) but **professional** (treating speakers as talent). The "International" aspect is represented through a diverse color palette and universal iconography, acknowledging that talent comes from everywhere.

### Core Attributes
*   **Warm & Welcoming**: High-contrast but soft edges. No intimidating "enterprise gray" walls.
*   **The Grand Stage**: Subtle visual cues of theaters, spotlights, and microphones without being kitschy.
*   **International**: avoiding region-specific design tropes; using a vibrant, multi-cultural color spectrum.
*   **Professional**: Clean typography and clear hierarchy. This is a tool for career growth.

---

## 2. Color Palette

### Primary: "The Spotlight"
Used for primary actions (Submit, Request Review) and key highlights.
*   **Spotlight Gold**: `#F6E05E` (Optimism, Attention) - *Use sparingly for high impact.*
*   **Royal Blue**: `#3182CE` (Trust, Professionalism, The "World" Stage) - *Primary brand color.*

### Secondary: "Global Voices"
A supporting palette representing diversity. Used for tags, avatars, and accents.
*   **Teal**: `#319795` (Clarity, Communication)
*   **Stage Orange**: `#DD6B20` (Energy, Warmth, Theater Carpets)
*   **Indigo**: `#4C51BF` (Depth - *Blue-leaning, not Purple*)

### Neutrals: "The Script"
*   **Ink Black**: `#1A202C` (Text)
*   **Paper White**: `#FFFFFF` (Card Backgrounds)
*   **Backstage Grey**: `#F7FAFC` (App Background - light and airy)

---

## 3. Typography

### Headings: *Rubik* or *Poppins*
Rounded sans-serifs that feel friendly and approachable but hold weight well.
*   **H1 (The Marquee)**: Bold, tight letter spacing.
*   **H2 (Section Headers)**: Medium weight, clear hierarchy.

### Body: *Inter* or *Lato*
Highly legible, professional sans-serif for reading feedback and drafting proposals.

---

## 4. Iconography & Visual Language

### The "Grand Stage" Motifs
*   **Spotlights**: Use solid, low-opacity geometric shapes or bold blocks of color to highlight key areas. **No Gradients**—stick to flat, distinct colors.
*   **Microphones**: Used for "New Proposal" or "Speaker Profile" icons.
*   **Curtains**: Very subtle vertical textures in footers or sidebars (opacity < 5%).

### Friendly & International
*   **Avatars**: Circular, perhaps with colorful rings (using the secondary palette) to show status.
*   **Empty States**: Illustrations of empty stages waiting for a speaker, or a nervous stick figure being encouraged by others.
*   **Feedback**: Use specific icons for "Cheer" (👏), "Think" (🤔), and "Love" (❤️) rather than generic stars.

---

## 5. UI Components

### Cards (Proposals)
*   Styled like **Event Tickets** or **Program Entries**.
*   **Left edge**: Color-coded status strip (Draft=Grey, Review Requested=Royal Blue, Archived=Backstage Grey).
*   **Shadows**: "Lifted" shadow (`box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1)`) to make them feel like physical objects on a desk.

### Buttons
*   **Primary**: Solid "Royal Blue" with a slight "glow" on hover. Rounded corners (match cards).
*   **Secondary**: Outline with "Spotlight Gold" or "Teal".

### Navigation
*   Top bar: Clean, white background.
*   Logo: Text-based with a small icon (e.g., a speech bubble turning into a spotlight).

---

## 6. CSS Framework Strategy
**❌ NO TAILWIND CSS**. This project uses standard, modern CSS.

### Technical Approach
*   **CSS Variables**: Define the color palette and spacing in `:root` for global consistency and easy theming.
*   **Layout**: Use `CSS Grid` and `Flexbox` for structural layout.
*   **Responsiveness**: **Mobile-First Design**. All views must be fully functional on mobile devices before scaling up to desktop. Use standard media queries.
*   **Modern Styling**:
    *   Use `rem` units for typography and spacing.
    *   Use `border-radius` and `box-shadow` for the "card" aesthetic.

### Interactions & Motion
*   **JavaScript Libraries**: **HTMX** and **Alpine.js** are encouraged to create a responsive, SPA-like feel without the overhead of a heavy frontend framework.
    *   Use *HTMX* for server interactions (swapping content, partial updates).
    *   Use *Alpine.js* for local UI state (modals, dropdowns, toggles).
*   **Transitions**: Smooth, subtle transitions for all interactive states (hover, focus, active).
    *   *Standard timing*: `transition: all 0.2s ease-in-out`.
    *   Buttons should "lift" or "glow" on hover.
    *   Inputs should have a clear, colored border transition on focus.
*   **Touch Targets**: Ensure all buttons and links are at least 44px x 44px on mobile.
