from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class CrossReference(BaseModel):
    fact_1_id: str
    fact_2_id: str
    relationship_type: str = Field(description="Must be one of: 'Corroboration', 'Contradiction', 'Reconciled Contradiction'")
    explanation: str = Field(description="Explanation of why they corroborate, contradict, or how context reconciles them.")

class AnalysisResult(BaseModel):
    relationships: list[CrossReference]

def analyze_facts(all_facts: list[dict], api_key: str) -> list[dict]:
    """Uses Gemini to find relationships between extracted facts."""
    client = genai.Client(api_key=api_key)
    
    # Format facts for the prompt
    facts_str = ""
    for idx, f in enumerate(all_facts):
        # Ensure ID is unique across docs for the prompt
        f['id'] = f"fact_{idx}" 
        facts_str += f"ID: {f['id']}\n"
        facts_str += f"Document: {f['document']}\n"
        facts_str += f"Entity: {f['entity']}\n"
        facts_str += f"Metric: {f['metric']}\n"
        facts_str += f"Value: {f['value']}\n"
        facts_str += f"Context: {f['context']}\n"
        facts_str += f"Source Quote: {f['source_quote']}\n"
        facts_str += "-"*20 + "\n"

    prompt = f"""
    You are an expert fact-checker and analyst.
    Review the following list of facts extracted from multiple documents.
    
    Your task is to find interesting relationships BETWEEN facts from DIFFERENT documents.
    Specifically, look for at least one example of each of these three cases (if present):
    1. 'Corroboration': Two facts from different documents that state the same thing or support each other, even if expressed differently.
    2. 'Contradiction': Two facts that genuinely conflict with each other.
    3. 'Reconciled Contradiction': Two facts that seem to contradict, but can be explained by their 'Context' (e.g., different time periods, different units, standalone vs consolidated).
    
    Only output meaningful relationships. Do not link completely unrelated facts.
    
    Facts:
    ---
    {facts_str}
    ---
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash', # Updated to 3.6 per API suggestion
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnalysisResult,
            temperature=0.1
        )
    )
    
    analysis_data = response.parsed
    if not analysis_data:
         import json
         analysis_data = AnalysisResult(**json.loads(response.text))
    return [r.model_dump() for r in analysis_data.relationships]
