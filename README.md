# Arbiter — AI-Driven Strategic Analysis Engine

Arbiter is a decision-support platform that transforms unstructured evidence (PDFs, project briefs, PRDs) into ranked, actionable strategic directives. It bridges the gap between massive data collection and confident executive decision-making.

---

## Quick Start

Follow these steps to run the application locally.

### 1. Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Google Gemini API Key (Get one at aistudio.google.com)

### 2. Clone the Repository

```bash
git clone https://github.com/FerdaKoplo/arbiter.git
cd arbiter
```

### 3. Backend Setup (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the API
python main.py
```

The backend API will run on `http://localhost:8000`.

### 4. Frontend Setup (React)

Open a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

---

## Project Overview

### Inspiration

In an era of information overload, decision-makers are buried under "data noise." Arbiter is designed to be more than a summarizer — it weights evidence, ranks possibilities, and acts as a digital arbiter that converts raw evidence into strategic action.

### What it does

Arbiter ingests project documentation and executes a multi-stage analysis:

1. **Claim Extraction** — Identifies core requirements and constraints.
2. **Option Ranking** — Scores potential strategies based on evidence density.
3. **Consultant Report** — Produces a Strategic Directive that includes architecture diagrams (Mermaid.js), SQL schemas, and implementation roadmaps.

### How we built it

- **Frontend:** React, TypeScript, Tailwind CSS, TanStack Query
- **Backend:** Python (FastAPI)
- **AI Engine:** Google Gemini 1.5 Flash
- **Visuals:** Mermaid.js for real-time architectural visualization

---

## Key Features

- **Verbatim Evidence System:** Every recommendation is linked back to specific quotes in source documents.
- **Anti-Hallucination Logic:** Enforces a strict "Source Truth" policy. If a technical detail is not present in the source, the system either marks it as unspecified or produces an "Informed Recommendation" instead of guessing.
- **Automated Artifacts:** Generates valid SQL schemas and API tables from business logic found in uploaded PRDs.
- **Dynamic Visualizations:** Automatically renders Mermaid code blocks into interactive system diagrams.

---

## Architecture (High-level)

Design priorities:

- Fast iteration
- Explicit state and structure
- Diagrammability
- Clear orchestration for the AI engine

---

## Anti-Hallucination & Prompting Strategy

A core challenge is preventing the AI from inventing undocumented facts. Arbiter addresses this with a layered prompt-engineering approach:

- Distinguish clearly between **Documented Facts** (explicit quotes) and **Strategic Recommendations** (inferred or advised).
- Flag missing technical details as "unspecified" in outputs; when necessary, provide **Informed Recommendations** with the rationales and confidence level attached.
- Store evidence links that trace each assertion back to its source text.

This policy is enforced across the pipeline and surfaced in generated reports.

---

## Example Output Types

- **Strategic Directive:** Executive summary, ranked options, recommended next steps.
- **Mermaid Diagrams:** Auto-generated architecture diagrams embedded in reports.
- **SQL Schemas:** Concrete table definitions derived from discovered business entities.
- **Traceable Evidence Map:** List of source quotes that support each claim or recommendation.

---

## Challenges & Learning

- **The "Silence Policy":** Ensuring the system does not guess when the PRD is silent on important technical choices. The system must either elicit the missing info or mark the field as unspecified and provide rationale for any recommended defaults.
- **Evidence Linking:** Balancing granularity of evidence (quote-level) with readability of reports.

---

## Running Notes

- Provide PRDs and supporting documents as PDFs or plain text for the best results.
- Expect outputs to contain two clearly labeled sections: **Documented Facts** and **Recommendations**. Each recommendation must cite supporting evidence or explicitly note the lack thereof.

---

## Contributing

Contributions are welcome. For major changes, open an issue describing the motivation and design, and follow the repository's contribution guidelines.

---
