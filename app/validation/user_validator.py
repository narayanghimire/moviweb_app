from flask import request
from werkzeug.exceptions import BadRequest

class UserValidator:
    @staticmethod
    def validate_add_user():
        """Validate the input name from the request"""
        name = request.form.get('name')
        if not name or len(name.strip()) == 0:
            raise BadRequest('Name is required and cannot be empty.')
        if not isinstance(name, str) or not name.isalpha():
            raise BadRequest('Name must be a string containing only alphabetic characters.')
        return name