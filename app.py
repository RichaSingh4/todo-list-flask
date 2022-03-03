from turtle import title
from flask import Flask, redirect, render_template, request, redirect #render_template is used to generate output from a template file based on the Jinja2 engine that is found in the application's templates folder.
from flask_sqlalchemy import SQLAlchemy #import sqlalchemy or database
from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint

app = Flask(__name__) #initializing the app


#initilazing the sqlalchemy or database
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):

    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    desc=db.Column(db.String,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str: #__repr__ is a special method used to represent a class's objects as a string. __repr__ is called by the repr() built-in function. You can define your own string representation of your class objects using the __repr__ method. Special methods are a set of predefined methods used to enrich your classes
        return f"{self.sno} - {self.title}"



@app.route("/",methods=['GET','POST']) #The route() decorator in Flask is used to bind an URL to a function
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)

    return render_template('index.html',allTodo=allTodo)
    # return "<p>Hello, World!</p>"

@app.route('/show')
def product():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is product page'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first() 
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    

if __name__=="__main__":
    app.run(debug=True) 