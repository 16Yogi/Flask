import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'media')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customer_regi.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key_for_flask'  
db = SQLAlchemy()
db.init_app(app)

# Create models
class providerReg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    profile = db.Column(db.LargeBinary, nullable=True)
    address = db.Column(db.String, nullable=False)
    password1 = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.fullname}"


@app.route("/")
def index():
    return render_template('user.html')


# Provider routes
@app.route("/provider_home/")
def provider_home():
    return render_template('provider/index.html')


@app.route("/provider_reg/", methods=['POST', 'GET'])
def provider_reg():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # print(fullname)
        if not fullname or not email or not address or not password1 or not password2:
            # flash("All fields are required!", "danger")
            # return redirect(url_for('provider_reg'))
            return "all fields are required"

        if password1 != password2:
            # flash("Passwords do not match!", "danger")
            # return redirect(url_for('provider_reg'))
            print("password not matched")
        else:
            print("password ok")

        profile = None
        if 'profile' in request.files:
            file = request.files['profile']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                with open(file_path, 'rb') as f:
                    profile = f.read()
            print("file ok")
        else:
            print("fail")

        pro_reg = providerReg(
            fullname=fullname,
            email=email,
            profile=profile,
            address=address,
            password1=password1
        )
        # print(pro_reg)
        # print("ok")
        db.session.add(pro_reg) 
        db.session.commit()
        print("Registration successful")
        # flash("Registration successful!", "success")

    # pro_all_reg = providerReg.query.all()
    # return render_template('provider/regForm.html', registrations=pro_all_reg)
    return render_template('provider/regForm.html')



@app.route("/provider_login/")
def provider_login():
    return render_template('provider/login.html')


# Customer routes
@app.route("/customer_home/")
def cust_home():
    return render_template("customer/index.html")


@app.route("/customer_reg/")
def cust_reg():
    return render_template("customer/cust_reg.html")


@app.route("/customer_log/")
def cust_log():
    return render_template("customer/cust_login.html")


# File Upload Logic
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Main application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
        print("Database initialized successfully.")
    app.run(debug=False)

