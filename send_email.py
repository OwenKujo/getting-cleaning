import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

# Usage: email_dict = {'to': 'recipient@example.com', 'subject': 'Hello', 'body': 'This is the message.'}

def send_email(email_dict, attachments=None):
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError('EMAIL_USER and EMAIL_PASS must be set in environment variables.')
    msg = EmailMessage()
    msg['From'] = EMAIL_USER
    msg['To'] = email_dict['to']
    msg['Subject'] = email_dict['subject']
    msg.set_content(email_dict['body'])
    # Attach files if any
    if attachments:
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        print(f"Email sent to {email_dict['to']}")

IS_TEST = False  # เปลี่ยนเป็น False เมื่อต้องการส่งจริง

finalist_attachments = [
    'S__5980222.jpg',
    'S__5980223.jpg',
    'S__47915015.jpg',
]

if IS_TEST:
    teams = [
        {
            'team_name': 'MOCK TEAM (append)',
            'emails': [
                'owenrapeepat@gmail.com',
                'rapeepatpromlat@gmail.com',
            ]
        }
    ]
else:
    teams = [
        {'team_name': 'BAIPOR….KRUB ( ใบปอ….ครับ )', 'emails': ['Cxchy2008@gmail.com', 't.thiraphotiwat@gmail.com', 'nsorana@cmkl.ac.th']},
        {'team_name': 'Booduk', 'emails': ['Isaree2348@gmail.com', 'pakornpan4126@gmail.com', 'engeng.khammakorn@gmail.com', 'nopparinbbb@gmail.com']},
        {'team_name': 'BANGLAKSOI9', 'emails': ['petchppsb@gmail.com', 'pataratonh@gmail.com', 'Pei15426@gmail.com', 'ts.thanachot@gmail.com']},
        {'team_name': 'BangRak Arts Trails', 'emails': ['miwphudit@gmail.com', 'Vongsathorn169@gmail.com', 'Beem.eur@gmail.com']},
        {'team_name': 'Bangrakonnect', 'emails': ['kruethaikp@gmail.com', 'sirapat.kaw@outlook.com', 'teemtat.wee@gmail.com']},
        {'team_name': 'BangRukThur', 'emails': ['salakit.ptrp@gmail.com', 'Case.yokyisa@gmail.com', 'iampeterpork@gmail.com', 'nnatchanon187@gmail.com', 'warawutvichaiya@gmail.com']},
        {'team_name': 'Eureka', 'emails': ['Patterinwza@gmail.com', 'bhronpailinmancharoen@gmail.com', 'oranassy@gmail.com']},
        {'team_name': 'Love Crafters', 'emails': ['onvilasinee@gmail.com', 'Thayanee1501@gmail.com', 'thanatorn.sawatsri@gmail.com', 'pawada.umpriwan@gmail.com']},
        {'team_name': 'LRAS', 'emails': ['p.puthiphat@gmail.com', 'tinthai.boot@gmail.com', 'phtryu555@gmail.com', 'tik.jedsdp@gmail.com']},
        {'team_name': 'NextStep Bang Rak', 'emails': ['charudejs@gmail.com', 'p.natchater@gmail.com', 'ruephawat@gmail.com', 'porporkpp23@hotmail.com']},
        {'team_name': 'Welovebangrak', 'emails': ['cartoon1742@gmail.com', 'auntidarat0@gmail.com', 'bmnamhapit@gmail.com', 'modbenjarut@gmail.com', 'siraprapakraikaew@gmail.com']},
        {'team_name': 'RakSure', 'emails': ['rapeeratchen@gmail.com', 'greatestpooh@gmail.com', 'psastserm@gmail.com', 'pugun.supichaya@gmail.com']},
        {'team_name': 'The Bangrak Way', 'emails': ['napasorn.tra@student.mahidol.edu', 'suwichadachbdu562@gmail.com', 'notechaporn03096@gmail.com']},
        {'team_name': 'แชทบอทอาจไม่มีหัวใจ แต่ตอบเธอไวกว่าแฟน', 'emails': ['addeen.sk@gmail.com', 'glittin.oun@student.mahidol.edu', '37022@sjc.ac.th', 'charutwan.ratangsu@gmail.com']},
        {'team_name': 'บางทีก็อาจจะยัง', 'emails': ['pan21468@gmail.com', 'pongtawan.klysubun@gmail.com', 'pimnapatkoov@gmail.com', 'stu44802@samakkhi.ac.th']},
    ]

for team in teams:
    to_emails = [e for e in team['emails'] if e]
    body = f'''
สวัสดีฮีโร่ BangRak Hackathon 2025!

ขอแสดงความยินดีกับทีม "{team["team_name"]}" ที่ได้เป็น Finalist 15 ทีมสุดท้ายของ BangRak Hackathon 2025
ทีมงานขอชื่นชมในความคิดสร้างสรรค์และความตั้งใจของทุกคน

**เข้าร่วมกลุ่ม Finalist ได้ที่ LINE Openchat:**
https://line.me/ti/g2/nPjWw3_g3t1FaB3VNhHq9lziqPQPCyjlWdJKCQ?utm_source=invitation&utm_medium=link_copy&utm_campaign=default

**กรุณายืนยันสิทธิ์การเข้าร่วมรอบชิงชนะเลิศ**
และส่งรายชื่อสมาชิกที่จะเข้าร่วม Bootcamp ในวันที่ 2-3 สิงหาคม 2568 สถานที่ TCDC Bangkok (หากไม่มีเหตุจำเป็น ทีมงานอยากให้มาทั้งทีม) 
โดยยืนยันสิทธิ์การเข้าร่วม และส่งชื่อสมาชิกที่เข้าร่วม Bootcamp ด้วยการตอบกลับอีเมลนี้

โปรดดูรายละเอียดและกำหนดการในไฟล์แนบ หากมีข้อสงสัยหรือข้อมูลเพิ่มเติม ทีมงานจะแจ้งให้ทราบทาง Facebook, Instagram และอีเมลนี้

ขอให้โชคดีในรอบชิงชนะเลิศ!
ทีมงาน BangRak Hackathon 2025
'''
    finalist_email_data = {
        'to': ','.join(to_emails),
        'subject': 'ขอแสดงความยินดี! ทีมคุณคือ Finalist BangRak Hackathon 2025',
        'body': body
    }
    send_email(finalist_email_data, attachments=finalist_attachments)
