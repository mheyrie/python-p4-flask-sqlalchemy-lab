#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    return f'''
            <h1>
            <ul>ID: {animal.id}</ul>
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
            </h1>
        '''

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    response_body = f''
    response_body += f'<h1><ul>ID: {zookeeper.id}</ul></h1>'
    response_body += f'<h1><ul>Name: {zookeeper.name}</ul></h1>'
    response_body += f'<h1><ul>Birthday: {zookeeper.birthday}</ul></h1>'

    animals = [animal for animal in zookeeper.animals]

    for animal in animals:
        response_body += f'<h1><ul>Animal: {animal.name}</ul></h1>'
    
    response = make_response(response_body)
    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    response_body = f''
    response_body += f'<h1><ul>ID: {enclosure.id}</ul></h1>'
    response_body += f'<h1><ul>Environment: {enclosure.environment}</ul></h1>'
    response_body += f'<h1><ul>Open to Visitors: {enclosure.open_to_visitors}</ul></h1>'

    animals = [animal for animal in enclosure.animals]

    for animal in animals:
        response_body += f'<h1><ul>Animal: {animal.name}</ul></h1>'
    
    response = make_response(response_body)
    
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
