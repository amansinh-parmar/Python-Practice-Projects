# Calculate the Student Marks and Find who got highest, lowest marks and who is Pass and Fail.

import numpy as np

students = np.array(["Jack", "Tom", "Julia", "Rolex", "Zane"])

# Rows = Students
# Columns = Subjects

marks = np.array(
    [
        [85, 90, 78, 88, 92],
        [70, 65, 80, 75, 72],
        [45, 55, 60, 50, 48],
        [30, 40, 35, 45, 38],
        [95, 92, 96, 89, 98],
    ]
)

print(marks)
# Total Marks
total_marks = np.sum(marks, axis=1)
print(f"Total Marks: {total_marks}")

# Average Marks
average = np.mean(marks)
print(f"Average Marks: {average}")

# Find the Topper
topper_index = np.argmax(total_marks)
print(f"Topper: {students[topper_index]}")
print(f"Total Marks: {total_marks[topper_index]}")

# Highest Mark
print(f"Highest Marks: {np.max(marks)}")
print(f"Lowest Marks: {np.min(marks)}\n")


# Identify Pass and Fail Students
result = np.all(marks >= 35, axis=1)

for i in range(len(students)):
    if result[i]:
        print(students[i], "Pass\n")
    else:
        print(students[i], "Fail\n")
