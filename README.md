# 🔥 Discipline Log – CLI Habit Tracker

> **"Discipline > Motivation" – now quantifiable.**

A pure Python command‑line productivity tracker that logs your daily skill and academic hours, calculates streaks, and shows you a weekly productivity score.  
No databases, no web frameworks – just raw discipline, measured daily.

---

## 🎯 Why This Project Exists

Motivation is fleeting. Discipline is a system.  
**Discipline Log** turns "being disciplined" into a number you can track.

- Log your deep‑work hours (skills + academics)
- See a weighted productivity score (0–100%)
- Track your current and best streak
- Review weekly performance at a glance

It was built by a student who believes discipline beats motivation – and wants a tool that proves it.

---

## 🧠 Features (v1.0 MVP)

| Feature               | Description |
|-----------------------|-------------|
| 📝 **Log today’s hours**  | Save skill hours, academic hours, and an optional note |
| 👀 **View today’s entry** | See what you’ve already logged for the day |
| 🔥 **Streak counter**     | Counts consecutive days with total hours ≥ 5 (adjustable) |
| 📊 **Productivity score** | Weighted formula: `(skill_hrs * 0.6 + academic_hrs * 0.4) / target * 100` |
| 📅 **Weekly summary**     | Last 7 days table, total hours, avg score, best day |
| 💾 **Data persistence**   | Saves to `data/logs.json` – no database required |
| 🧹 **Clean CLI menu**     | Interactive menu with input validation and ASCII progress bars |

---

## 🛠️ Tech Stack

- **Language:** Python 3.7+
- **Libraries:** Standard library only (`json`, `datetime`, `os`)
- **Storage:** JSON file

---

## 📂 Project Structure

```text
discipline_tracker/
├── tracker.py         # Main CLI application
├── data/
│   └── logs.json      # All your daily logs (auto‑created)
└── utils/
    └── helpers.py     # Logic: streak, score, weekly summary, progress bar
```

---

## 🚀 Getting Started

### 1. 📥 Clone the repository
```bash
git clone https://github.com/yourusername/discipline-tracker.git
cd discipline-tracker
```

### 2. 🐍 Check Python version
```bash
python --version   # Should be 3.7 or higher
```

### 3. 🏃 Run the tracker
```bash
python tracker.py
```
*On the first run, the app automatically creates the `data/` folder and an empty `logs.json`.*

---

## 📖 Usage

After running `python tracker.py`, you'll interact with a simple menu.

**Example Session:**
```text
Choice: 1
Skill hours (0-12): 3.5
Academic hours (0-12): 4.0
Note: DOM manipulation practice

✅ Logged for 2026-06-11
Daily Score: 83% [================    ]
```

---

## ⚙️ Customization

Inside `tracker.py`, you can modify constants to fit your goals:

| Variable | Default | Meaning |
|----------|---------|---------|
| `TARGET_HOURS` | `7.0` | Daily target for 100% productivity score |
| `STREAK_THRESHOLD` | `5.0` | Min total hours to count a day towards the streak |

---

## 📜 License

**MIT** – feel free to use, modify, and share. Just keep building discipline.

---

*Built by a student for students. Use it for 7 days straight. Prove the system works.*