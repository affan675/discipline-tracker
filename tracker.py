import os
import json
from datetime import date
from utils.helpers import (
    load_data,
    save_data,
    calculate_streak,
    calculate_score,
    get_weekly_summary,
    format_progress_bar,
    clear_screen
)

DATA_FILE = "data/logs.json"
TARGET_HOURS = 7.0        # daily target for 100% score
STREAK_THRESHOLD = 5.0    # min total hours to count a day toward streak

def main():
    # Make sure data folder and file exist
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

    while True:
        clear_screen()
        print("🔥 Discipline Log – Habit Tracker (v1.0)")
        print("-" * 38)
        print("1. 📝 Log today")
        print("2. 👀 View today")
        print("3. 🔥 Show streak")
        print("4. 📊 Weekly summary")
        print("5. 🚪 Exit")
        choice = input("\nChoice: ").strip()

        if choice == '1':
            add_log()
        elif choice == '2':
            view_today()
        elif choice == '3':
            show_streak()
        elif choice == '4':
            weekly_summary()
        elif choice == '5':
            print("\n🚀 Discipline > motivation. Keep building.")
            break
        else:
            input("Invalid option. Press Enter to continue...")

def add_log():
    clear_screen()
    print("📝 Log Today's Hours")
    print("-" * 18)
    today_str = date.today().isoformat()

    logs = load_data(DATA_FILE)
    existing = next((log for log in logs if log['date'] == today_str), None)

    if existing:
        print(f"Entry for {today_str} already exists:")
        print(f"  Skill hours: {existing['skill_hrs']}")
        print(f"  Academic hours: {existing['academic_hrs']}")
        print(f"  Note: {existing['note']}")
        overwrite = input("Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            input("Log unchanged. Press Enter to continue...")
            return
        else:
            logs = [log for log in logs if log['date'] != today_str]

    try:
        skill = float(input("Skill hours (0-12): "))
        if skill < 0 or skill > 12:
            print("Skill hours must be 0–12.")
            input("Press Enter..."); return
        acad = float(input("Academic hours (0-12): "))
        if acad < 0 or acad > 12:
            print("Academic hours must be 0–12.")
            input("Press Enter..."); return
    except ValueError:
        print("Invalid number.")
        input("Press Enter..."); return

    note = input("Note (optional): ").strip()
    entry = {
        "date": today_str,
        "skill_hrs": skill,
        "academic_hrs": acad,
        "note": note
    }
    logs.append(entry)
    save_data(DATA_FILE, logs)

    score = calculate_score(skill, acad, TARGET_HOURS)
    bar = format_progress_bar(score)
    print(f"\n✅ Logged for {today_str}")
    print(f"Daily Score: {score:.0f}% {bar}")
    input("Press Enter to continue...")

def view_today():
    clear_screen()
    print("📅 Today's Log")
    print("-" * 12)
    today_str = date.today().isoformat()
    logs = load_data(DATA_FILE)
    entry = next((log for log in logs if log['date'] == today_str), None)

    if entry:
        print(f"Date: {entry['date']}")
        print(f"Skill hours: {entry['skill_hrs']}")
        print(f"Academic hours: {entry['academic_hrs']}")
        print(f"Note: {entry['note']}")
        total = entry['skill_hrs'] + entry['academic_hrs']
        print(f"Total hours: {total:.1f}")
        score = calculate_score(entry['skill_hrs'], entry['academic_hrs'], TARGET_HOURS)
        bar = format_progress_bar(score)
        print(f"Productivity score: {score:.0f}% {bar}")
    else:
        print("No log for today yet. Go build discipline!")
    input("\nPress Enter to continue...")

def show_streak():
    clear_screen()
    print("🔥 Streak Info")
    print("-" * 12)
    logs = load_data(DATA_FILE)
    if not logs:
        print("No logs yet. Start logging.")
        input("Press Enter..."); return

    current, best = calculate_streak(logs, STREAK_THRESHOLD)
    print(f"🔥 Current streak: {current} days")
    print(f"💪 Best streak: {best} days")
    input("\nPress Enter to continue...")

def weekly_summary():
    clear_screen()
    print("📊 Weekly Summary")
    print("-" * 16)
    logs = load_data(DATA_FILE)
    summary = get_weekly_summary(logs, TARGET_HOURS)

    if not summary["days"]:
        print("No data in the last 7 days.")
        input("Press Enter..."); return

    print(f"Period: {summary['start_date']} to {summary['end_date']}\n")
    print(f"{'Date':<12} {'Skill':>6} {'Acad':>6} {'Total':>6} {'Score':>6}")
    print("-" * 44)

    for day in summary["days"]:
        d = day["date"]
        s = day["skill_hrs"]
        a = day["academic_hrs"]
        t = s + a
        sc = day["score"]
        bar = format_progress_bar(sc, width=10)
        print(f"{d:<12} {s:>6.1f} {a:>6.1f} {t:>6.1f} {sc:>5.0f}% {bar}")

    print("-" * 44)
    print(f"Total hours: {summary['total_hours']:.1f}")
    print(f"Avg productivity score: {summary['avg_score']:.0f}%")
    if summary["best_day"]:
        best = summary["best_day"]
        print(f"Best day: {best['date']} (score {best['score']:.0f}%)")
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()