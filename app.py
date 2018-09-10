from flask import Flask, render_template
app = Flask(__name__)

tasks = [
    {
        "title": "first large task",
        "size": "large",
        "today": True,
        "badge": "danger"
    },
    {
        "title": "first medium task",
        "size": "medium",
        "today": True,
        "badge": "warning"
    },
    {
        "title": "first small task",
        "size": "small",
        "today": True,
        "badge": "success"
    }
]   

@app.route("/")
def hello():
    return render_template('index.html', tasks=tasks)


app.run(debug=True)
