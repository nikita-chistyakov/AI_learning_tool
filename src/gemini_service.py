# src/gemini_service.py
import google.generativeai as genai
import json

_model = None # Private variable to hold the initialized model

def configure_gemini(api_key):
    """Configures the Gemini API with the given API key."""
    global _model
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.4, # For more factual responses in translation/Q&A
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    _model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                   generation_config=generation_config)

def get_word_info_from_ai(french_word: str) -> dict:
    """
    Uses Gemini to get English translation and an example sentence in JSON format.
    """
    if _model is None:
        raise Exception("Gemini model not configured. Call configure_gemini() first.")

    prompt = f"""
    Provide the English translation and a simple example sentence for the French word: '{french_word}'.
    Format the response as a JSON object with the following keys:
    "french_word" (the input word), "english_translation", and "example_sentence".
    """
    # Override generation_config for JSON specifically for this request if needed
    json_generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "french_word": {"type": "STRING"},
                "english_translation": {"type": "STRING"},
                "example_sentence": {"type": "STRING"}
            },
            "required": ["french_word", "english_translation", "example_sentence"]
        }
    }
    response = _model.generate_content(prompt, generation_config=json_generation_config)
    return json.loads(response.text)

def get_ai_response_for_qa(question: str) -> str:
    """
    Uses Gemini to answer a general language learning question.
    """
    if _model is None:
        raise Exception("Gemini model not configured. Call configure_gemini() first.")

    prompt = f"""
    You are an expert French language tutor. Answer the following question about French language learning concisely and helpfully.
    Question: {question}
    """
    # Use standard generation_config for general text response
    response = _model.generate_content(prompt)
    return response.text