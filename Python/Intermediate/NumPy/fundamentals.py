import numpy as np

list1 = [1, 2, 3, 4, 5]
# print(list1)
# print(list[0])

list2 = ["Jack Reacher", 28, list1, True]

# print(list2)


# NumPy = Numeric Python
# ndarray = n-diamensional array
print("NumPy Arrays")
np1 = np.array([0, 1, 2, 3, 4, 5])
print(np1)
print(f"{np1.shape}\n")

# Range
print("Range")
np2 = np.arange(7)
print(f"{np2}\n")

# Step
print("Step")
np3 = np.arange(0, 10, 2)
print(f"{np3}\n")

# Zeros
print("Zeros")
np4 = np.zeros(5)
print(f"{np4}\n")

# Multidimensional zeros
print("Multidimensional Zeros")
np5 = np.zeros((2, 10))
print(f"{np5}\n")

# Full
print("Full")
np6 = np.full((10), 7)
print(f"{np6}\n")

# Multidimensional Full
print("Multidimensional Full")
np7 = np.full((2, 10), 7)
print(f"{np7}\n")

# Convert Python lists to np
print("Convert Python lists to NumPy")
py_list = [1, 2, 3, 4]
np8 = np.array(py_list)
print(f"{np8}\n")


np9 = np.array(list2, dtype=object)
print(f"{np9}\n")
