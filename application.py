# from flask import Flask
# app = Flask(__name__)
# from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)


# class Drink(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(80),unique=True,nullable=False)
#     description = db.Column(db.String(120))

#     def __repr__(self):
#         return f"{self.name} - {self.description}"

# @app.route('/')
# def index():
#     return 'Hello!'

# @app.route('/drinks')
# def get_drinks():
#     return {"drinks":"drink data"}

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# Model (table)
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


# Home route
@app.route('/')
def index():
    return "Hello!"


# GET all drinks
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {
            "id": drink.id,
            "name": drink.name,
            "description": drink.description
        }
        output.append(drink_data)

    return {"drinks": output}


# GET single drink
@app.route('/drinks/<int:id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)

    return {
        "id": drink.id,
        "name": drink.name,
        "description": drink.description
    }


# ADD new drink
@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.get_json()

    new_drink = Drink(
        name=data['name'],
        description=data['description']
    )

    db.session.add(new_drink)
    db.session.commit()

    return {"message": "Drink added successfully"}


# UPDATE drink
@app.route('/drinks/<int:id>', methods=['PUT'])
def update_drink(id):
    drink = Drink.query.get_or_404(id)

    data = request.get_json()

    drink.name = data['name']
    drink.description = data['description']

    db.session.commit()

    return {"message": "Drink updated successfully"}


# DELETE drink
@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get_or_404(id)

    db.session.delete(drink)
    db.session.commit()

    return {"message": "Drink deleted successfully"}


# Run the server
if __name__ == "__main__":
    app.run(debug=True)