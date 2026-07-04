"""
Test ma'lumotlari yuklash skripti.
Ishlatish:  python seed.py
Server http://localhost:8005 da ishlayotgan bo'lishi kerak.
"""
import requests, random, sys

BASE = "http://localhost:8000/api/v1"

FANLAR = [
    "Matematika", "Fizika", "Kimyo", "Biologiya", "Tarix",
    "Informatika", "Ingliz tili", "Rus tili", "Adabiyot", "Geografiya",
    "Chizmachilik", "Iqtisodiyot", "Falsafa", "Huquq", "Sotsiologiya",
    "Psixologiya", "Sport", "Musiqa", "Tasviriy san'at", "Texnologiya",
]

FAMILIYALAR = [
    "Aliyev", "Karimov", "Rahimov", "Umarov", "Xasanov",
    "Toshmatov", "Yusupov", "Nazarov", "Qodirov", "Mirzayev",
    "Sultonov", "Ergashev", "Holiqov", "Baxtiyorov", "Nurmatov",
    "Ismoilov", "Sobirov", "Abdullayev", "Jumayev", "Haydarov",
]
ISMLAR = [
    "Bobur", "Jasur", "Sherzod", "Dilnoza", "Malika",
    "Kamola", "Sanjar", "Zafar", "Nilufar", "Munira",
    "Ulugbek", "Farrux", "Mohira", "Sarvinoz", "Doniyor",
    "Shohruh", "Gulnora", "Barno", "Tohir", "Nodir",
]

XONA_TURLARI = ["dars", "laboratoriya", "majlis_zali", "sport_zali"]
YUNALISHLAR  = ["Informatika", "Iqtisodiyot", "Huquq", "Muhandislik",
                "Tibbiyot", "Pedagogika", "San'at", "Tarix"]

# Standart 7 dars soati
VAQTLAR = [
    ("08:00", "09:30"),
    ("09:45", "11:15"),
    ("11:30", "13:00"),
    ("14:00", "15:30"),
    ("15:45", "17:15"),
    ("17:30", "19:00"),
    ("19:15", "20:45"),
]

# ─────────────────────────────────────────

def post(endpoint, body):
    r = requests.post(f"{BASE}{endpoint}", json=body, timeout=10)
    if r.status_code not in (200, 201):
        print(f"  ❌ {endpoint} | {r.status_code} | {r.text[:120]}")
        return None
    return r.json()

def get(endpoint):
    r = requests.get(f"{BASE}{endpoint}", timeout=10)
    if not r.ok:
        return []
    return r.json()

# ─────────────────────────────────────────
print("🚀 Seed boshlandi...\n")

# 1. O'qituvchilar (20 ta)
print("👨‍🏫 20 ta o'qituvchi qo'shilmoqda...")
teacher_ids = []
for i in range(20):
    t = post("/teachers/", {
        "full_name": f"{FAMILIYALAR[i]} {ISMLAR[i]}",
        "subject":   FANLAR[i],
        "email":     f"{FAMILIYALAR[i].lower()}{i+1}@school.uz",
    })
    if t:
        teacher_ids.append(t["id"])
        print(f"  ✅ {t['full_name']} — {t['subject']}")

# 2. Xonalar (14 ta)
print("\n🏛️ 14 ta xona qo'shilmoqda...")
room_ids = []
for i in range(1, 11):
    r = post("/rooms/", {
        "name":      f"{100 + i}-xona",
        "capacity":  random.choice([25, 30, 35, 40]),
        "room_type": "dars",
    })
    if r:
        room_ids.append(r["id"])
        print(f"  ✅ {r['name']}")

for idx, rtype in enumerate(["Fizika lab", "Kimyo lab", "Sport zali", "Majlis zali"]):
    rtype_key = ["laboratoriya", "laboratoriya", "sport_zali", "majlis_zali"][idx]
    r = post("/rooms/", {
        "name":      rtype,
        "capacity":  random.choice([20, 30, 50, 100]),
        "room_type": rtype_key,
    })
    if r:
        room_ids.append(r["id"])
        print(f"  ✅ {r['name']}")

# 3. Guruhlar (10 ta)
print("\n👥 10 ta guruh qo'shilmoqda...")
group_ids = []
for i in range(10):
    yunalish = YUNALISHLAR[i % len(YUNALISHLAR)]
    kurs = (i % 4) + 1
    g = post("/groups/", {
        "name":           f"{yunalish[:3].upper()}-{kurs}{i+1:02d}",
        "student_count":  random.randint(18, 35),
        "course_year":    kurs,
        "specialization": yunalish,
    })
    if g:
        group_ids.append(g["id"])
        print(f"  ✅ {g['name']} ({yunalish}, {kurs}-kurs)")

if not teacher_ids or not room_ids or not group_ids:
    print("\n❌ ID lar yetarli emas, darslar qo'shilmadi.")
    sys.exit(1)

# 4. Jadval — har bir kun (1-7) uchun
print("\n📅 Jadval qo'shilmoqda (har 7 kun × 7 soat)...")
KUNLAR = {1:"Dushanba", 2:"Seshanba", 3:"Chorshanba",
          4:"Payshanba", 5:"Juma", 6:"Shanba", 7:"Yakshanba"}

tt_count = 0
# Qaysi (teacher, room, group) juftliklarni qo'shamiz
# Har kun uchun 4-7 ta dars, ovarlap bo'lmasin
for day in range(1, 7):
    # Har kun uchun random 5 ta slot tanlash
    slots = random.sample(VAQTLAR, 5)
    used_rooms    = set()
    used_teachers = set()
    used_groups   = set()

    for start, end in slots:
        # Conflict bo'lmasin — band bo'lmaganlarni top
        av_teachers = [tid for tid in teacher_ids if tid not in used_teachers]
        av_rooms    = [rid for rid in room_ids    if rid not in used_rooms]
        av_groups   = [gid for gid in group_ids   if gid not in used_groups]

        if not av_teachers or not av_rooms or not av_groups:
            break

        tid = random.choice(av_teachers)
        rid = random.choice(av_rooms)
        gid = random.choice(av_groups)

        # Fan o'qituvchining fani
        teacher_list = get("/teachers/")
        tname_map = {t["id"]: t["subject"] for t in teacher_list}
        subject = tname_map.get(tid, random.choice(FANLAR))

        entry = post("/timetable/", {
            "teacher_id":  tid,
            "room_id":     rid,
            "group_id":    gid,
            "day_of_week": day,
            "start_time":  start + ":00",
            "end_time":    end   + ":00",
            "subject":     subject,
        })
        if entry:
            used_teachers.add(tid)
            used_rooms.add(rid)
            used_groups.add(gid)
            tt_count += 1
            print(f"  ✅ {KUNLAR[day]:10s} {start}-{end}  {subject}")

print(f"\n🎉 Tayyor! Jami {tt_count} ta dars qo'shildi.")
print(f"   O'qituvchilar : {len(teacher_ids)}")
print(f"   Xonalar       : {len(room_ids)}")
print(f"   Guruhlar      : {len(group_ids)}")
