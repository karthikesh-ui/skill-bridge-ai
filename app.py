from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from backend.career_engine import read, career, discover, build_pathway
from backend.gemini_service import guidance
load_dotenv()
app = Flask(__name__)
PAGES = ['index','discovery','careers','career-details','pathway','roadmap','dashboard','resources','profile']
@app.get('/')
def home(): return render_template('index.html', page='index')
@app.get('/<page>')
def page(page):
    if page not in PAGES: return jsonify(error='Page not found'),404
    return render_template(page+'.html', page=page)
@app.get('/api/health')
def health(): return jsonify(status='ok')
@app.get('/api/careers')
def careers(): return jsonify(read('careers'))
@app.get('/api/career/<career_id>')
def career_details(career_id):
    c=career(career_id)
    return jsonify({**c,**read('pathways')[career_id]}) if c else (jsonify(error='Career not found'),404)
@app.post('/api/career/discover')
def career_discover():
    body=request.get_json(silent=True) or {}
    return jsonify(discover(body))
@app.post('/api/pathway')
def pathway():
    body=request.get_json(silent=True) or {}
    result=build_pathway(body.get('career_id'), body.get('profile') or {})
    return jsonify(result) if result else (jsonify(error='Career not found'),404)
@app.post('/api/career/guidance')
def career_guidance():
    body=request.get_json(silent=True) or {}; cid=body.get('career_id')
    c=career(cid)
    if not c: return jsonify(error='Career not found'),404
    return jsonify(guidance(c, str(body.get('question','What should I do next?')), read('pathways')[cid]))
if __name__ == '__main__': app.run(debug=True, port=5000)
