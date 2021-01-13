from flask import Flask, url_for, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TodoItem(db.Model):
    def __init__(self, title, content, duedate):
        self.title = title
        self.duedate = duedate
        self.content = content
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    duedate = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.title} is due on {self.duedate}"
class Event(db.Model):
    def __init__(self, event_type, date, notes):
        self.event_type = event_type
        self.date = date
        self.notes = notes
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.event_type} {self.date} {self.notes}"
@app.errorhandler(404)
def error(e):
    return render_template('error.html'), 404
@app.errorhandler(405)
def error405(e):
    return render_template('error405.html'), 405
@app.route("/")
def home():
    data = TodoItem.query.all()
    data = data[::-1]
    return render_template('index.html', title='Home', header='Dashboard', date=date.today(), due=data)
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        list1 = TodoItem.query.all()
        list1 = list1[::-1]
        if len(list1) == 0:
            content = [{'title':'Nothing to do! Click the plus to add tasks', 'content':'All your tasks are done', 'duedate':'Nothing is due'}]
        else:
            content = list1
        return render_template('todo.html', content=content, title="Todo List", header='Todo List')
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        ddate = request.form.get('due_date')
        todo = TodoItem(title, description, ddate)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo', methods=['GET']))
@app.route("/todo/del/<id>")
def del_id(id):
    id = TodoItem.query.get(id)
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('todo'))
@app.route("/dates-and-times", methods=['GET', 'POST'])
def dat():
    if request.method == 'GET':
        events = Event.query.all()
        events = events[::-1]
        return render_template('dat.html', header="Important Dates and Times", title="Important dates", dates=events)
    else:
        e_type = request.form.get('type')
        date = request.form.get('date')
        notes = request.form.get('notes')
        event = Event(e_type, date, notes)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('dat', methods=['GET']))
@app.route("/update/<id>")
def update(id):
    session['id'] = id
    todo = TodoItem.query.get(id)
    TTT = todo.title
    DESC = todo.content
    DDATE = todo.duedate
    return render_template('update.html', TTT=TTT, DESC=DESC, DDATE=DDATE)
@app.route("/update-dat/<id>")
def update_dat(id):
    session['id'] = id
    event = Event.query.get(id)
    etype = event.event_type
    desc = event.notes
    date = event.date
    return render_template('update_dat.html', type=etype, desc=desc, date=date)
@app.route("/save-updated", methods=['POST'])
def save_updated():
    id = session['id']
    item_to_be_updated = TodoItem.query.get(id)
    title = request.form.get('title')
    content = request.form.get('description')
    ddate = request.form.get('due_date')
    item_to_be_updated.title = title
    item_to_be_updated.content = content
    item_to_be_updated.duedate = ddate
    db.session.commit()
    session.pop('id', None)
    return redirect(url_for('todo'))
@app.route("/save-updated-dat", methods=['POST'])
def save_updated_dat():
    id = session['id']
    item_to_be_updated = Event.query.get(id)
    event_type = request.form.get('title')
    date = request.form.get('description')
    notes = request.form.get('due_date')
    item_to_be_updated.event_type = event_type
    item_to_be_updated.date = date
    item_to_be_updated.notes = notes
    db.session.commit()
    session.pop('id', None)
    return redirect(url_for('dat'))
@app.route("/del/event/<id>")
def del_event(id):
    id = Event.query.get(id)
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('dat'))
if __name__ == "__main__":
    db.create_all() # creates all the tables in the db
    app.run(debug=True, port='8000')
