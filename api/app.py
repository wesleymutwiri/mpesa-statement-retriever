
# from app.models import Goals
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import field_for

from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

import sqlite3
import jwt
import os
import time

load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
    os.path.abspath("../database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


username = os.environ.get('USERNAME')
default_password = os.environ.get('PASSWORD')


def generate_token(expires_in=600):
    return jwt.encode({'id': 1, 'exp': time.time() + expires_in}, app.config['SECRET_KEY'], 'HS256')


def verify_auth_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        return "Shit is valid G"
    except:
        raise(ValueError, "Auth token is invalid")


class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    due_date = db.Column(db.Date(), nullable=False)
    price_required = db.Column(db.Integer(), nullable=False, default=0)
    current_price = db.Column(db.Integer(), default=0)
    is_completed = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BudgetCategory(db.Model):
    __tablename__ = 'budget_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    budgets = db.relationship('Budget', backref='budget_category', lazy=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(
        "budget_category.id"), nullable=False)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GoalSchema(ma.SQLAlchemyAutoSchema):
    id = field_for(Goals, 'id', dump_only=True)

    class Meta:
        model = Goals
        load_instance = True


class BudgetSchema(ma.SQLAlchemyAutoSchema):
    id = field_for(Budget, 'id', dump_only=True)

    class Meta:
        model = Budget
        load_instance = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response(jsonify({'message': "Where is your token?"}), 403)
        try:
            verify_auth_token(token)
        except:
            return make_response(jsonify({'message': "We have issues here"}), 400)
        return f(*args, **kwargs)
    return decorator


@app.route("/login", methods=['POST'])
def get_token():
    credentials = request.get_json()
    print(default_password)
    print(username)
    if credentials["username"] == username and credentials["password"] == default_password:
        token = generate_token()
        return jsonify({'token': token, 'duration': 600})
    else:
        return make_response(jsonify({"response": "Invalid credentials"}), 403)


@app.route("/", methods=['GET'])
def home():
    return {"Name": "Home-page"}


@app.route("/transactions", methods=['GET'])
@token_required
def get_transactions():
    conn = sqlite3.connect("../database.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(
        'SELECT Balance,"Completion Time",Details,Withdrawn FROM Transactions ORDER BY "-Completion Time"')
    rows = cur.fetchall()
    return jsonify(rows)


@app.route("/transaction/<month>")
def get_month_transactions(month):
    conn = sqlite3.connect("../database.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # cur.execute(
    # "SELECT * FROM 'MonthlyTotals'")
    query = "SELECT * FROM TotalsTrial WHERE dateFrom BETWEEN datetime('%m', 'start of month') AND datetime('now', 'localtime') = {}".format(
        month)
    cur.execute(query)
    rows = cur.fetchall()
    return jsonify(rows)


@app.route("/goals", methods=['POST'])
def create_goal():
    post_data = request.get_json()
    goal_schema = GoalSchema()
    goal = goal_schema.load(post_data)
    result = goal_schema.dump(goal.create())
    return make_response(jsonify({"result": result}), 201)


@app.route("/goals/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    current_goal = Goals.query.get(goal_id)
    put_data = request.get_json()
    goal_schema = GoalSchema()
    goal = goal_schema.load(put_data, instance=current_goal, partial=True)
    result = goal_schema.dump(goal.create())
    return jsonify({"message": "record has been updated successfully", "result": result})


@app.route("/goals/<goal_id>", methods=["GET"])
def get_single_goal(goal_id):
    current_goal = Goals.query.get(goal_id)

    goal_schema = GoalSchema()
    result = goal_schema.dump(current_goal.create())
    return jsonify({"result": result})


@app.route("/goals")
def get_goals():
    goals = Goals.query.all()
    goal_schema = GoalSchema(many=True)
    goal = goal_schema.dump(goals)
    return jsonify({"goals": goal})


# @app.route("/goals")
# def create_tables():
#     conn = sqlite3.connect("database.db")
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
if __name__ == '__main__':
    app.run()
