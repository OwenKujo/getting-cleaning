import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

# Usage: email_dict = {'to': 'recipient@example.com', 'subject': 'Hello', 'body': 'This is the message.'}

def send_email(email_dict):
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
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        print(f"Email sent to {email_dict['to']}")

# Example usage (uncomment to use):
email_data = {
    'to': '',  # will be set in the loop
    'subject': 'ยืนยันการสมัคร BangRak Hackathon 2025',
    'body': '''สวัสดีฮีโร่ BangRak Hackathon 2025!

ทีมงานได้รับไอเดียและข้อเสนอสุดสร้างสรรค์ของทีมคุณเรียบร้อยแล้ว
ขอบคุณที่กล้าคิด กล้าฝัน และพร้อมลุยไปกับเรา
ทุกไอเดียของคุณคือพลังสำคัญที่จะเปลี่ยนแปลงบางรักให้ดียิ่งขึ้น

ไม่ว่าผลจะเป็นอย่างไร คุณคือฮีโร่ของบางรักและแรงบันดาลใจของพวกเรา
ถ้ามีข่าวสารหรือข้อมูลเพิ่มเติม ทีมงานจะแจ้งให้ทราบทาง Facebook, Instagram และอีเมลนี้

ขอบคุณที่ร่วมสร้างอนาคตของบากรักไปด้วยกัน
แล้วเจอกันในสนามฮีโร่!

ขอเป็นกำลังใจให้ทุกทีมครับ!!
ทีมงาน BangRak Hackathon 2025'''
}

raw_emails = '''
kn.41320@kanlayanee.ac.th
preamm2015@gmail.com
lilly22222550@gmail.com
pimchanok270750@gmail.com
lippakorn245@gmail.com
natthamon.than@dome.tu.ac.th
newf60057@gmail.com
phubase.phu@student.mahidol.edu
zernmcpe@gmail.com
petchppsb@gmail.com
monet.vmo@gmail.com
68011645@kmitl.ac.th
napasorn.tra@student.mahidol.edu
varisara.38490@gmail.com
rapeeratchen@gmail.com
barmy5431@gmail.com
pimchanokek6@gmail.com
achiraya.cna@gmail.com
ammyprom6@gmail.com
ndechrapepong@gmail.com
punrada160848@gmail.com
fungfha25@gmail.com
Ppumuai@gmail.com
keeratikotama@gmail.com
pimmada.seu@st.econ.tu.ac.th
Apilakjeentang@gmail.com
mtwopower550@gmail.com
narast.naen@bumail.net
kphanekew@gmail.com
p.puthiphat@gmail.com
chokthanwa121212@gmail.com
jirapatchaosuanjaroen.best@gmail.com
srimara07@gmail.com
engwararin007@gmail.com
std.nk39607@gmail.com
pannvitchapol@gmail.com
tentysgmt@gmail.com
kopter.chanatphol@gmail.com
kaygoodsure@gmail.com
Kanyarat.raw14@gmail.com
17537@nbr.ac.th
nararat1718@gmail.com
ketsarin1156@gmail.com
teaynyny@gmail.com
Nichanan34210@gmail.com
thunyalukthongchay@gmail.com
kkua0548@gmail.com
Oakphowit46@gmail.com
Oakphowit46@gmail.com
krittidetch.b@gmail.com
Chinawong_k@silpakorn.edu
Sakulploy30@gmail.com
6532087621@student.chula.ac.th
sakunthip.khu@gmail.com
kanokwanpomelo214@gmail.com
6834325123@student.chula.ac.th
proud.rada19@gmail.com
bunpan.kaopun@gmail.com
tarxlr32@gmail.com
raiwinsptk@gmail.com
salakit.ptrp@gmail.com
oazizter@gmail.com
sansarng.pra@gmail.com
Linsunisa1384@gmail.com
kavintraac@gmail.com
achirateawsirisup@gmail.com
Lapadrada.c@kkumail.com
noppasit560@gmail.com
napasrapeec@gmail.com
pan21468@gmail.com
Chamil162551@gmail.com
ittichetxd@gmail.com
beemchaocharoen@gmail.com
Punnamasonong24@gmail.com
worawaran.lo@ku.th
jasminrodyim@gmail.com
kaotomworasilp@gmail.com
67100160@kmitl.ac.th
pompormpt@gmail.com
cartoon1742@gmail.com
atiwitwcc@gmail.com
anutida.mai21@gmail.com
Chamil162551@gmail.com
Salwatee32284@gmail.com
2558sirikorn@gmail.com
sasitornthongjitti@gmail.com
Panuchaya21@gmail.com
Billgatecooky@gmail.com
warintron152521@gmail.com
kunchotha00@gmail.com
yanthichapongsangiam@gmail.com
phoengyai_p@silpakorn.edu
twrrnkhr@gmail.com
Cxchy2008@gmail.com
donghaeya86@gmail.com
nongchanya11451@gmail.com
natchapon887@gmail.com
p.pitchayaaaa@gmail.com
kruethaikp@gmail.com
pianoparinda@gmail.com
channarong.chokun@gmail.com
chompapopd@gmail.com
37577@montfort.ac.th
mawin025.tp@gmail.com
Pattarin7163@gmail.com
teverygood@gmail.com
poonpunkarunaboonsirisin@gmail.com
05949@pccm.ac.th
donghaeya86@gmail.com
aenasurada@gmail.com
Isaree2348@gmail.com
narakorn06478334428@gmail.com
wisanlaya5758@gmail.com
miwphudit@gmail.com
Peachydatty@gmail.com 
gitaneur@gmail.com
khumkhoon2553@gmail.com
Mickymonnn@gmail.com
paep.penner20@gmail.com
jakkritpho12@gmail.com
thanpisit2549@icloud.com
charudejs@gmail.com
kanokporn.n2546@gmail.com
ss51808@samsenwit.ac.th
chansuda2548@gmail.com
addeen.sk@gmail.com
jiratchot01@gmail.com
titaree1311@gmail.com
nannalintan@gmail.com
onvilasinee@gmail.com
warangkanavevie@gmail.com
Kingkondrie123@gmail.com
Patterinwza@gmail.com
6630121021@student.chula.ac.th
52762@hatyaiwit.ac.th
teppei1239@gmail.com
sedtawuttawan@gmail.com
daranpop.songsawas@gmail.com
santipabppch12345@gmail.com
Monn8036@gmail.com
phet12590@gmail.com
Possavee.pan@gmail.com
3224oonchira@gmail.com
bugattmark@gmail.com
'''

# Split, strip, and deduplicate
emails = set(e.strip() for e in raw_emails.splitlines() if e.strip())

sent_count = 0
for email in emails:
    email_data['to'] = email
    send_email(email_data)
    sent_count += 1
print(f"\nTotal emails sent: {sent_count}")
