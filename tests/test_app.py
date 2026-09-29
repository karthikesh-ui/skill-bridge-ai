import unittest
from app import app

class AppTests(unittest.TestCase):
    def setUp(self): self.client = app.test_client()

    def test_main_flow(self):
        self.assertEqual(self.client.get('/api/health').json['status'], 'ok')
        careers = self.client.get('/api/careers').json
        self.assertGreaterEqual(len(careers), 20)
        for c in careers:
            detail = self.client.get('/api/career/' + c['id'])
            self.assertEqual(detail.status_code, 200)
            self.assertTrue(detail.json['course_options'])
            path = self.client.post('/api/pathway', json={'career_id': c['id'], 'profile': {}})
            self.assertEqual(path.status_code, 200)
            self.assertTrue(path.json['routes'][0]['stages'])
        matches = self.client.post('/api/career/discover', json={
            'interests':['computers','math'],
            'profile':{'no_math': True, 'no_btech': True}
        }).json
        self.assertTrue(matches and matches[0]['match'] > 0)
        self.assertTrue(any(m['route_note'] for m in matches))
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

if __name__ == '__main__': unittest.main()
