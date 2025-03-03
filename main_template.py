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
                max_tokens=250,  # Limit response length to manage token usage
                temperature=0.7,  # Controls creativity (0 = deterministic, 1 = creative)
            )

            answer = response.choices[0].message['content'].strip()
            return {"answer": answer}, 200

        except Exception as e:
            return {"error": f"Failed to get response from OpenAI: {str(e)}"}, 500


api.add_resource(Chatbot, '/chatbot')


# api.add_resource(result_text, "/result_text")

if __name__ == "__main__":
    app.run(debug=True)
