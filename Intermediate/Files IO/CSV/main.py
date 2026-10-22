import csv

# ==> Use Write to write New Data
# Data to store in CSV file
header = ["Time", "Task", "Days", "Decription"]

roadmap = [
    ["1:00 Hr", "CSV", "1", "Project"],
    ["1:00 Hr", "JSON", "1", "Project"],
    ["1:00 Hr", "NumPy", "2", "Project"],
    ["1:00 Hr", "Pandas", "2", "Project"],
]

with open("roadmap.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(header)
    writer.writerows(roadmap)

print("Roadmap.csv file created successfully..")

# ==> Use Append to Add New Data
new_tasks = [
    ["1:00 Hr", "Metplotlib", 2, "Data Visualization"],
    ["1:00 Hr", "Seaborn", 2, "Data Visualization"],
]

with open("roadmap.csv", "a", newline="") as file:
    writer = csv.writer(file)

    writer.writerows(new_tasks)

print("New Data Added Successfully..")

# ==> Use Reader to read the Data
with open("roadmap.csv", "r", newline="") as file:
    reader = csv.reader(file)

    next(reader)  # Skip the header and get the data
    for row in reader:
        print(row)
