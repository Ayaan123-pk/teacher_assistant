
import config
from openai import OpenAI

GROQ_URL = "https://api.groq.com/openai/v1"

MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b"
]

def generate_response(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 512
) -> str:

    key = getattr(config, "GROQ_API_KEY", None)

    if not key:
        return "Error: Groq API key is missing."

    client = OpenAI(
        api_key=key,
        base_url=GROQ_URL
    )

    errors = []

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            answer = response.choices[0].message.content

            if answer:
                return answer

            errors.append(f"{model}: Empty response")

        except Exception as e:
            errors.append(f"{model}: {str(e)}")

    return "All Groq models failed:\n" + "\n".join(errors)
