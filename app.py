from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import pandas as pd
import json
import os
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'bangrak2025_secret_key'  # Required for session management

EXCEL_FILE = 'Bang Rak Hackathon 2025 (Responses).xlsx'
SCORES_FILE = 'scores.json'

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///scores.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Password for access
PASSWORD = os.environ.get('SCORING_PASSWORD')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255), nullable=False)
    judge = db.Column(db.String(64), nullable=False)
    scores = db.Column(db.JSON, nullable=False)
    __table_args__ = (db.UniqueConstraint('team_name', 'judge', name='unique_team_judge'),)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def db_load_scores():
    all_scores = Score.query.all()
    result = {}
    for s in all_scores:
        if s.team_name not in result:
            result[s.team_name] = {}
        result[s.team_name][s.judge] = s.scores
    return result

def db_save_score(team_name, judge, judge_scores):
    score = Score.query.filter_by(team_name=team_name, judge=judge).first()
    if score:
        score.scores = judge_scores
    else:
        score = Score(team_name=team_name, judge=judge, scores=judge_scores)
        db.session.add(score)
    db.session.commit()

def db_clear_judge_score(team_name, judge):
    score = Score.query.filter_by(team_name=team_name, judge=judge).first()
    if score:
        db.session.delete(score)
        db.session.commit()

def db_reset_scores():
    Score.query.delete()
    db.session.commit()

# Helper to load team data from Excel
def load_teams():
    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna('')
    teams = df.to_dict(orient='records')
    return teams

JUDGES = ["Judge's Owen", "Judge's Kevin", "Judge's Ice"]
CRITERIA = [
    ("Problem-Solution Fit", 20),
    ("Creativity & Originality", 15),
    ("Feasibility & Prototyping", 20),
    ("Community Impact", 20),
    ("Scalability / Potential to Scale", 15),
    ("Pitching & Communication", 10),
]

LOCKED_CRITERION = 'Pitching & Communication'
LOCKED_SCORE = 10

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    teams = load_teams()
    scores = db_load_scores()
    team_statuses = []
    for team in teams:
        if not isinstance(team, dict):
            continue
        name = team.get("ชื่อทีม\nTeam's name", '')
        if not isinstance(name, str):
            continue
        name = name.strip()
        if not name:
            continue
        judge_status = {j: (name in scores and j in scores[name]) for j in JUDGES}
        team_statuses.append({'name': name, 'judge_status': judge_status})
    return render_template('team_list.html', team_statuses=team_statuses, judges=JUDGES)

@app.route('/team/<team_name>', methods=['GET', 'POST'])
@login_required
def team_detail(team_name):
    teams = load_teams()
    scores = db_load_scores()
    # Case-insensitive, whitespace-insensitive match
    team = next(
        (
            t for t in teams
            if isinstance(t.get("ชื่อทีม\nTeam's name", ''), str)
            and t.get("ชื่อทีม\nTeam's name", '').strip().lower() == team_name.strip().lower()
        ),
        None
    )
    if not team:
        return f"Team '{team_name}' not found", 404
    # Judge selection
    selected_judge = request.args.get('judge', JUDGES[0])
    if request.method == 'POST':
        # Update scores for selected judge
        judge_scores = {}
        for crit, max_score in CRITERIA:
            if crit == LOCKED_CRITERION:
                judge_scores[crit] = LOCKED_SCORE
            else:
                val = request.form.get(crit.replace(' ', '_'))
                try:
                    judge_scores[crit] = int(val)
                except:
                    judge_scores[crit] = 0
        db_save_score(team_name, selected_judge, judge_scores)
        return redirect(url_for('team_detail', team_name=team_name, judge=selected_judge))
    # Prepare scores for display
    team_scores = scores.get(team_name, {})
    judge_scores = team_scores.get(selected_judge, {})
    # Calculate total for each judge and average
    judge_totals = {}
    for judge in JUDGES:
        js = team_scores.get(judge, {})
        judge_totals[judge] = sum((js.get(crit, LOCKED_SCORE if crit == LOCKED_CRITERION else 0) for crit, _ in CRITERIA))
    # Calculate average per criteria and total
    avg_scores = {}
    for crit, _ in CRITERIA:
        if crit == LOCKED_CRITERION:
            avg_scores[crit] = LOCKED_SCORE
        else:
            avg_scores[crit] = round(sum(team_scores.get(j, {}).get(crit, 0) for j in JUDGES) / len(JUDGES), 2)
    avg_total = round(sum(judge_totals[j] for j in JUDGES) / len(JUDGES), 2)
    return render_template(
        'team_detail.html',
        team=team,
        judges=JUDGES,
        selected_judge=selected_judge,
        criteria=CRITERIA,
        judge_scores=judge_scores,
        judge_totals=judge_totals,
        avg_scores=avg_scores,
        avg_total=avg_total,
        locked_criterion=LOCKED_CRITERION,
        locked_score=LOCKED_SCORE
    )

@app.route('/team/<team_name>/clear/<judge>', methods=['POST'])
@login_required
def clear_judge_score(team_name, judge):
    db_clear_judge_score(team_name, judge)
    return redirect(url_for('team_detail', team_name=team_name, judge=judge))

@app.route('/ranking')
@login_required
def ranking():
    teams = load_teams()
    scores = db_load_scores()
    ranking_data = []
    for team in teams:
        if not isinstance(team, dict):
            continue
        name = team.get("ชื่อทีม\nTeam's name", '')
        if not isinstance(name, str):
            continue
        name = name.strip()
        if not name:
            continue
        team_scores = scores.get(name, {})
        judge_totals = []
        for judge in JUDGES:
            js = team_scores.get(judge, {})
            judge_totals.append(sum(js.get(crit, 0) for crit, _ in CRITERIA))
        avg_total = round(sum(judge_totals) / len(JUDGES), 2)
        ranking_data.append({
            'name': name,
            'judge_totals': judge_totals,
            'avg_total': avg_total
        })
    ranking_data.sort(key=lambda x: x['avg_total'], reverse=True)
    ranking_data = ranking_data[:20]  # Only top 20
    return render_template('ranking.html', ranking_data=ranking_data, judges=JUDGES)

@app.route('/reset_scores', methods=['POST'])
@login_required
def reset_scores():
    db_reset_scores()
    return redirect(url_for('ranking'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False) 