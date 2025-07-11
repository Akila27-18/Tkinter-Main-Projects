# graph_utils.py
import matplotlib.pyplot as plt

def show_individual_result(data):
    labels = ["Subject 1", "Subject 2", "Subject 3"]
    scores = data[2:5]
    plt.bar(labels, scores, color="skyblue")
    plt.title(f"Results for {data[1]} ({data[0]})")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    plt.show()

def show_class_average(all_students):
    sub_totals = [0, 0, 0]
    count = len(all_students)
    if count == 0:
        return
    for s in all_students:
        sub_totals[0] += s[2]
        sub_totals[1] += s[3]
        sub_totals[2] += s[4]
    averages = [round(t / count, 2) for t in sub_totals]
    labels = ["Subject 1", "Subject 2", "Subject 3"]
    plt.bar(labels, averages, color="orange")
    plt.title("Class Average per Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.show()
