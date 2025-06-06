# AI_learning_tool

## Try me here:
https://languageai.streamlit.app/

## File structure
`````` 
AI French Learning Assistant/
├── .streamlit/
│   └── secrets.toml  # For local development secrets
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies for Streamlit Cloud
├── src/              # Source code for core logic
│   ├── __init__.py   # Makes 'src' a Python package
│   ├── gemini_service.py
│   ├── database_manager.py
│   ├── quiz_logic.py
│   └── utils.py      # For general utility functions (e.g., prompt templates)
└── README.md         # Good practice for project overview ``````