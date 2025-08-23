import requests
import json
from django.conf import settings

def suggest_titles(content: str):
    """
    Suggests catchy blog titles for a given content string using the Gemini API.
    This version includes more robust error handling and response structure control.

    Args:
        content (str): The body of the blog post to generate titles for.

    Returns:
        list: A list of suggested titles, or a list with a single error message.
    """
    model = "models/gemini-2.5-flash-preview-05-20"
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={settings.GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Suggest 5 catchy, numbered blog titles for this content. Respond with just the numbered list and no extra text. If you cannot generate titles, respond with 'no-titles-generated':\n\n{content}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.5,
            "responseMimeType": "text/plain"  # Force a simple text response
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()

        data = res.json()

        if not data.get("candidates"):
            return [f"Gemini API returned an empty response. Response data: {data}"]

        candidate = data["candidates"][0]

        if "content" not in candidate:
            return [f"Gemini API response blocked. Finish reason: {candidate.get('finishReason', 'N/A')}"]

        text_output = candidate["content"]["parts"][0]["text"]

        if "no-titles-generated" in text_output.lower():
            return ["The model could not generate titles for the provided content."]

        # Split into individual suggestions
        suggestions = [line.strip(" -0123456789.") for line in text_output.split("\n") if line.strip()]

        if not suggestions:
            return ["No titles could be extracted from the API response."]

        return suggestions

    except requests.exceptions.RequestException as req_err:
        return [f"Network or API request error: {req_err}"]
    except (KeyError, IndexError, json.JSONDecodeError) as parse_err:
        return [f"Unexpected API response structure or parsing error: {parse_err}. Response data: {data}"]
    except Exception as e:
        return [f"An unexpected error occurred: {e}"]
