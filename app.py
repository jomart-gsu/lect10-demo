import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://gtwyyadzwzgipy:d61efc665fdf4f76ecd0ce29e19b3559a3a06bd54867918688924bd0e89fd301@ec2-34-228-154-153.compute-1.amazonaws.com:5432/dq9ibvge361nh"
# suppresses a warning - not strictly needed
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# define some Models!

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    due_date = db.Column(db.String(80))

    def __repr__(self):
        return f"<Todo {self.title}"

db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    todos = Todo.query.all()
    titles = []
    due_dates = []
    for todo in todos:
        titles.append(todo.title)
        due_dates.append(todo.due_date)
    
    if flask.request.method == "POST":
        title = flask.request.form.get('title')
        due_date = flask.request.form.get('due_date')
        todo = Todo(title=title, due_date=due_date)
        db.session.add(todo)
        db.session.commit()
        titles.append(title)
        due_dates.append(due_date)
        return flask.jsonify({"response": "Saved a new TODO"})
    
    return flask.render_template(
        "index.html",
        length=len(titles),
        titles=titles,
        due_dates=due_dates
    )


app.run(debug=True)


