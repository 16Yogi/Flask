from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define the database model
class RegisterForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # String with max length
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email as a string

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"


# Routes
@app.route("/",methods=['POST','GET'])
def home():
    alluser = RegisterForm.query.all()
    return render_template('pages/index.html')


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        # Save to the database
        new_user = RegisterForm(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        print(f"Registered: {name}, {email}")
    return render_template('pages/register.html')


@app.route("/login/")
def login():
    return render_template('pages/login.html')


if __name__ == "__main__":
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
