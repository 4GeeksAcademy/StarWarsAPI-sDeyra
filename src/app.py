"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    usuarios= User.query.all()
    if usuarios== []:
        return jsonify({"msg": "No existen usuarios"}), 404
    response_body = [usuario.serialize() for usuario in usuarios]
    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes= Personaje.query.all()
    if personajes== []:
        return jsonify({"msg": "No existe personaje"}), 404
    response_body = [personaje.serialize() for personaje in personajes]
    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    planetas= Planet.query.all()
    if planetas== []:
        return jsonify({"msg": "No existe planeta"}), 404
    response_body = [planeta.serialize() for planeta in planetas]
    return jsonify(response_body), 200

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personajes_id(id): 
    personaje=Personaje.query.filter_by(id=id).first() #el primer id hace referencia a la tabla, el  segundo al de la ruta dinamica linea 63
    if personaje is None:
        return jsonify({"msg": "No existe el personaje"}), 404
    return jsonify(personaje.serialize()), 200

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planetas_id(id): 
    planeta=Planet.query.filter_by(id=id).first()
    if planeta is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    return jsonify(planeta.serialize()), 200

@app.route('/favorites/planetas/<int:planet_id>', methods=['POST'])
def post_planetas_fav(planet_id):
    planeta=Planet.query.filter_by(id=planet_id).first()
    if planeta is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    
    new_fav=Favorites(
        user_id=4, 
        planetid=planet_id,
    )
    db.session.add(new_fav)
    db.session.commit()
    return jsonify ({"msg": "Nuevo favorito creado"}), 201

@app.route('/favorites/personajes/<int:personaje_id>', methods=['POST'])
def post_personaje_fav(personaje_id):
    personaje_id=Personaje.query.filter_by(id=personaje_id).first()
    if personaje_id is None:
        return jsonify({"msg": "No existe el personaje"}), 404
    
    new_fav=Favorites(
        user_id=4, 
        post_personaje_fav=personaje_id,
    )
    db.session.add(new_fav)
    db.session.commit()
    return jsonify ({"msg": "Nuevo favorito creado"}), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
