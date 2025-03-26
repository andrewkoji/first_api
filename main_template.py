from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
import openai
import os 
import pandas as pd
import numpy as np


app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
def quad_linear_system():
    while True:
        x = np.random.randint(-10, 10)
        c = np.random.randint(-10, 10)  # Coefficient of x in the quadratic equation
        e = np.random.randint(-50, 50)  # Constant term in the quadratic equation
        d = np.random.randint(-5, 5)    # Coefficient of x in the linear equation
        f = np.random.randint(-10, 10)  # Constant term in the linear equation
        
        # Linear equation: y = dx + f
        linear = (
            f"y = "
            + (f"{'-' if d < 0 else ''}{'x' if abs(d) == 1 else f'{abs(d)}x'} " if d != 0 else "")
            + (f"{'+ ' if f > 0 and d != 0 else '- ' if f < 0 else ''}{abs(f)}" if f != 0 else "")
        ).strip()

        # Quadratic equation: y = x^2 + cx + e
        quadratic = (
            f"y = x^2 "
            + (f"{'+ ' if c > 0 else '- '}{'x' if abs(c) == 1 else f'{abs(c)}x'} " if c != 0 else "")
            + (f"{'+ ' if e > 0 and c != 0 else '- ' if e < 0 else ''}{abs(e)}" if e != 0 else "")
        ).strip()
        x_values = np.arange(-10, 11)
        df = pd.DataFrame({
            'x': x_values,  # Directly assign the array to the 'x' column
            f'{linear}': [d * t + f for t in x_values],
            f'{quadratic}': [t**2 + c * t + e for t in x_values]
        })
        b = c - d
        a = e - f
        
        # factored_function = f"x^2 {'+ ' if b > 0 else '- '}{abs(b)}x {'+ ' if a > 0 else '- '}{abs(a)}"
        factored_function = (
            f"x^2 "
            + (f"{'+ ' if b > 0 else '- '}{'x' if abs(b) == 1 else f'{abs(b)}x'} " if b != 0 else "")
            + (f"{'+ ' if a > 0 and b != 0 else '- ' if a < 0 else ''}{abs(a)}" if a != 0 else "")
        ).strip()
        if a == 0:
            continue
        
        factors = [(i, a // i) for i in range(1, abs(a) + 1) if a % i == 0]
        
        for i, j in factors:
            if i + j == b:
                return {
                    "coefficients": [1, c, e, d, f],
                    "linear_function": linear,
                    "quadratic_function": quadratic,
                    "factored_function": f"{factored_function} = 0",
                    "factors": f"(x {'-' if i < 0 else '+'} {abs(i)})(x {'-' if j < 0 else '+'} {abs(j)}) = 0",
                    "roots": [f"x = {'' if i < 0 else '-'} {abs(i)},  x = {'' if j < 0 else '-'} {abs(j)}"],
                    "substitution": [f"y = {d}({-i})+{f} = {-i*d + f}", f"y = {d}({-j})+{f} = {-j*d + f}"],
                    "solutions": [f"( {-i}, {-i*d + f})",f"({-j}, {-j*d + f})"],
                    "table of values": df.to_dict(orient="records") 
                }

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
class QuadraticSystem(Resource):
    def get(self):
        """
        Returns a randomly generated quadratic-linear system and its factored form.
        ---
        tags:
          - Quadratic System Generator
        responses:
          200:
            description: A successfully generated quadratic-linear system
            content:
              application/json:
                schema:
                  type: object
        """
        try:
            return quad_linear_system(), 200
        except Exception as e:
            return {"error": f"Failed to generate system: {str(e)}"}, 500

api.add_resource(QuadraticSystem, '/quadratic-system')

api.add_resource(Chatbot, '/chatbot')


# api.add_resource(result_text, "/result_text")

if __name__ == "__main__":
    app.run(debug=True)
