import datetime
from database import cursor, conn
from config import DAILY_LIMIT

user_limits = {}

def is_premium(user_id):
    cursor.execute("SELECT premium_until FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if not row or not row[0]:
        return False
    return datetime.datetime.fromisoformat(row[0]) > datetime.datetime.now()

def check_limit(user_id):
    today = datetime.date.today()

    if user_id not in user_limits:
        user_limits[user_id] = {"date": today, "count": 0}

    if user_limits[user_id]["date"] != today:
        user_limits[user_id] = {"date": today, "count": 0}

    if user_limits[user_id]["count"] >= DAILY_LIMIT:
        return False

    user_limits[user_id]["count"] += 1
    return True

def give_premium(user_id, days=30):
    until = (datetime.datetime.now() + datetime.timedelta(days=days)).isoformat()
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, premium_until) VALUES (?, ?)",
        (user_id, until)
    )
    conn.commit()
