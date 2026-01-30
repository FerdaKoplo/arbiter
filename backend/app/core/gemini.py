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
        # model="gemini-3-pro-preview",
        model="gemini-2.5-flash",
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
    """
    Generates a grounded, high-level IT Consultant Report using the full context window.
    """

    # 1. Prepare Full Context (No truncation)
    # We join all documents so the consultant sees the full picture
    full_document_context = "\n\n--- DOCUMENT SOURCE START ---\n\n".join(
        all_document_texts
    )

    # 2. Strict System Prompt
    context_prompt = f"""
    You are an expert Chief Technology Officer (CTO) and Solution Architect.
    Your job is to synthesize a strategic implementation plan based *strictly* on the provided documentation and decision engine results.
    
    ### INPUT DATA
    
    **DECISION CONTEXT:**
    - **Winning Option:** "{winning_option_name}"
    - **Calculated Score:** {winning_score}
    
    **ENGINE REASONING LOGS (Evidence):**
    {str(engine_reasons)}
    
    **SOURCE DOCUMENTATION (The "Truth"):**
    {full_document_context}
    
    ### INSTRUCTIONS
    Generate a **Strategic Implementation Directive** in Markdown.
    
    **Guidance on Tone & Accuracy:**
    1.  **No Hallucinations:** Do not invent features, constraints, or budget numbers not found in the source text. If the text is silent, state "Not specified in documentation."
    2.  **Citation Style:** When making a claim (e.g., "We must avoid accounting features"), reference the specific text or rule number from the Source Documentation.
    3.  **Tone:** Direct, authoritative, and low-ego. Write for a CEO/Founder.
    
    Explain *why* this option won.
    - Explicitly reference the "SUPPORTS" logs from the Engine Logic.
    - Explicitly reference the "BLOCKS" logs that disqualified other approaches (if evident).
    - Quote specific constraints from the Source Documentation (e.g., "Per Section 1.5, the product is NOT...").

    Propose a stack that fits the *constraints* found in the text.
    - **Core Stack:** [Language/Framework] - justify why based on the text.
    - **Database:** [SQL/NoSQL] - justify based on data structure needs.
    - **Key Constraints:** List what we must NOT build (e.g., "No chat features").

    A tight, weekly breakdown to hit the "MVP" definition found in the text.
    - **Week 1:** [Foundation]
    - **Week 2:** [Core Features]
    - **Week 3:** [Integration/Refinement]
    - **Week 4:** [Launch/Deployment]

    Analyze the "WEAKENS" or negative factors from the Engine Logic.
    - **Risk:** [What is the risk?]
    - **Mitigation:** [How do we fix it using the recommended stack?]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=context_prompt
    )

    if not response.text:
        return "## Error Generating Report\n\nThe AI model did not return any text. This is likely due to a safety filter trigger or an API issue."

    return response.text
