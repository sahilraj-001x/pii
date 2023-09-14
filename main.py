from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, session, Response
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, TextAreaField, PasswordField, \
    BooleanField
from wtforms.validators import DataRequired, Length
import random
from cryptography.fernet import Fernet
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user, login_required
from wtforms.validators import DataRequired
import cv2
import secrets
import cvlib as cv
import sqlite3
import pyttsx3
import speech_recognition as sr
from questions import hindi, bengali
from test1 import *


# from test1 import *

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.7)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[10].id)

app.config['SECRET_KEY'] = 'abcd1234903632751753'
photos_folder = path.join('static', 'photos')
app.config["UPLOAD_FOLDER"] = photos_folder
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

rand_name = random.random()
random_hex = secrets.token_hex(8)
conn = sqlite3.connect("pii.db")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_casacde = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')


def talk(say):
    engine.say(say)
    engine.runAndWait()


r = sr.Recognizer()


@login_manager.user_loader
def load_user(user_id):
    return project.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pii.db'
db = SQLAlchemy(app)
token = random.randint(9999, 99999)
key = Fernet.generate_key()
f = Fernet(key)


class project(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    pro_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    connection = db.relationship('user', backref='puid', lazy=True)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Integer, nullable=False)
    ui = db.Column(db.Integer, unique=True, nullable=False, default=random.randint(11111111, 99999999))
    age = db.Column(db.Integer, nullable=False)
    ph_no = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(20))
    pincode = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.code'), nullable=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"user('{self.name}', '{self.ph_no}', '{self.project_id}', '{self.ui}')"


class CodeForm(FlaskForm):
    pro_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)],
                           render_kw={"placeholder": "Institute/Project Name", "onclick": "record()"})
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)],
                             render_kw={"placeholder": "Enter Password", "onclick": "record_pass()"})
    category = SelectField('Select Category',
                           choices=['', 'Government', 'Education', 'Healthcare', 'Industry', 'Media', 'Banking'],
                           validators=[DataRequired()])
    # category2 = SelectField('Select Database', choices=['', 'Local Database', 'Server Database'], validators=[DataRequired()])
    submit = SubmitField('Generate Code')
    submit2 = SubmitField('Proceed')


class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()], render_kw={"placeholder": "Enter your Name"})
    dob = DateField('dob', validators=[DataRequired()], render_kw={"placeholder": "Enter your DOB"})
    age = StringField('age', validators=[DataRequired()], render_kw={"placeholder": "Enter your age"})
    ph_no = IntegerField('phn', validators=[DataRequired()], render_kw={"placeholder": "Enter your phone number"})
    address = TextAreaField('address', validators=[DataRequired()], render_kw={"placeholder": "Enter your address"})
    state = StringField('state', validators=[DataRequired()], render_kw={"placeholder": "Enter your State"})
    pincode = IntegerField('pincode', validators=[DataRequired()], render_kw={"placeholder": "Enter your pincode"})
    proj_id = IntegerField('proj_id', validators=[DataRequired()])
    submit = SubmitField("Enter the details")

    # def validate_phone(self, ph_no):
    #     if ph_no.data != current_user.ph_no:
    #         user_phn = user.query.filter_by(ph_no=ph_no.data).first()
    #         if user_phn:
    #             raise ValueError('Please check your Phone Number')


class LoginForm(FlaskForm):
    pro_name = StringField('pro_name', validators=[DataRequired()], render_kw={"placeholder": "Project/Institute Name"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


@app.route("/", methods=['POST', 'GET'])
@app.route("/intro", methods=['POST', 'GET'])
def into_to_pii():
    # talk("Welcome to Pye. It is developed to automate, the manual process of entering data, so that people don't have to wait in long queue, and no error occur, while entering the data. After getting the details of different users, Pye generates a unique eye d for everyone, which is sent directly in their email. Pye uses various algorithms, to compress and encrypt the data, before saving it in database, and for securing the network connection in the web.  Hello, I am your virtual assistant, to help you know Pye better.")
    # return redirect("/home")
    return render_template("intro.html")


@app.route("/home", methods=['POST', 'GET'])
def homepage():
    if current_user.is_authenticated:
        return redirect("/startpage_local")
    form = CodeForm()
    if form.validate_on_submit():
        en_pro_name = f.encrypt(form.pro_name.data.encode())
        en_pro_cat = f.encrypt(form.category.data.encode())
        en_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        project_details = project(code=token, pro_name=form.pro_name.data, password=en_pass, type=form.category.data)
        db.session.add(project_details)
        db.session.commit()
    return render_template("home.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/startpage_local")
    form = LoginForm()
    if form.validate_on_submit():
        name = project.query.filter_by(pro_name=form.pro_name.data).first()
        if name and bcrypt.check_password_hash(name.password, form.password.data):
            login_user(name, remember=form.remember.data)
            return redirect('/startpage_local')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/login')


@app.route("/startpage_local", methods=['POST', 'GET'])
@login_required
def startpage_local():
    return render_template("startpage.html")


@app.route("/startpage_server", methods=['POST', 'GET'])
def startpage_server():
    project = request.form.get("project")
    return render_template("startpage.html")


@app.route("/face_capture", methods=['POST', 'GET'])
def capture():
    Response(face_scan())

    return redirect("/home")
# return render_template("/capture.html")


def actions():
    try:
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source, phrase_time_limit=5)
            mic = r.recognize_google(audio_text)
            print(mic)
    except:
        print("Sorry, I did not get that")
    return mic


@app.route("/add_data", methods=['POST', 'GET'])
@login_required
def add_data():
    # form = UserForm()
    # # if request.method == 'POST':
    # if form.validate_on_submit():
    #     img_name = session['img_name']
    #     user_details = user(name=form.name.data, dob=form.dob.data, age=form.age.data, ph_no=form.ph_no.data,
    #                                 address=form.address.data,
    #                                 state=form.state.data, pincode=form.pincode.data, project_id=current_user.code,
    #                                 image=img_name)
    #     db.session.add(user_details)
    #     db.session.commit()
    #     return redirect("/startpage_local")

    # return render_template("add.html", form=form)




    # talk("Please select your language")
    engine.say("Please select your language")
    engine.runAndWait()
    mic = actions()
    print(mic)

    if "hindi" in mic:
        print("hindi")
        hindi()
    if "bengali" or "bangla" in mic:
        print("bengali")
        bengali()
    # return render_template("blank.html")
    return redirect("/face_capture")
    # return render_template("add.html")

@app.route("/test_for_pyaudio")
def test_for_pyaudio():
    run()
    # engine.say("Please select your language")
    # engine.runAndWait()
    # command = actions()
    # print(command)
    #
    # if "hindi" in command:
    #     print("hindi")
    #     hindi()
    # if "bengali" or "bangla" in command:
    #     print("bengali")
    #     bengali()
    # return redirect("/face_capture")


@app.route("/saving_data", methods=['POST', 'GET'])
@login_required
def sav_data():
    form = UserForm()


@app.route("/modify_data", methods=['POST', 'GET'])
def modify_data():
    posts = user.query.filter_by(project_id=current_user.code).all()
    # image_file = url_for('open_cv', filename='faces/' + current_user.code)
    return render_template("modify.html", users=posts)


@app.route("/timed_out", methods=['POST', 'GET'])
def error_or_404():
    return render_template("timed_out.html")


@app.route("/user//delete", methods=['POST', 'GET'])
@login_required
def delete_post():
    conn.execute("DELETE FROM user WHERE ")
    return redirect("/startpage_local")


def face_scan():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        face, confidence = cv.detect_face(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_casacde.detectMultiScale(roi_gray)
            for (x1, y1, w1, h1) in eyes:
                cv2.rectangle(roi_color, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

            smiles = smile_cascade.detectMultiScale(gray, 2.1, 25)
            for (x2, y2, w2, h2) in smiles:
                cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

        k = cv2.waitKey(160) & 0xff
        if k == 150:
            break

        if not ret:
            print("failed to grab frame")
            break

        img_name = random_hex + ".png"
        session['img_name'] = img_name
        cv2.imwrite('/Users/apple/PycharmProjects/pii/open_cv/faces/' + img_name, frame)
        break


if __name__ == "__main__":
    app.secret_key = 'thisismysupersecretkey'
    app.run(debug=True)
