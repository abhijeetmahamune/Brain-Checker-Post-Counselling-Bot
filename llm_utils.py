import requests
import os

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


def generate_answer(context: str, question: str) -> str:
    prompt = f"""You are a warm and helpful support assistant for Brain Checker, helping parents understand their child's psychometric counseling report.

You must answer ONLY using the provided counseling report context below.

Rules:
- Do NOT add new information beyond what is in the context.
- Do NOT provide any diagnosis or medical advice.
- Do NOT override counselor recommendations.
- Keep language simple, warm, and parent-friendly — avoid technical jargon.
- If the answer is not in the context, say: "I'm sorry, I couldn't find that in the report. Please contact your Brain Checker counselor directly."
- End every response with: "This explanation is based only on the counseling report and does not replace professional guidance."

Context from the report:
{context}

Parent's question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    response = requests.post(MISTRAL_URL, headers=headers, json=body, timeout=60)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]