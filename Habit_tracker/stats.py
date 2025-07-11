import matplotlib.pyplot as plt
from database import get_habits, get_log
from datetime import date, timedelta

def show_stats():
    habits = get_habits()
    today = date.today()
    labels = []
    streaks = []

    for habit_id, name in habits:
        logs = get_log(habit_id)
        dates = set([d for d, done in logs if done])
        current_streak = 0
        longest = 0

        for i in range(365):
            d = today - timedelta(days=i)
            if d.isoformat() in dates:
                current_streak += 1
                longest = max(longest, current_streak)
            else:
                if i == 0:
                    continue  # today not done doesn't break streak
                current_streak = 0

        labels.append(name)
        streaks.append(longest)

    plt.bar(labels, streaks, color="skyblue")
    plt.title("Longest Streaks")
    plt.ylabel("Days")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
