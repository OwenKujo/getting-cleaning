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

JUDGES = ["Judge's Owen", "Judge's Kevin", "Judge's Ice"]
CRITERIA = [
    ("Problem-Solution Fit", 20),
    ("Creativity & Originality", 15),
    ("Feasibility & Prototyping", 20),
    ("Community Impact", 20),
    ("Scalability / Potential to Scale", 15),
    ("Pitching & Communication", 10),
]

@app.route('/')
def home():
    teams = load_teams()
    scores = load_scores()
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
def team_detail(team_name):
    teams = load_teams()
    scores = load_scores()
    team = next((t for t in teams if t.get("ชื่อทีม\nTeam's name") == team_name), None)
    if not team:
        return f"Team '{team_name}' not found", 404
    # Judge selection
    selected_judge = request.args.get('judge', JUDGES[0])
    if request.method == 'POST':
        # Update scores for selected judge
        judge_scores = {}
        for crit, max_score in CRITERIA:
            val = request.form.get(crit.replace(' ', '_'))
            try:
                judge_scores[crit] = int(val)
            except:
                judge_scores[crit] = 0
        if team_name not in scores:
            scores[team_name] = {}
        scores[team_name][selected_judge] = judge_scores
        save_scores(scores)
        return redirect(url_for('team_detail', team_name=team_name, judge=selected_judge))
    # Prepare scores for display
    team_scores = scores.get(team_name, {})
    judge_scores = team_scores.get(selected_judge, {})
    # Calculate total for each judge and average
    judge_totals = {}
    for judge in JUDGES:
        js = team_scores.get(judge, {})
        judge_totals[judge] = sum(js.get(crit, 0) for crit, _ in CRITERIA)
    # Calculate average per criteria and total
    avg_scores = {}
    for crit, _ in CRITERIA:
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
        avg_total=avg_total
    )

@app.route('/team/<team_name>/clear/<judge>', methods=['POST'])
def clear_judge_score(team_name, judge):
    scores = load_scores()
    if team_name in scores and judge in scores[team_name]:
        del scores[team_name][judge]
        # If no judges left, remove the team entry
        if not scores[team_name]:
            del scores[team_name]
        save_scores(scores)
    return redirect(url_for('team_detail', team_name=team_name, judge=judge))

@app.route('/ranking')
def ranking():
    teams = load_teams()
    scores = load_scores()
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
def reset_scores():
    save_scores({})
    return redirect(url_for('ranking'))

if __name__ == '__main__':
    app.run(debug=False) 