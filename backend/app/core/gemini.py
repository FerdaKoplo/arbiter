from typing import List
from pydantic import BaseModel, ValidationError
from google import genai
import json

client = genai.Client()


class GeminiClaim(BaseModel):
    claim_text: str
    normalized_text: str
    confidence: float
    span_start: int
    span_end: int
    claim_type: str


class GeminiClaimsOutput(BaseModel):
    claims: List[GeminiClaim]


def extract_claims_from_text(prompt_text: str) -> GeminiClaimsOutput:
    prompt = f"""
    Extract claims from the text below.
    Return JSON exactly in this format:

    {{
        "claims": [
            {{
                "claim_text": "...",
                "normalized_text": "...",
                "confidence": 0.0-1.0,
                "span_start": integer,
                "span_end": integer,
                "claim_type": "FACT|OPINION|INFERENCE"
            }}
        ]
    }}

    Text:
    \"\"\"{prompt_text}\"\"\"
    """

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        # model="gemini-2.5-flash",
        # model="gemini-pro-latest",
        contents=prompt,
    )

    raw_text = response.text

    if not raw_text:
        raise ValueError("Gemini returned empty response")

    clean_text = raw_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()

    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError:
        print(f"FAILED JSON: {clean_text}")
        raise ValueError(f"Gemini output is not valid JSON")

    try:
        validated = GeminiClaimsOutput.parse_obj(data)
    except ValidationError as e:
        raise ValueError(f"Gemini output failed validation: {e}")

    return validated


def generate_consultant_report(
    winning_option_name: str,
    winning_score: float,
    engine_reasons: list[str],
    all_document_texts: list[str],
) -> str:
    full_document_context = "\n\n--- DOCUMENT SOURCE START ---\n\n".join(
        all_document_texts
    )

    context_prompt = f"""
    You are an expert Chief Technology Officer (CTO) and Solution Architect.
    Your job is to synthesize a strategic implementation plan based *strictly* on the provided documentation and decision engine results.
    
    ### INPUT DATA
    - **Winning Option:** "{winning_option_name}" (Score: {winning_score})
    - **Key Evidence:** {str(engine_reasons)[:10000]}... (truncated for focus)
    - **Source Documents:** {full_document_context[:20000]}... (truncated)
    
    ### ANTI-HALLUCINATION RULES:
    1. **Source Truth:** ONLY use info found in the Source Documents.
    2. **Silence Policy:** If the text is silent, say "Not specified."
    
    ### TEMPLATE INSTRUCTIONS:
    * **Diagram:** Generate valid `mermaid` syntax for a System Architecture.
    * **Code:** Generate valid `sql` or `python` code blocks where requested.
    * **Granularity:** Because you have full context, be extremely specific (e.g., quote specific budget numbers or user constraints).
    
    ### REQUIRED OUTPUT FORMAT:

    ## 1. Executive Summary
    [High-impact summary of the strategic value.]

    ## 2. Strategic Rationale & Evidence
    * **Why this won:** [Synthesize "SUPPORTS" evidence].
    * **Verbatim Support:** [Quote 2-3 specific sentences from the docs that prove this is the right choice].

    ## 3. System Architecture
    [Brief description of the data flow.]
    ```mermaid
    graph TD
    %% Create a detailed flow based on the specific constraints in the text
    [Generate Mermaid Chart]
    ```

    ## 4. Technical Specifications
    * **Stack:** [Language/Framework]
    * **Database:** [SQL/NoSQL]
    * **Infrastructure:** [Cloud/On-Prem details if in text]

    ## 5. Generated Artifacts (MVP Starter Pack)
    
    **A. Database Schema (Draft)**
    *Based on the data entities mentioned in the text (e.g., Users, Products, Orders).*
    ```sql
    -- Generate a CREATE TABLE SQL script based strictly on the fields mentioned in the docs
    -- Example: If docs mention "User must have a phone number", add phone_number column.
    ```

    **B. Core API Endpoints**
    *Based on the user actions described (e.g., "User uploads document").*
    | Method | Endpoint | Description |
    | :--- | :--- | :--- |
    | POST | /example | [Description from docs] |

    ## 6. Implementation Roadmap (Detailed)
    **Week 1: Foundation**
    * [Specific Task]
    
    **Week 2: Core Features**
    * [Specific Task]

    ## 7. Risk Assessment (Pre-Mortem)
    * **Risk:** [Weakness from logs] -> **Mitigation:** [Specific fix]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=context_prompt
    )

    if not response.text:
        return "## Error Generating Report\n\nThe AI model did not return any text. This is likely due to a safety filter trigger or an API issue."

    return response.text
