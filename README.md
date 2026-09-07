# Superjoin Fact Knowledge Layer

This project is a prototype for the Superjoin Engineering Intern Hiring Assignment. It builds a Fact Knowledge Layer that extracts facts from PDFs and reasons about their relationships (corroboration, contradictions) across multiple documents.

## Approach & Architecture

-   **Frontend:** Streamlit for a simple, interactive UI.
-   **PDF Parsing:** `pymupdf` to extract raw text from uploaded PDFs.
-   **AI Core:** Two-phase pipeline using Google Gemini API (`google-genai`).
    -   **Phase 1 (Extraction):** Gemini 2.5 Flash processes chunks of document text to extract structured facts using Pydantic schemas, guaranteeing entity, metric, value, context, and exact source quotes.
    -   **Phase 2 (Reasoning):** Gemini 2.5 Pro compares all extracted facts to identify relationships, explicitly looking for corroborations, genuine contradictions, and apparent contradictions reconciled by context.
-   **Storage:** Facts and relationships are stored in-memory during the session and rendered dynamically, avoiding the need for a complex graph database setup for this prototype.

## Setup and Run Instructions

1.  **Prerequisites:** Python 3.9+ installed.
2.  **Clone the repository.**
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
6.  **Usage:** Open the local URL provided by Streamlit. Enter your Gemini API Key (get a free one from Google AI Studio). Upload the starter dataset PDFs and click "Process Documents".

## Video Demo
[Insert Link to your 3-minute Loom/YouTube video here]

## Limitations and Next Steps

-   **Context Window Limits:** Currently, to process quickly, we take a large chunk of the document. For massive documents, we need a robust map-reduce approach or semantic chunking.
-   **Table Extraction:** PDF text extraction struggles with complex tables. Next step: Integrate a Vision Model or dedicated OCR pipeline for tabular data.
-   **Fact Granularity:** The LLM sometimes groups multiple sub-facts into one. Improving the prompt to enforce atomicity of facts would be a strong next step.
