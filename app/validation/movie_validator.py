from flask import request
from werkzeug.exceptions import BadRequest

class MovieValidator:
    @staticmethod
    def validate_add_movie():
        """Validate the input data for adding a new movie."""
        # Get the 'name' field from the form data
        name = request.form.get('name')

        if not name or len(name.strip()) == 0:
            raise BadRequest('Movie name is required and cannot be empty.')

        # Return the valid movie name
        return name

    @staticmethod
    def validate_update_movie():
        """Validate the input data for updating an existing movie."""
        name = request.form.get('name')
        year = request.form.get('year')

        if not name or len(name.strip()) == 0:
            raise BadRequest('Movie name is required and cannot be empty.')

        if not year or not year.isdigit() or len(year) != 4:
            raise BadRequest('Year must be a valid 4-digit number.')

        return name, year
