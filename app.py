import requests
import time
import string
import random

# إعدادات الصيد
CHECK_LIMIT = 50  # عدد اليوزرات التي سيفحصها في كل مرة يعمل فيها السكربت
CHAR_COUNT = 4    # طول اليوزر (4 حروف)

def generate_username(length):
    # توليد يوزر عشوائي من حروف وأرقام
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def check_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 404:
        return True  # اليوزر متاح!
    return False     # اليوزر محجوز

def start_hunting():
    print(f"🚀 بدء عملية البحث عن يوزرات متاحة بطول {CHAR_COUNT} حروف...")
    found_users = []
    
    for _ in range(CHECK_LIMIT):
        user = generate_username(CHAR_COUNT)
        if check_github_user(user):
            print(f"✅ متاح: {user}")
            found_users.append(user)
        else:
            print(f"❌ محجوز: {user}")
        time.sleep(0.5)  # لتجنب الحظر من API جيت هاب
    
    if found_users:
        print("\n🏆 القائمة المكتشفة:")
        for u in found_users:
            with open("available_users.txt", "a") as f:
                f.write(u + "\n")
            print(f"- {u}")

if __name__ == "__main__":
    start_hunting()
