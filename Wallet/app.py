from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, UserMixin, current_user
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'very-top-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
MINIMUM_BAL = 100


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    PhNo = db.Column(db.Integer, unique=True)
    balance = db.Column(db.Float, nullable=True, default=0)
    password = db.Column(db.String(100))
    logs = db.Column(db.String)

    def __repr__(self):
        return "User(name = {}, balance = {}".format(self.name, self.balance)


class LogModel(db.Model):
    __tablename__ = 'logs'
    SNo = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    status = db.Column(db.String(10))
    amount = db.Column(db.Float)


db.create_all()  #done only once


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized... Please login to continue', 'danger')
            return redirect(url_for('login'))
    return wrap


@login_manager.user_loader
def load_user(id):
    user = UserModel.query.get(id)
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, balance=current_user.balance, id=current_user.id)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('ID')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = UserModel.query.filter_by(id=id).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    flask_login.login_user(user)
    session['logged_in'] = True
    session['id'] = id
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/signup',methods=['POST'])
def signup_post():
    id = request.form.get('ID')
    uname = request.form.get('name')
    PhNo = request.form.get('Ph No')
    password = request.form.get('password')
    bal = MINIMUM_BAL
    user = UserModel.query.filter_by(id=id).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))
    new_user = UserModel(id=id, name=uname, PhNo=PhNo, balance=bal, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flask_login.logout_user()
    return redirect(url_for('index'))

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("balance", type=float, help="Balance of the user is required", required=True)
user_put_args.add_argument("PhNo", type=int, help="Phone number of the user is required", required=True)
user_put_args.add_argument("password", type=str, help="Password of the user is required", required=True)

user_withdraw_args = reqparse.RequestParser()
user_withdraw_args.add_argument("amount", location='json', type=float, help="Amount to withdraw is required", required=True)

user_deposit_args = reqparse.RequestParser()
user_deposit_args.add_argument("amount", location='json', type=float, help="Amount to deposit is required", required=True)

resource_fields = {
    'id': fields.String,
    'balance': fields.Float,
}
resource_log_fields = {
    'status': fields.String,
    'amount': fields.Float,
}

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, uid):
        result = UserModel.query.with_entities(UserModel.balance, UserModel.id).filter_by(id=uid).first()
        if not result:
            abort(404, message="User does not exist")
        dict = {"id":result["id"], "balance":result["balance"]}
        return dict

    @marshal_with(resource_fields)
    def put(self, uid):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(id=uid).first()
        if result:
            abort(409, message="User already exists")
        if(args["balance"]<MINIMUM_BAL):
            abort(409, message="Insufficient Balance Deposited. Min deposit = {}".format(MINIMUM_BAL))
        user = UserModel(id=uid, name=args['name'], PhNo=args["PhNo"], balance=args["balance"], password=generate_password_hash(args["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201


class Deposit(Resource):
    @is_logged_in
    @marshal_with(resource_fields)
    def patch(self):
        args = user_deposit_args.parse_args()
        curid = session.get('id')
        result = UserModel.query.filter_by(id=curid).first()
        if not result:
            abort(404, message="User does not exist. Cannot deposit :(")
        result.balance += args["amount"]
        log = LogModel(id=curid,status="Deposit",amount =args["amount"])
        db.session.add(log)
        db.session.commit()
        return result


class Withdraw(Resource):
    @is_logged_in
    @marshal_with(resource_fields)
    def patch(self):
        args = user_withdraw_args.parse_args()
        curid = session.get('id')
        result = UserModel.query.filter_by(id=curid).first()
        if result.balance < MINIMUM_BAL + args["amount"]:
            abort(403, message="Insufficient balance")
        result.balance -= args["amount"]
        log = LogModel(id=curid, status="Withdraw", amount=args["amount"])
        db.session.add(log)
        db.session.commit()
        return result

class Log(Resource):
    @is_logged_in
    @marshal_with(resource_log_fields)
    def get(self):
        curid = session.get('id')
        logs = LogModel.query.filter_by(id=curid).all()
        return logs

api.add_resource(User, "/user/<int:uid>")
api.add_resource(Withdraw, "/user/withdraw")
api.add_resource(Deposit, "/user/deposit")
api.add_resource(Log, "/user/log")

if __name__ == '__main__':
    app.run()

