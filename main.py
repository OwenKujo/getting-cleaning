from pythainlp.tokenize import word_tokenize
from meanings_data import (
    meanings_money, meanings_work, meanings_animal, meanings_activities,
    meanings_good_bad, meanigs_right_left, meanings_general, meanings_love
)
def Dream_Prediction(time_str, topic):
    try:
        hour = int(time_str.split()[1].split(":")[0])
    except Exception:
        return "รูปแบบเวลาความฝันไม่ถูกต้อง\nไม่สามารถทำนายได้"

    if 7 < hour < 19:
        time_msg = "ฝันกลางวัน: ไม่สามารถเชื่อถือได้\n➡ อาจเกิดจากจินตนาการ"
    elif 19 <= hour < 23:
        time_msg = "ฝันหัวค่ำ: ลางบอกเหตุถึงบุคคลทางไกล"
    elif hour >= 23 or hour < 3:
        time_msg = "ฝันยามดึก: เรื่องจริงเกี่ยวกับครอบครัว"
    elif 3 <= hour < 7:
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


# รับ input จากผู้ใช้
user_text = input("กรุณากรอกประโยคความฝัน: ")
user_time = input("กรุณากรอกเวลาความฝัน (รูปแบบ YYYY-MM-DD HH:MM:SS): ")
user_topic = input("เลือกหัวข้อ (1=การเงิน, 2=ความรัก, 3=การงาน, 4=สัตว์, 5=เหตุการณ์ทั่วไป, 6=เรื่องดี/ร้าย, 7=ขวาร้ายซ้ายดี, 8=ทั่วไป): ")

# แสดงผล
print("\n🔮 ผลการทำนายฝัน 🔮")
print(Dream_Prediction(user_time, user_topic))
print(find_dream_meaning(user_text, user_topic))
