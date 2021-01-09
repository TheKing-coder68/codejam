from flask import Flask, url_for, render_template, redirect
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

schedule = [
    {
        'period':1,
        'time':'8:05-59'
    },
    {
        'period':2,
        'time':'8:05-59'
    },
    {
        'period':3,
        'time':'8:05-59'
    },
    {
        'period':4,
        'time':'8:05-59'
    },{
        'period':5,
        'time':'8:05-59'
    },
    {
        'period':6,
        'time':'8:05-59'
    },{
        'period':7,
        'time':'8:05-59'
    },
    {
        'period':8,
        'time':'8:05-59'
    },{
        'period':9,
        'time':'8:05-59'
    },
    {
        'period':10,
        'time':'8:05-59'
    },
]
class TodoItem(db.Model):
    def __init__(self, title, content):
        self.title = title
        self.content = content
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"Todo Item('{self.title}', '{self.content}')"
@app.route("/")
def home():
    return render_template('index.html', title='Home', header='Schedule', data=schedule)
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        list1 = TodoItem.query.all()
        list1 = list1[::-1]
        return render_template('todo.html', content=list1, title="Todo List", header='Todo List')
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        todo = TodoItem(title, description)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo', methods=['GET']))
@app.route("/todo/del/<id>")
def del_id(id):
    id = TodoItem.query.get(id)
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('todo'))
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port='8000')