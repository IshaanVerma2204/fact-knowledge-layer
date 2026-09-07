import fitz
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class Fact(BaseModel):
    id: str = Field(description="A unique identifier for this fact (e.g., f1, f2)")
    category: str = Field(description="Dynamically assign a category for this fact (e.g., 'Financial', 'Operational', 'Macroeconomic', 'Leadership')")
    entity: str = Field(description="The subject of the fact, e.g., 'Delhivery', 'India', 'Reserve Bank'")
    metric: str = Field(description="The specific metric or attribute, e.g., 'Revenue from operations', 'Real GDP Growth'")
    value: str = Field(description="The value of the metric, e.g., 'Rs 7,225 Cr', '8.2%'")
    context: str = Field(description="Crucial context like time period, units, or scope, e.g., 'FY23-24', 'Base year 2011-12'")
    source_quote: str = Field(description="The exact snippet of text from the document proving this fact")

class ExtractedFacts(BaseModel):
    facts: list[Fact]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF bytes."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    # We grab the text. In a real system we'd chunk this intelligently.
    for page in doc:
        text += page.get_text() + "\n"
    return text

def extract_facts(text: str, document_name: str, api_key: str) -> list[dict]:
    """Uses Gemini to extract structured facts from text."""
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert financial and macroeconomic analyst. 
    Read the following text extracted from a document named '{document_name}'.
    
    Extract the 15 most important numerical and semantic facts from this text. 
    Focus on key metrics like revenue, growth rates, major events, or key figures.
    Make sure to provide a unique 'id' for each fact (e.g., '{document_name}_fact_1').
    Dynamically assign a logical 'category' to each fact to create an evolving schema.
    Ensure the 'source_quote' exactly matches the text provided.
    
    Document Text:
    ---
    {text[:80000]} # Limit characters to avoid timeouts for massive docs
    ---
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExtractedFacts,
            temperature=0.1
        )
    )
    
    facts_data = response.parsed
    if not facts_data: # Fallback
         import json
         facts_data = ExtractedFacts(**json.loads(response.text))
         
    result = []
    for fact in facts_data.facts:
        f_dict = fact.model_dump()
        f_dict['document'] = document_name
        result.append(f_dict)
    return result
