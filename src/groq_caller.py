"""
Groq LLM caller with automatic rate limit retry.
"""
import litellm
import time
import re
import os

litellm.suppress_debug_info = True
GROQ_MODEL = "llama-3.1-8b-instant"


def call_groq(system_prompt, user_prompt, max_tokens=900, retries=6):
    for attempt in range(retries):
        try:
            resp = litellm.completion(
                model="groq/" + GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                api_key=os.environ["GROQ_API_KEY"],
                max_tokens=max_tokens,
                temperature=0.1,
            )
            content = resp.choices[0].message.content
            if content and content.strip():
                return content.strip()
            time.sleep(20)
        except Exception as e:
            err = str(e)
            if "429" in err or "rate_limit" in err.lower():
                match = re.search(r"try again in ([\d.]+)s", err)
                wait = float(match.group(1)) + 5 if match else 30 * (attempt + 1)
                time.sleep(wait)
            else:
                time.sleep(15)
    return "Analysis unavailable."