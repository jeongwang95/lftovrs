from flask import Blueprint, request, jsonify
from lftovrs.models import db, Ingredient, ingredient_schema, ingredients_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# add new ingredient
@api.route('/ingredients/<token>', methods = ['POST'])
def add_ingredient(token):
    name = request.json['name'].strip().lower()
    category = request.json['category']
    amount = request.json['amount'].strip().lower()

    # check if ingredient is already in user's leftovers
    if Ingredient.query.filter_by(name=name, token=token).first():
        return jsonify({'message': f'{name} is already in your leftovers. If you want to update your ingredient, use the UPDATE function.'}), 401
    else:
        ingredient = Ingredient(name, category, token, amount)

        db.session.add(ingredient)
        db.session.commit()

        response = ingredient_schema.dump(ingredient)

        return jsonify(response)

# retrieve all ingredients for current user
@api.route('/ingredients/<token>', methods = ['GET'])
def get_ingredients(token):
    ingredients = Ingredient.query.filter_by(token=token).all()
    
    response = ingredients_schema.dump(ingredients)

    return jsonify(response)

# update an ingredient
@api.route('/ingredients/<token>/<id>', methods = ['PUT', 'POST'])
def update_ingredient(token, id):
    ingredient = Ingredient.query.get(id)
    ingredient.name = request.json['name'].strip().lower()
    ingredient.category = request.json['category']
    ingredient.amount = request.json['amount'].strip().lower()

    db.session.commit()

    response = ingredient_schema.dump(ingredient)

    return jsonify(response)

# delete an ingredient
@api.route('ingredients/<token>/<id>', methods = ['DELETE'])
def delete_ingredient(token, id):
    ingredient = Ingredient.query.get(id)

    db.session.delete(ingredient)
    db.session.commit()

    response = ingredient_schema.dump(ingredient)

    return jsonify(response)