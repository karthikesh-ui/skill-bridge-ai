import os

try:
    from google import genai
except ModuleNotFoundError:  # pragma: no cover - optional dependency handled at runtime
    genai = None


def guidance(career, question, pathway):
    fallback = f"{career['name']} may suit your interests. Start by reviewing {pathway['stream']}. Compare the listed course routes, practice {', '.join(pathway['skills'][:2])}, and verify current admission or exam requirements from official sources."
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key or key == 'your_api_key_here':
        return {'text': fallback, 'source': 'fallback'}

    prompt = (f"You are a friendly career explainer for an Indian student. Use ONLY these curated facts: "
              f"career={career['name']}; stream={pathway['stream']}; courses={pathway['degree']}; "
              f"exams={pathway['exams']}; skills={pathway['skills']}. "
              f"Student question: {question[:500]}. Do not invent eligibility. Keep under 130 words. Advise official verification.")

    try:
        if genai is None:
            raise RuntimeError('google-genai package is not installed')

        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        answer = getattr(response, 'text', None)
        if not answer:
            candidates = getattr(response, 'candidates', []) or []
            for candidate in candidates:
                parts = getattr(getattr(candidate, 'content', None), 'parts', []) or []
                for part in parts:
                    text = getattr(part, 'text', None)
                    if text:
                        answer = text
                        break
                if answer:
                    break

        if not answer:
            raise ValueError('Gemini returned no text content')

        return {'text': answer, 'source': 'gemini'}
    except Exception:
        return {'text': fallback, 'source': 'fallback'}
