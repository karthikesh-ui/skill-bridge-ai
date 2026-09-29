import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'data'

def read(name):
    return json.loads((DATA / f'{name}.json').read_text(encoding='utf-8'))

def career(career_id):
    return next((c for c in read('careers') if c['id'] == career_id), None)

def discover(answers):
    """Transparent exploration score: shared interests, with profile-aware route guidance.

    This is an ordering aid, never an aptitude test or probability.
    """
    interests = set(answers.get('interests') or [])
    profile = answers.get('profile') or {}
    no_math = bool(profile.get('no_math'))
    no_biology = bool(profile.get('no_biology'))
    no_btech = bool(profile.get('no_btech'))
    results = []
    paths = read('pathways')
    for c in read('careers'):
        shared = sorted(interests.intersection(c['tags']))
        score = len(shared)
        advice = []
        data = paths[c['id']]
        if no_math and c['category'] == 'Engineering':
            advice.append('Engineering admission often has subject requirements. Check the latest official rules and compare other routes.')
        if no_biology and c['id'] in ('doctor', 'nurse', 'pharmacist'):
            advice.append('Healthcare courses may require Biology or other science subjects. Check each course’s current rules.')
        if no_btech and 'B.Tech' in data['degree']:
            advice.append('You prefer a route outside B.Tech. Compare the other course options shown in the pathway.')
        if answers.get('education') in ('In 11th', '12th completed', 'In college'):
            advice.append('You can start from your current education stage; you do not need to restart at 10th.')
        results.append({**c, 'match': score,
                        'why': 'You selected ' + ', '.join(shared) + '.' if shared else 'Explore this career to compare it with your interests.',
                        'route_note': ' '.join(advice),
                        'course_preview': [x['name'] for x in data['course_options'][:2]]})
    return sorted(results, key=lambda c: (-c['match'], c['name']))[:8]

def build_pathway(career_id, profile):
    c = career(career_id)
    if not c:
        return None
    info = read('pathways')[career_id]
    stage = profile.get('education') or '10th completed'
    notes = [f'Your current stage: {stage}. Begin with the step relevant to you.']
    if profile.get('no_math'):
        notes.append('Without Mathematics, verify each course’s subject requirements and compare alternative routes.')
    if profile.get('no_biology'):
        notes.append('Without Biology, verify requirements for any healthcare course before applying.')
    if profile.get('no_btech'):
        notes.append('You prefer not to take B.Tech; explore the other courses listed below.')
    notes.append('Admission and exam rules can change; confirm them with official sources.')
    return {'career': c, **info, 'personal_note': ' '.join(notes)}
