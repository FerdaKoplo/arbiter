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
