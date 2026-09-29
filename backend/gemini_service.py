import os
import requests

def guidance(career, question, pathway):
    fallback = f"{career['name']} may suit your interests. Start by reviewing {pathway['stream']}. Compare the listed course routes, practice {', '.join(pathway['skills'][:2])}, and verify current admission or exam requirements from official sources."
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key or key == 'your_api_key_here': return {'text': fallback, 'source': 'fallback'}
    prompt = (f"You are a friendly career explainer for an Indian student. Use ONLY these curated facts: "
              f"career={career['name']}; stream={pathway['stream']}; courses={pathway['degree']}; "
              f"exams={pathway['exams']}; skills={pathway['skills']}. "
              f"Student question: {question[:500]}. Do not invent eligibility. Keep under 130 words. Advise official verification.")
    try:
        response = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
            headers={'x-goog-api-key': key},json={'contents':[{'parts':[{'text':prompt}]}]},timeout=12)
        response.raise_for_status()
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        return {'text':answer, 'source':'gemini'}
    except (requests.RequestException, KeyError, IndexError, TypeError):
        return {'text':fallback, 'source':'fallback'}
