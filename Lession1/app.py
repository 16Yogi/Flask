from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from datetime import datetime

app = Flask(__name__)

# database
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #if getting Track error
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str: 
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['GET','POST'])
def index():
    # return "<p>Hello, World!</p>"
    if request.method == 'POST':
        # print(request.form['title'])
        # print(request.form['desc'])
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title,desc=desc) 
        db.session.add(todo)
        db.session.commit()

    # todo = Todo(title="First todo",desc="start investing in stock market")
    # db.session.add(todo)
    # db.session.commit()
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template('index.html',allTodo=allTodo)


# @app.route('/show')
# def products():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return 'this is products page'


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()  
        todo.title = title  
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)



@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True,port=8000,host="")

