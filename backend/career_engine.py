import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'data'

MATCH_WEIGHTS = {
    'subjects': 3,
    'activities': 2,
    'career_areas': 2,
    'work_preference': 1,
    'competitive_exams': 1,
}

def read(name):
    data = json.loads((DATA / f'{name}.json').read_text(encoding='utf-8'))
    extensions = json.loads((DATA / 'career_extensions.json').read_text(encoding='utf-8'))
    if name == 'careers':
        return data + [{key: value for key, value in item.items() if key not in ('matching', 'stream', 'degree', 'exams', 'skills', 'preparation', 'experience', 'alternative', 'courses')} for item in extensions]
    if name == 'matching':
        data.update({item['id']: item['matching'] for item in extensions})
    elif name == 'skills':
        data.update({item['id']: item['skills'] for item in extensions})
    elif name == 'exams':
        data.update({item['id']: item['exams'] for item in extensions})
    elif name == 'pathways':
        for item in extensions:
            course_options = [
                {'name': course, 'note': 'Illustrative option only. Confirm recognition, eligibility, fees and admission details with official institution sources.'}
                for course in item['courses']
            ]
            common_stages = [
                {'title': 'After 10th / current stage', 'detail': f"After 10th, compare subject combinations and recognized entry-level options related to {item['category'].lower()}.", 'alternatives': item['alternative']},
                {'title': '11th–12th / preparation', 'detail': item['stream'], 'alternatives': 'Subject combinations and admission rules vary; verify current official requirements.'},
                {'title': 'Course / further study', 'detail': item['degree'], 'alternatives': item['alternative']},
                {'title': 'Skills', 'detail': ', '.join(item['skills']), 'alternatives': 'Build skills through appropriate study and supervised practice.'},
                {'title': 'Practical experience', 'detail': item['experience'], 'alternatives': 'Choose a safe, supervised project or learning activity.'},
                {'title': 'Career exploration', 'detail': item['name'], 'alternatives': 'Role titles and entry requirements vary between employers and regions.'},
            ]
            alternate_stages = [dict(stage) for stage in common_stages]
            alternate_stages[2] = {'title': 'Alternative route', 'detail': item['alternative'], 'alternatives': item['degree']}
            data[item['id']] = {
                'overview': item['description'],
                'stream': item['stream'],
                'degree': item['degree'],
                'exams': item['exams'],
                'skills': item['skills'],
                'preparation': item['preparation'],
                'routes': [{'name': 'Example route', 'stages': common_stages}, {'name': 'Alternative route', 'stages': alternate_stages}],
                'course_options': course_options,
                'decision_help': 'These are illustrative routes, not admission guarantees. Compare current official rules, recognition and costs before deciding.',
                'starter_actions': [f"Explore {item['courses'][0]}", f"Practise {item['skills'][0]}", item['preparation']],
            }
    return data

def career(career_id):
    return next((c for c in read('careers') if c['id'] == career_id), None)

def discover(answers):
    """Rank careers by normalized overlap; this is an exploration aid, not a probability."""
    answer_fields = {
        'subjects': answers.get('subjects') or [],
        'activities': answers.get('activities') or [],
        'career_areas': answers.get('career_areas') or [],
    }
    for field, values in answer_fields.items():
        if isinstance(values, str):
            answer_fields[field] = [values]
        answer_fields[field] = {str(value).strip().casefold() for value in answer_fields[field] if str(value).strip()}
    work_preference = str(answers.get('work_preference') or '').strip().casefold()
    exam_interest = str(answers.get('competitive_exams') or '').strip().casefold()
    profile = answers.get('profile') or {}
    no_math = bool(profile.get('no_math'))
    no_biology = bool(profile.get('no_biology'))
    no_btech = bool(profile.get('no_btech'))
    results = []
    has_answers = any(answer_fields.values())
    if not has_answers:
        return {
            'results': [],
            'related': [],
            'needs_more': True,
            'message': 'Choose one or more subjects, activities, or areas to get personalized suggestions.',
        }
    paths = read('pathways')
    matching_profiles = read('matching')
    for c in read('careers'):
        matching = matching_profiles.get(c['id'], {})
        denominator = sum(MATCH_WEIGHTS[field] for field, values in answer_fields.items() if values)
        denominator += MATCH_WEIGHTS['work_preference'] if work_preference in ('practical', 'theoretical', 'both') else 0
        denominator += MATCH_WEIGHTS['competitive_exams'] if exam_interest in ('interested', 'not interested') else 0
        weighted_score = 0
        matched = {}
        for field, answers_for_field in answer_fields.items():
            options = matching.get(field, [])
            if answers_for_field and options:
                option_map = {str(value).casefold(): value for value in options}
                shared = sorted(answers_for_field.intersection(option_map), key=str.casefold)
                matched[field] = [option_map[value] for value in shared]
                weighted_score += MATCH_WEIGHTS[field] * len(shared) / len(answers_for_field)
        if work_preference in ('practical', 'theoretical', 'both'):
            if work_preference in matching.get('preferences', []):
                weighted_score += MATCH_WEIGHTS['work_preference']
        if exam_interest in ('interested', 'not interested'):
            if matching.get('competitive_exams_possible') == (exam_interest == 'interested'):
                weighted_score += MATCH_WEIGHTS['competitive_exams']
        if weighted_score == 0:
            continue
        advice = []
        data = paths[c['id']]
        if no_math and c['category'] == 'Engineering':
            advice.append('Engineering admission often has subject requirements. Check the latest official rules and compare other routes.')
        if no_biology and c['id'] in ('doctor', 'nurse', 'pharmacist', 'physiotherapist', 'medical-lab-technologist'):
            advice.append('Healthcare courses may require Biology or other science subjects. Check each course’s current rules.')
        if no_btech and 'B.Tech' in data['degree']:
            advice.append('You prefer a route outside B.Tech. Compare the other course options shown in the pathway.')
        if answers.get('education') in ('In 11th', '12th completed', 'In college'):
            advice.append('You can start from your current education stage; you do not need to restart at 10th.')
        matched_labels = [
            f"subjects: {', '.join(matched.get('subjects', [])) or 'none matched'}",
            f"activities: {', '.join(matched.get('activities', [])) or 'none matched'}",
        ]
        if matched.get('career_areas'):
            matched_labels.append(f"career areas: {', '.join(matched['career_areas'])}")
        if work_preference in matching.get('preferences', []):
            matched_labels.append(f"work preference: {work_preference}")
        if exam_interest in ('interested', 'not interested') and matching.get('competitive_exams_possible') == (exam_interest == 'interested'):
            matched_labels.append(f"exam preference: {exam_interest}")
        normalized_score = weighted_score / denominator if denominator else 0
        results.append({**c, 'match': round(normalized_score, 4),
                        'why': 'Matched ' + '; '.join(matched_labels) + '.',
                        'route_note': ' '.join(advice),
                        'course_preview': [x['name'] for x in data['course_options'][:2]],
                        'matched_subjects': matched.get('subjects', []),
                        'matched_activities': matched.get('activities', [])})
    results.sort(key=lambda result: (-result['match'], result['name']))
    return {
        'results': results[:6],
        'related': results[6:12],
        'needs_more': len(results) < 4,
        'message': 'Add another subject, activity, or career area for more personalized suggestions.' if len(results) < 4 else '',
    }

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
