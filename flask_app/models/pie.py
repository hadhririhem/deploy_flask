from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

class Pie:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.votes = data['votes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO pies ( name , filling , crust , created_at, updated_at, user_id ) VALUES ( %(name)s , %(filling)s , %(crust)s ,NOW() , NOW(), %(user_id)s);"
        return connectToMySQL('exam').query_db( query, data ) 
    @classmethod
    def get_all(cls) : 
        query = "SELECT * FROM pies;"
        results = connectToMySQL('exam').query_db(query)
        print (results)
        pies = []
        for p in results :
            pies.append(cls(p))
        return pies
    @classmethod
    def get_pie(cls, data) : 
        query = "SELECT * FROM pies WHERE id = %(id)s;"
        results = connectToMySQL('exam').query_db(query, data)
        return cls(results[0])
    @classmethod
    def update_pie(cls, data) : 
        query = "UPDATE pies SET name=%(name)s, filling =%(filling)s, crust=%(crust)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('exam').query_db(query,data)
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pies WHERE id = %(id)s;"
        return connectToMySQL('exam').query_db(query,data)
    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data["name"]) < 1 :
            flash("You need to enter a name")
            is_valid = False
        if len(data["filling"]) < 1 :
            flash("You need to enter a filling")
            is_valid =  False
        if len ( data["crust"]) < 1  : 
            flash("You need to enter a crust")
            is_valid = False
        return is_valid