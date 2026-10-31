import tkinter as tk
from tkinter import ttk, messagebox

# Student Record Searching and Sorting System
# Subject: Design and Analysis of Algorithms (DAA)

students = [
    {"id": 103, "name": "Aman", "marks": 78},
    {"id": 101, "name": "Rahul", "marks": 92},
    {"id": 105, "name": "Priya", "marks": 85},
    {"id": 102, "name": "Neha", "marks": 67},
    {"id": 104, "name": "Karan", "marks": 88}
]


# ---------- SEARCHING ALGORITHMS ----------

def linear_search(records, query):
    query = query.strip().lower()
    for student in records:
        if (str(student["id"]) == query
                or student["name"].lower() == query):
            return student
    return None


def binary_search(records, student_id):
    # Records must be sorted by ID.
    ordered = sorted(records, key=lambda s: s["id"])
    low, high = 0, len(ordered) - 1

    while low <= high:
        mid = (low + high) // 2
        if ordered[mid]["id"] == student_id:
            return ordered[mid]
        elif ordered[mid]["id"] < student_id:
            low = mid + 1
        else:
            high = mid - 1
    return None


# ---------- SORTING ALGORITHMS ----------

def bubble_sort(records, descending=False):
    result = records.copy()
    n = len(result)

    for i in range(n - 1):
        for j in range(n - i - 1):
            a = result[j]["marks"]
            b = result[j + 1]["marks"]

            if ((a > b and not descending)
                    or (a < b and descending)):
                result[j], result[j + 1] = (
                    result[j + 1], result[j]
                )
    return result


def merge_sort(records):
    if len(records) <= 1:
        return records.copy()

    mid = len(records) // 2
    left = merge_sort(records[:mid])
    right = merge_sort(records[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["name"].lower() <= right[j]["name"].lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- GUI FUNCTIONS ----------

def display_records(records=None):
    if records is None:
        records = students

    for item in table.get_children():
        table.delete(item)

    for s in records:
        table.insert(
            "", "end",
            values=(s["id"], s["name"], f"{s['marks']:.2f}")
        )

    average = (
        sum(s["marks"] for s in students) / len(students)
        if students else 0
    )
    count_label.config(text=f"Total Students: {len(students)}")
    average_label.config(text=f"Average Marks: {average:.2f}")


def search_student():
    query = search_entry.get().strip()

    if not query:
        messagebox.showwarning(
            "Input Required", "Enter a student ID or name."
        )
        return

    if query.isdigit():
        result = binary_search(students, int(query))
        method = "Binary Search"
    else:
        result = linear_search(students, query)
        method = "Linear Search"

    if result:
        display_records([result])
        status_label.config(text=f"{method}: Student found")
    else:
        display_records([])
        status_label.config(text="Student record not found")


def reset_records():
    search_entry.delete(0, tk.END)
    display_records()
    status_label.config(text="Showing all student records")


def add_student():
    try:
        sid = int(id_entry.get().strip())
        name = name_entry.get().strip()
        marks = float(marks_entry.get().strip())

        if any(s["id"] == sid for s in students):
            messagebox.showerror(
                "Duplicate ID", "This student ID already exists."
            )
            return

        if not name:
            messagebox.showerror(
                "Invalid Name", "Enter a student name."
            )
            return

        if not 0 <= marks <= 100:
            messagebox.showerror(
                "Invalid Marks", "Marks must be between 0 and 100."
            )
            return

        students.append({
            "id": sid,
            "name": name,
            "marks": marks
        })

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

        display_records()
        status_label.config(text="Student added successfully")

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "ID must be an integer and marks must be numeric."
        )


def sort_marks_ascending():
    display_records(bubble_sort(students))
    status_label.config(text="Bubble Sort: Marks ascending")


def sort_marks_descending():
    display_records(bubble_sort(students, descending=True))
    status_label.config(text="Bubble Sort: Marks descending")


def sort_names():
    display_records(merge_sort(students))
    status_label.config(text="Merge Sort: Names A to Z")


def sort_ids():
    display_records(sorted(students, key=lambda s: s["id"]))
    status_label.config(text="Student IDs sorted ascending")


# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Student Record Searching and Sorting System")
root.geometry("900x650")
root.minsize(760, 560)
root.configure(bg="#F1F5F9")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    rowheight=30,
    font=("Arial", 11),
    background="white",
    fieldbackground="white"
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold"),
    background="#DCE6F1"
)

header = tk.Frame(root, bg="#17365D", pady=16)
header.pack(fill="x")

tk.Label(
    header,
    text="STUDENT RECORD MANAGEMENT SYSTEM",
    font=("Arial", 19, "bold"),
    bg="#17365D",
    fg="white"
).pack()

tk.Label(
    header,
    text="DAA Mini Project | Python GUI",
    font=("Arial", 10),
    bg="#17365D",
    fg="white"
).pack(pady=(5, 0))

main = tk.Frame(root, bg="#F1F5F9", padx=18, pady=12)
main.pack(fill="both", expand=True)

# Search section
search_frame = tk.LabelFrame(
    main, text="Search Student", bg="#F1F5F9",
    padx=10, pady=10, font=("Arial", 10, "bold")
)
search_frame.pack(fill="x", pady=(0, 10))

search_entry = ttk.Entry(search_frame, font=("Arial", 11))
search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
search_entry.bind("<Return>", lambda event: search_student())

tk.Button(
    search_frame, text="Search",
    command=search_student, bg="#2563EB", fg="white",
    padx=12
).pack(side="left", padx=3)

tk.Button(
    search_frame, text="Show All",
    command=reset_records, padx=10
).pack(side="left", padx=3)

# Table
table_frame = tk.Frame(main, bg="#F1F5F9")
table_frame.pack(fill="both", expand=True)

columns = ("id", "name", "marks")
table = ttk.Treeview(
    table_frame, columns=columns, show="headings",
    height=8
)

table.heading("id", text="Student ID")
table.heading("name", text="Student Name")
table.heading("marks", text="Marks")

table.column("id", width=150, anchor="center")
table.column("name", width=300, anchor="center")
table.column("marks", width=150, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=table.yview
)
table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Sorting buttons
sort_frame = tk.LabelFrame(
    main, text="Sorting Algorithms", bg="#F1F5F9",
    padx=8, pady=8, font=("Arial", 10, "bold")
)
sort_frame.pack(fill="x", pady=10)

tk.Button(
    sort_frame, text="Marks: Low to High",
    command=sort_marks_ascending, bg="#0F766E", fg="white"
).pack(side="left", padx=4, pady=3)

tk.Button(
    sort_frame, text="Marks: High to Low",
    command=sort_marks_descending, bg="#0F766E", fg="white"
).pack(side="left", padx=4, pady=3)

tk.Button(
    sort_frame, text="Names: A to Z",
    command=sort_names, bg="#6D28D9", fg="white"
).pack(side="left", padx=4, pady=3)

tk.Button(
    sort_frame, text="Sort by ID",
    command=sort_ids
).pack(side="left", padx=4, pady=3)

# Add student section
add_frame = tk.LabelFrame(
    main, text="Add New Student", bg="#F1F5F9",
    padx=8, pady=8, font=("Arial", 10, "bold")
)
add_frame.pack(fill="x", pady=(0, 8))

tk.Label(add_frame, text="ID", bg="#F1F5F9").grid(
    row=0, column=0, padx=4
)
id_entry = ttk.Entry(add_frame, width=12)
id_entry.grid(row=0, column=1, padx=4)

tk.Label(add_frame, text="Name", bg="#F1F5F9").grid(
    row=0, column=2, padx=4
)
name_entry = ttk.Entry(add_frame, width=18)
name_entry.grid(row=0, column=3, padx=4)

tk.Label(add_frame, text="Marks", bg="#F1F5F9").grid(
    row=0, column=4, padx=4
)
marks_entry = ttk.Entry(add_frame, width=10)
marks_entry.grid(row=0, column=5, padx=4)

tk.Button(
    add_frame, text="Add Student",
    command=add_student, bg="#2563EB", fg="white"
).grid(row=0, column=6, padx=8)

# Summary and status
summary = tk.Frame(main, bg="#F1F5F9")
summary.pack(fill="x", pady=(2, 0))

count_label = tk.Label(
    summary, text="", bg="#F1F5F9",
    font=("Arial", 11, "bold")
)
count_label.pack(side="left")

average_label = tk.Label(
    summary, text="", bg="#F1F5F9",
    font=("Arial", 11, "bold")
)
average_label.pack(side="right")

status_label = tk.Label(
    root, text="Ready", anchor="w",
    bg="#DCE6F1", padx=12, pady=6
)
status_label.pack(fill="x", side="bottom")

display_records()
root.mainloop()

