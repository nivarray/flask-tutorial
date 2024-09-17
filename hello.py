from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# create a Flask Instance
app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# secret key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# initialize the DB
db = SQLAlchemy(app)

# create model
class Users(db.Model):  # define things you want here
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # create a string
    def __repr__(self):
        return "<Name %r>" % self.name

with app.app_context():
    db.create_all()


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class, need a secret key (security reason)
# This form will be displayed on the webpage
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['POST', 'GET'])
def add_user():
    name = None
    form = UserForm()  # class object
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# create a route decorator
@app.route('/')
def index():
    first_name = "Ray"
    stuff = "This is bold text"
    fav_pizza = ["Pepperoni", "Cheese", "Mushrooms",  41 ]
    return render_template("index.html", first_name=first_name, stuff=stuff, fav_pizza=fav_pizza)

# localhost:5000/user/ray
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# Create Name Page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NameForm() # Class object
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ' '
        flash("Form Submitted Successfully!")
    return render_template("name.html", name=name, form=form)

# Customer Error Pages
# 
#  Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#  Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500





if __name__ == "__main__":
    app.run(debug=True)