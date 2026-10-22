import json

# ==> Use Write to create and write new data
roadmap = {
    "Project": "Python Learning Roadmap",
    "task": [
        {
            "time": "1:00 Hr",
            "task": "CSV",
            "days": 1,
            "description": "Learn CSV file handling",
        },
        {
            "time": "1:00 Hr",
            "task": "JSON",
            "days": 1,
            "description": "Learn JSON file handling",
        },
    ],
}

with open("roadmap.json", "w") as file:
    # writes Python data into a JSON file
    json.dump(roadmap, file, indent=4)      # formats the file to make it readable

print("Roadmap.json Saved Successfully..")

# ==> Use Append to add new data
new_task = {
    "time": "1:00 Hr",
    "task": "NumPy",
    "days": 2,
    "description": "Learn numerical computing",
}

# Read existing data
with open("roadmap.json", "r") as file:
    roadmap = json.load(file)

# Add the new task
roadmap["task"].append(new_task)

# Save the updated data
with open("roadmap.json", "w") as file:
    json.dump(roadmap, file, indent=4)

print("New task added successfully..")


# ==> Use Read to read the data
with open('roadmap.json', 'r') as file:
    roadmap = json.load(file)

print('Project: ', roadmap['Project'])

for task in roadmap['task']:
    print('Task:', task['task'])
    print('Days:', task['days'])
    print('Description:', task['description'])
    print('Time:', task['time'])
    print('-' * 30)

# ==> Use 'r' and 'w' to Delete the data
with open("roadmap.json", "r") as file:
    roadmap = json.load(file)

roadmap["task"] = [task for task in roadmap["task"] if task["task"] != "CSV"]

with open("roadmap.json", "w") as file:
    json.dump(roadmap, file, indent=4)

print("Task Deleted Successfully..")
