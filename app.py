from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

with open('save.json') as input_file:
    tasks = json.load(input_file)

# tasks = [
#     {
#         "id": 0,
#         "title": "first large task",
#         "size": "large",
#         "today": True,
#         "badge": "danger",
#         "text": "hmm",
#         "archived": False
#     },
#     {
#         "id": 1,
#         "title": "first medium task",
#         "size": "medium",
#         "today": True,
#         "badge": "warning",
#         "text": "hmm",
#         "archived": False
#     },
#     {
#         "id": 2,
#         "title": "first small task",
#         "size": "small",
#         "today": True,
#         "badge": "success",
#         "text": "hmm",
#         "archived": False
#     }
# ]

badges = {
    "small": "success",
    "medium": "warning",
    "large": "danger"
}


def get_tasks():
    output = []
    for task in tasks:
        if not task['archived']:
            output.append(task)
    return output

def save_task_change():
    with open('save.json', 'w') as output_file:
        json.dump(tasks, output_file)

def new_task(title, text, size):
    global tasks
    tasks.append({
        "title": title,
        "text": text,
        "size": size.lower(),
        "badge": badges[size.lower()],
        "id": len(tasks),
        "today": False,
        "archived": False
    })



@app.route("/")
def root():
    task_sizes = {}
    for task in tasks:
        if not task['today'] and not task['archived']:
            if task['size'] not in task_sizes:
                task_sizes[task['size']] = 0
            task_sizes[task['size']] += 1
    return render_template('index.html', tasks=get_tasks(), task_sizes=task_sizes)

@app.route("/post", methods=["POST"])
def post():
    # request.method == "POST"
    new_task(request.form['title'], request.form['text'], request.form['size'])
    save_task_change()
    return redirect(url_for('root'))

@app.route("/tasks/<id>/archive")
def delete_task(id):
    global tasks
    tasks[int(id)]['archived'] = True
    save_task_change()
    return redirect(url_for('root'))

@app.route("/tasks/<id>/nottoday")
def nottoday_task(id):
    global tasks
    tasks[int(id)]['today'] = False
    save_task_change()
    return redirect(url_for('root'))

@app.route("/tasks/<id>/today")
def today_task(id):
    global tasks
    tasks[int(id)]['today'] = True
    save_task_change()
    return redirect(url_for('root'))

app.run(debug=True)
