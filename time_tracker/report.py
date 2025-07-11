import matplotlib.pyplot as plt
from database import get_tasks_by_date, get_weekly_summary
from datetime import date

def show_pie_chart():
    tasks = get_tasks_by_date(date.today().isoformat())
    labels = [row[0] for row in tasks]
    durations = [row[1] for row in tasks]

    if not durations:
        print("No tasks to display.")
        return

    plt.pie(durations, labels=labels, autopct='%1.1f%%')
    plt.title("Time Spent Per Task Today")
    plt.show()

def show_weekly_summary():
    data = get_weekly_summary()
    tasks = [x[0] for x in data]
    durations = [x[1]/60 for x in data]  # convert to minutes

    plt.bar(tasks, durations, color='skyblue')
    plt.ylabel("Time (min)")
    plt.title("Weekly Time Summary")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
