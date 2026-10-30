# Python List
print("Python")
a = [10, 20, 30, 40]
print(f"{a * 2}\n")

print("NumPy")
import numpy as np

a = np.array([10, 20, 30, 40])
print(a * 2)

arr = np.array([10, 20, 30, 40])
print(f"Sum: {np.sum(arr)}")  # Total Calculation
print(f"Mean: {np.mean(arr)}")  # Find Average
print(f"Max: {np.max(arr)}")  # Maximum Value
print(f"Min: {np.min(arr)}")  # Minimum Value
print(f"Standard Deviation: {np.std(arr)}")  # Standard deviation calculate


# Real Life Example
print('\nExample')
import numpy as np

marks = np.array([80, 75, 90, 85, 70])
average = np.mean(marks)
print(f"Average Marks: {average}")
