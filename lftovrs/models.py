from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid

db = SQLAlchemy()
ma = Marshmallow()

# ingredients table that stores id, name of ingredient, ingredient type, amount, and user id (token) that is associated with the ingredient
class Ingredient(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    amount = db.Column(db.String) # ingredient amount is optional
    token = db.Column(db.String, nullable=False)

    def __init__(self, name, category, token, amount=''):
        self.id = self.set_id()
        self.name = name
        self.category = category
        self.amount = amount
        self.token = token

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name} has been added to your leftovers."

class IngredientSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'category', 'amount']

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)
