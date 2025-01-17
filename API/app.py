from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reg.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database Model
class regi(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"


# Routes
@app.route("/")
def index():
    return render_template("index.html")

# registration
@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
                
        new_user = (regi)(username=username, email=email)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"response": "User registered successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"response": f"Error: {str(e)}"})
    return render_template("register/registration.html")





@app.route("/login/")
def login():
    return render_template("register/login.html")

    
@app.route("/sum/<int:n>/<int:m>")
def restapi(n, m):
    result = {
        "Number1": n,
        "Number2": m,
        "Sum": n + m
    }
    return jsonify(result)

# test request  
@app.route("/test1",methods=['POST','GET'])
def test1():
    if request.method=='POST':
        res1 = request.json 
        name = res1['name']
        return jsonify({"response ":"Hello "+name})
    elif request.method=='GET':
        return jsonify({"response":"Get request"})
    else:
        return jsonify({"No request found"})


# Run the application (for development only)
if __name__ == "__main__":
    app.run(debug=True)
