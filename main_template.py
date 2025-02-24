from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
import openai
import os 


app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

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

class Chatbot(Resource):
    def get(self):
        """
        Returns a response from the OpenAI GPT-3.5 chatbot based on the provided prompt.
        ---
        tags:
          - AI Chatbot
        parameters:
          - name: prompt
            in: query
            type: string
            required: true
            description: The prompt to send to the chatbot
        responses:
          200:
            description: A successful GET request with chatbot response
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    answer:
                      type: string
                      description: The chatbot's response
          400:
            description: Invalid input parameters
        """
        prompt = request.args.get('prompt')

        if not prompt:
            return {"error": "The 'prompt' parameter is required."}, 400

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,  # Limit response length to manage token usage
                temperature=0.7,  # Controls creativity (0 = deterministic, 1 = creative)
            )

            answer = response.choices[0].message['content'].strip()
            return {"answer": answer}, 200

        except Exception as e:
            return {"error": f"Failed to get response from OpenAI: {str(e)}"}, 500


api.add_resource(Chatbot, '/chatbot')

api.add_resource(DuplicateText, '/duplicate')
api.add_resource(UppercaseText, "/uppercase")
api.add_resource(LowercaseText, "/lowercase")
# api.add_resource(result_text, "/result_text")

if __name__ == "__main__":
    app.run(debug=True)
