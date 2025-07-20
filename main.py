from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import json
import os

app = Flask(__name__)

EXCEL_FILE = 'Bang Rak Hackathon 2025 (Responses).xlsx'
SCORES_FILE = 'scores.json'

# Helper to load team data from Excel
def load_teams():
    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna('')
    teams = df.to_dict(orient='records')
    return teams

# Helper to load scores from JSON
def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Helper to save scores to JSON
def save_scores(scores):
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    teams = load_teams()
    scores = load_scores()
    # Assume each team has a unique 'Team Name' field
    for team in teams:
        team_id = team.get('Team Name', str(team))
        team['score'] = scores.get(team_id, '')
    return render_template('teams.html', teams=teams)

@app.route('/score/<team_id>', methods=['POST'])
def update_score(team_id):
    score = request.form.get('score')
    scores = load_scores()
    scores[team_id] = score
    save_scores(scores)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
