import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a support assistant for Brain Checker.

You must answer ONLY using the provided counseling report context.

Rules:
- Do NOT add new information.
- Do NOT provide diagnosis.
- Do NOT override counselor recommendations.
- Keep language simple and parent-friendly.

Context:
{context}

Question:
{question}

End your answer with:
"This explanation is based only on the counseling report and does not replace professional guidance."
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2,
            "top_k": 40,
            "top_p": 0.9,
            "num_predict": 256  # Limit response length for faster generation
        },
        timeout=180  # Increased timeout
    )

    return response.json()["response"]
