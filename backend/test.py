import os
from litellm import completion

os.environ["LITELLM_API_KEY"] = "your_actual_gemini_api_key"
response = completion(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": "Hello Gemini, how are you?"}],
    litellm_provider="google"
)
print(response)
