import json
from datetime import date, datetime, timedelta

def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_score(skill_hrs, academic_hrs, target=7.0):
    """Weighted productivity score (0–100%)."""
    if target <= 0:
        return 0.0
    weighted = skill_hrs * 0.6 + academic_hrs * 0.4
    score = (weighted / target) * 100
    return max(0.0, min(100.0, score))

def calculate_streak(logs, threshold=5.0):
    """Return current streak and best streak (consecutive days with total >= threshold)."""
    if not logs:
        return 0, 0

    # Set of dates that meet threshold
    streak_dates = set()
    for log in logs:
        total = log['skill_hrs'] + log['academic_hrs']
        if total >= threshold:
            streak_dates.add(log['date'])

    # Current streak (from today backwards)
    today = date.today()
    current_streak = 0
    check_date = today
    while check_date.isoformat() in streak_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    # Best streak ever
    dates_met = sorted(streak_dates)
    if not dates_met:
        return current_streak, 0

    best_streak = 1
    current = 1
    for i in range(1, len(dates_met)):
        prev = datetime.strptime(dates_met[i-1], "%Y-%m-%d").date()
        curr = datetime.strptime(dates_met[i], "%Y-%m-%d").date()
        if (curr - prev).days == 1:
            current += 1
            best_streak = max(best_streak, current)
        else:
            current = 1
    best_streak = max(best_streak, current)  # in case streak continues to today

    return current_streak, best_streak

def get_weekly_summary(logs, target=7.0):
    """Return last 7 days table data and stats."""
    today = date.today()
    start = today - timedelta(days=6)
    days_data = []
    total_hours = 0.0
    scores = []

    for i in range(7):
        day = start + timedelta(days=i)
        day_str = day.isoformat()
        entry = next((log for log in logs if log['date'] == day_str), None)
        if entry:
            s = entry['skill_hrs']
            a = entry['academic_hrs']
            total = s + a
            sc = calculate_score(s, a, target)
            days_data.append({
                "date": day_str,
                "skill_hrs": s,
                "academic_hrs": a,
                "total": total,
                "score": sc
            })
            total_hours += total
            scores.append(sc)
        else:
            days_data.append({
                "date": day_str,
                "skill_hrs": 0,
                "academic_hrs": 0,
                "total": 0,
                "score": 0
            })
            scores.append(0)

    avg_score = sum(scores) / len(scores) if scores else 0
    best_day = max(days_data, key=lambda x: x['score']) if days_data else None
    return {
        "start_date": start.isoformat(),
        "end_date": today.isoformat(),
        "days": days_data,
        "total_hours": total_hours,
        "avg_score": avg_score,
        "best_day": best_day if best_day and best_day['score'] > 0 else None
    }

def format_progress_bar(percentage, width=20):
    """ASCII progress bar like [=======   ]."""
    filled = int(percentage / 100 * width)
    bar = '[' + '=' * filled + ' ' * (width - filled) + ']'
    return bar

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')