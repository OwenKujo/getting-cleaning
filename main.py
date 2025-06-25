from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import openai
import re
from openai import RateLimitError

from pythainlp.tokenize import word_tokenize
from meanings_data import (
    meanings_money, meanings_work, meanings_animal, meanings_activities,
    meanings_good_bad, meanigs_right_left, meanings_general, meanings_love
)

def Dream_Prediction(time_str, topic):
    # time_str is now one of: 'กลางวัน', 'หัวค่ำ', 'ยามดึก', 'ยามเช้า'
    if time_str == 'กลางวัน':
        time_msg = "ฝันกลางวัน: ไม่สามารถเชื่อถือได้\n➡ อาจเกิดจากจินตนาการ"
    elif time_str == 'หัวค่ำ':
        time_msg = "ฝันหัวค่ำ: ลางบอกเหตุถึงบุคคลทางไกล"
    elif time_str == 'ยามดึก':
        time_msg = "ฝันยามดึก: เรื่องจริงเกี่ยวกับครอบครัว"
    elif time_str == 'ยามเช้า':
        time_msg = "ฝันยามเช้า: จะเกิดขึ้นในเวลาอันใกล้"
    else:
        time_msg = "ไม่พบช่วงเวลาความฝัน"

    topic_msg = {
        '1': "หมวดการเงิน",
        '2': "หมวดความรัก",
        '3': "หมวดการงาน",
        '4': "หมวดสัตว์",
        '5': "หมวดเหตุการณ์ทั่วไป",
        '6': "หมวดทํษนายเรื่องดี เรื่องร้าย",
        '7': "หมวดเหมือนขวาร้าย ซ้ายดี",
        '8': "หมวดทั้่วไป",
    }.get(str(topic), "ไม่พบหัวข้อที่ต้องการทำนาย")

    return f"{time_msg}\n{topic_msg}"

# คำทำนายฝันตามหัวข้อต่างๆ

def find_dream_meaning(text, topic):
    tokens = word_tokenize(text, engine='newmm')
    if topic == '1':
        meanings = meanings_money
    elif topic == '2':
        meanings = meanings_love
    elif topic == '3':
        meanings = meanings_work
    elif topic == '4':
        meanings = meanings_animal
    elif topic == '5':
        meanings = meanings_activities
    elif topic == '6':
        meanings = meanings_good_bad    
    elif topic == '7':
        meanings = meanigs_right_left
    elif topic == '8':
        meanings = meanings_general
    else:
        return "หัวข้อไม่ถูกต้อง"

    for word in tokens:
        if word in meanings:
            meaning, numbers = meanings[word]
            return f"🔍 ฝันถึง '{word}'\n💡 ความหมาย: {meaning}\n🔢 เลขนำโชค: {' '.join(numbers)}"
    return "ขออภัย ไม่พบคำทำนายที่ตรงกับความฝันของคุณ"

def get_relevant_meanings(dream_text, topic):
    # เลือก meanings dict ตาม topic
    topic_map = {
        '1': meanings_money,
        '2': meanings_love,
        '3': meanings_work,
        '4': meanings_animal,
        '5': meanings_activities,
        '6': meanings_good_bad,
        '7': meanigs_right_left,
        '8': meanings_general,
    }
    meanings = topic_map.get(str(topic), {})
    tokens = word_tokenize(dream_text, engine='newmm')
    found = []
    for word in tokens:
        if word in meanings:
            meaning, numbers = meanings[word]
            found.append(f"'{word}': {meaning} (เลข: {' '.join(numbers)})")
    return '\n'.join(found) if found else 'ไม่พบข้อมูลในฐานข้อมูล'

def llm_interpret_dream_with_data(dream_text, time, topic):
    relevant = get_relevant_meanings(dream_text, topic)
    prompt = (
        f"ฐานข้อมูลทำนายฝัน:\n{relevant}\n\n"
        f"ผู้ใช้ฝันว่า: {dream_text}\nช่วงเวลา: {time}\nหัวข้อ: {topic}\n"
        "โปรดทำนายความหมายของความฝันนี้อย่างละเอียด อ้างอิงจากฐานข้อมูลข้างต้นด้วย และให้เลขนำโชคหลายชุด (3-6 ชุด ชุดละ 2-4 ตัวเลข) โดยแยกแต่ละชุดด้วยเว้นวรรคหรือคอมม่า และอธิบายเลขแต่ละชุดด้วย ถ้าไม่มีในฐานข้อมูลให้สร้างเลขนำโชคใหม่ที่เหมาะสมกับความฝันนี้"
    )
    client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    ai_text = response.choices[0].message.content
    return ai_text

# --- Flask App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fortune_q9tq_user:oYe6KE2wQauo9mG9d28StvKrbNwKyzx8@dpg-d1da0k7diees73cmobj0-a.oregon-postgres.render.com/fortune_q9tq'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    dreams = db.relationship('Dream', backref='user', lazy=True)

class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(10), nullable=False)
    result = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes (HTML templates to be added) ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Validation
        if not username or not password or not confirm_password:
            flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'danger')
            return render_template('register.html')
        if len(username) > 32:
            flash('ชื่อผู้ใช้ต้องไม่เกิน 32 ตัวอักษร', 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash('รหัสผ่านไม่ตรงกัน', 'danger')
            return render_template('register.html')
        # Check for duplicate username (case-insensitive)
        if User.query.filter(db.func.lower(User.username) == username.lower()).first():
            flash('ชื่อผู้ใช้นี้ถูกใช้แล้ว', 'danger')
            return render_template('register.html')
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน', 'danger')
            return render_template('login.html')
        user = User.query.filter(db.func.lower(User.username) == username.lower()).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('เข้าสู่ระบบสำเร็จ', 'success')
            return redirect(url_for('profile'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    dreams = Dream.query.filter_by(user_id=current_user.id).order_by(Dream.id.desc()).all()
    return render_template('profile.html', dreams=dreams)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    dream_text = request.form['dream_text']
    dream_time = request.form['dream_time']
    dream_topic = request.form['dream_topic']

    prediction = Dream_Prediction(dream_time, dream_topic)
    meaning = find_dream_meaning(dream_text, dream_topic)

    try:
        ai_text = llm_interpret_dream_with_data(dream_text, dream_time, dream_topic)
    except RateLimitError:
        ai_text = "ขออภัย ระบบ AI ไม่สามารถทำนายได้ในขณะนี้ (เกินโควต้าการใช้งาน OpenAI)"
    except Exception as e:
        ai_text = f"เกิดข้อผิดพลาดกับระบบ AI: {e}"

    new_dream = Dream(
        text=dream_text,
        time=dream_time,
        topic=dream_topic,
        result=ai_text,
        user_id=current_user.id
    )
    db.session.add(new_dream)
    db.session.commit()

    return render_template(
        'result.html',
        prediction=prediction,
        meaning=meaning,
        llm_result=ai_text
    )

@app.route('/delete_dream/<int:dream_id>', methods=['POST'])
@login_required
def delete_dream(dream_id):
    dream = Dream.query.get_or_404(dream_id)
    if dream.user_id != current_user.id:
        abort(403)
    db.session.delete(dream)
    db.session.commit()
    flash('ลบประวัติความฝันเรียบร้อยแล้ว', 'success')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
