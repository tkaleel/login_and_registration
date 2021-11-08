from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name, last_name, email_address, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(email_address)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('login_registration_schema').query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('login_registration_schema').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email_address = %(email_address)s;"
        result = connectToMySQL('login_registration_schema').query_db(query,data)
        if len(result) <1:
            return False
        return cls(result[0])
        
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email_address']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid