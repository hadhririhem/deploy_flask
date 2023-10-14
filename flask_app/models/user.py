from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.pie import Pie
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pies = []

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL('exam').query_db( query, data ) 
    @classmethod 
    def get_all(cls) : 
        query = "SELECT * FROM users;"
        results = connectToMySQL('exam').query_db(query)
        users = []
        for u in results :
            users.append(cls(u))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('exam').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('exam').query_db(query, data)
        return cls(results[0])
    @classmethod 
    def get_all_pies(cls, data):
        query = "SELECT * FROM users LEFT JOIN pies ON pies.user_id = users.id WHERE users.id = %(id)s ORDER BY votes DESC;"
        results = connectToMySQL('exam').query_db(query, data)
        print(results)
        users = cls(results[0])
        for row in results:
            pie_data = {
                "id" : row["pies.id"],
                "name" : row["name"],
                "filling" : row["filling"],
                "crust" : row["crust"],
                "votes" : row["votes"],
                "created_at" : row["pies.created_at"],
                "updated_at" : row["pies.updated_at"]
            }
            pies = Pie(pie_data)
            users.pies.append(pies)
            return users
    @staticmethod 
    def is_valid(data) : 
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('exam').query_db(query, data)
        if len(results) >=1 :
            flash("Email already taken")
            is_valid = False
        if len(data["first_name"]) < 3 :
            flash("First Name should be at least 3 charachters")
            is_valid = False
        if len(data["last_name"]) < 3 :
            flash("Last Name should be at least 3 charachters")
            is_valid = False
        if not NAME_REGEX.match(data["first_name"]) : 
            flash("The first and Last name should be only charachters")
            is_valid = False
        if not NAME_REGEX.match(data["last_name"]) :
            flash("The first and Last name should be only charachters")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]) : 
            flash("The email you entered is not valid, please try again")
            is_valid = False
        if data["password"] != data["password-c"] :
            flash("The two passwords don't match")
            is_valid = False
        if len(data["password"]) <= 8 :
            flash("password too short")
            is_valid = False
        return is_valid


