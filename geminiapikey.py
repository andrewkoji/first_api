import os

print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")

# # Access the Google Gemini API key from environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     print("Environment variables:", os.environ)  # Debugging: Print all environment variables
#     raise ValueError("Google Gemini API key not found. Please set the 'GEMINI_API_KEY' environment variable.")

# # Example usage
# print(f"Your Google Gemini API key is: {GEMINI_API_KEY}")
