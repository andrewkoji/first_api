from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    def get(self):
        """
        Returns the provided text in uppercase.
        ---
        tags:
          - Text Processing
        parameters:
          - name: text
            in: query
            type: string
            required: true
            description: The text to be converted to uppercase
        responses:
          200:
            description: A successful GET request
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    text:
                      type: string
                      description: The text in uppercase
        """
        text = request.args.get('text')
        if not text:
            return {"error": "The 'text' parameter is required."}, 400

        return {"text": text.upper()}, 200

class LowercaseText(Resource):

    def get(self):
        """
        Returns the provided text in uppercase.
        ---
        tags:
          - Text Processing
        parameters:
          - name: text
            in: query
            type: string
            required: true
            description: The text to be converted to lowercase
        responses:
          200:
            description: A successful GET request
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    text:
                      type: string
                      description: The text in lowercase
        """
        text = request.args.get('text')
        if not text:
            return {"error": "The 'text' parameter is required."}, 400

        return {"text": text.lower()}, 200


class DuplicateText(Resource):

    def get(self):
        """
        Returns the provided text duplicated a specified number of times, with optional case formatting.
        ---
        tags:
          - Text Processing
        parameters:
          - name: text
            in: query
            type: string
            required: true
            description: The text to be duplicated
          - name: times
            in: query
            type: integer
            required: true
            description: The number of times to duplicate the text
          - name: case
            in: query
            type: string
            required: true
            enum: [UPPER, LOWER, NONE]
            description: The case format to apply to the duplicated text
        responses:
          200:
            description: A successful GET request
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    text:
                      type: string
                      description: The processed duplicated text
          400:
            description: Invalid input parameters
        """
        text = request.args.get('text')
        times = request.args.get('times')
        case = request.args.get('case')

        # Validate parameters
        if not text:
            return {"error": "The 'text' parameter is required."}, 400
        if not times:
            return {"error": "The 'times' parameter is required."}, 400
        if not case:
            return {"error": "The 'case' parameter is required."}, 400

        try:
            duplication_factor = int(times)
            if duplication_factor <= 0:
                return {"error": "The 'times' parameter must be a positive integer."}, 400
        except ValueError:
            return {"error": "The 'times' parameter must be an integer."}, 400

        case = case.upper()
        if case not in ['UPPER', 'LOWER', 'NONE']:
            return {"error": "The 'case' parameter must be 'UPPER', 'LOWER', or 'NONE'."}, 400

        duplicated_text = text * duplication_factor

        if case == 'UPPER':
            result = duplicated_text.upper()
        elif case == 'LOWER':
            result = duplicated_text.lower()
        else:  # NONE
            result = duplicated_text

        return {"text": result}, 200



api.add_resource(DuplicateText, '/duplicate')
api.add_resource(UppercaseText, "/uppercase")
api.add_resource(LowercaseText, "/lowercase")
# api.add_resource(result_text, "/result_text")

if __name__ == "__main__":
    app.run(debug=True)
