from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.deadline).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    assigned_to = request.form['assigned_to']
    deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
    priority = request.form['priority']

    new_task = Task(title=title, description=description, assigned_to=assigned_to,
                    deadline=deadline, priority=priority)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    task.title = request.form['title']
    task.description = request.form['description']
    task.assigned_to = request.form['assigned_to']
    task.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
    task.priority = request.form['priority']
    task.completed = 'completed' in request.form
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

print("Instance path:", app.instance_path)
print("Resolved DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
