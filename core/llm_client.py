from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm(system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # replace llama3-70b-8192 with this,  # free + very capable
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content