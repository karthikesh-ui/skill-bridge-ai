import unittest
from unittest.mock import patch

from app import app

class AppTests(unittest.TestCase):
    def setUp(self): self.client = app.test_client()

    def test_main_flow(self):
        self.assertEqual(self.client.get('/api/health').json['status'], 'ok')
        careers = self.client.get('/api/careers').json
        self.assertGreaterEqual(len(careers), 40)
        for c in careers:
            detail = self.client.get('/api/career/' + c['id'])
            self.assertEqual(detail.status_code, 200)
            self.assertTrue(detail.json['course_options'])
            path = self.client.post('/api/pathway', json={'career_id': c['id'], 'profile': {}})
            self.assertEqual(path.status_code, 200)
            self.assertTrue(path.json['routes'][0]['stages'])
        matches = self.client.post('/api/career/discover', json={
            'subjects':['Computers', 'Mathematics'],
            'activities':['coding'],
            'career_areas':['Technology'],
            'profile':{'no_math': True, 'no_btech': True}
        }).json
        self.assertTrue(matches['results'] and matches['results'][0]['match'] > 0)
        self.assertTrue(any(m['route_note'] for m in matches['results']))
        path = self.client.post('/api/pathway', json={
            'career_id':'software-engineer','profile':{'no_math':True,'no_btech':True}
        }).json
        self.assertGreaterEqual(len(path['routes']), 2)
        self.assertIn('Without Mathematics', path['personal_note'])
        self.assertIn('prefer not to take B.Tech', path['personal_note'])
        self.assertEqual(self.client.post('/api/career/guidance', json={
            'career_id':'software-engineer'
        }).json['source'], 'fallback')
        for page in ['/','/discovery','/careers','/career-details','/pathway',
                     '/roadmap','/dashboard','/resources','/profile']:
            self.assertEqual(self.client.get(page).status_code, 200, page)

    def test_answer_profiles_rank_relevant_professions(self):
        profiles = [
            ({'subjects': ['Biology'], 'activities': ['helping people'], 'career_areas': ['Healthcare']}, {'doctor', 'nurse', 'pharmacist'}),
            ({'subjects': ['Computers'], 'activities': ['coding'], 'career_areas': ['Technology']}, {'software-engineer', 'ai-engineer', 'cybersecurity', 'web-developer'}),
            ({'subjects': ['Art'], 'activities': ['designing'], 'career_areas': ['Creative/Design/Media']}, {'designer', 'graphic-designer', 'animator', 'interior-designer'}),
            ({'subjects': ['Business/Accounting'], 'activities': ['solving numerical problems'], 'career_areas': ['Business/Commerce']}, {'chartered-accountant', 'accountant', 'financial-analyst', 'finance'}),
            ({'subjects': ['Social Science'], 'activities': ['helping people'], 'career_areas': ['Public Service']}, {'civil-services', 'state-government', 'government-services'}),
            ({'subjects': ['Physics'], 'activities': ['building/repairing things'], 'career_areas': ['Engineering']}, {'mechanical-engineer', 'civil-engineer', 'electrical-engineer', 'electronics-engineer'}),
        ]
        for answers, expected in profiles:
            with self.subTest(answers=answers):
                response = self.client.post('/api/career/discover', json=answers).json
                self.assertTrue(response['results'])
                self.assertTrue(all(item['match'] > 0 for item in response['results']))
                self.assertTrue(expected.intersection(item['id'] for item in response['results']))
                self.assertTrue(all('subjects:' in item['why'] or 'activities:' in item['why'] for item in response['results']))

    def test_unsure_and_empty_answers_do_not_default_to_technology(self):
        response = self.client.post('/api/career/discover', json={
            'subjects': [], 'activities': [], 'career_areas': [],
            'work_preference': 'both', 'competitive_exams': 'unsure',
            'interests': ['computers', 'problems']
        }).json
        self.assertTrue(response['needs_more'])
        self.assertEqual(response['results'], [])
        self.assertEqual(response['related'], [])

    def test_discovery_is_deterministic_and_unsure_is_neutral(self):
        answers = {'subjects': ['Biology'], 'activities': ['helping people'], 'career_areas': ['Healthcare']}
        first = self.client.post('/api/career/discover', json=answers).json
        second = self.client.post('/api/career/discover', json=answers).json
        with_unsure = self.client.post('/api/career/discover', json={**answers, 'competitive_exams': 'unsure'}).json
        self.assertEqual(first, second)
        self.assertEqual([item['id'] for item in first['results']], [item['id'] for item in with_unsure['results']])
        self.assertFalse(set(item['id'] for item in first['results']) & set(item['id'] for item in first['related']))

    def test_every_career_has_matching_skills_exams_and_usable_pathway(self):
        from backend.career_engine import read

        careers = read('careers')
        ids = {item['id'] for item in careers}
        self.assertEqual(len(ids), len(careers))
        self.assertTrue(ids <= set(read('matching')))
        self.assertTrue(ids <= set(read('skills')))
        self.assertTrue(ids <= set(read('exams')))
        self.assertTrue(ids <= set(read('pathways')))
        for career_id in ids:
            detail = self.client.get('/api/career/' + career_id)
            self.assertEqual(detail.status_code, 200, career_id)
            self.assertTrue(detail.json['course_options'], career_id)
            self.assertTrue(detail.json['skills'], career_id)
            self.assertTrue(detail.json['routes'][0]['stages'], career_id)

    def test_guidance_uses_gemini_client_when_key_is_present(self):
        from backend.gemini_service import guidance

        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            with patch('backend.gemini_service.genai') as mock_genai:
                mock_client = mock_genai.Client.return_value
                mock_client.models.generate_content.return_value.text = 'Custom Gemini answer'

                result = guidance({
                    'name': 'Software Engineer',
                    'stream': 'Computer Science',
                    'degree': 'B.Tech Computer Science',
                    'exams': ['JEE'],
                    'skills': ['Python', 'Algorithms']
                }, 'What should I study?', {
                    'stream': 'Computer Science',
                    'degree': 'B.Tech Computer Science',
                    'exams': ['JEE'],
                    'skills': ['Python', 'Algorithms']
                })

                self.assertEqual(result['source'], 'gemini')
                self.assertEqual(result['text'], 'Custom Gemini answer')
                mock_genai.Client.assert_called_once_with(api_key='test-key')

if __name__ == '__main__': unittest.main()
