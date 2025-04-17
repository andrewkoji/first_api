from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS for your Streamlit app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://linear-quadratic-system.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def quad_linear_system():
    # ...existing code...
    while True:
        x = np.random.randint(-15, 15)
        c = np.random.randint(-10, 10)
        e = np.random.randint(-50, 50)
        d = np.random.randint(-5, 5)
        f = np.random.randint(-10, 10)

        linear = (
            f"y = "
            + (f"{'-' if d < 0 else ''}{'x' if abs(d) == 1 else f'{abs(d)}x'} " if d != 0 else "")
            + (f"{'+ ' if f > 0 and d != 0 else '- ' if f < 0 else ''}{abs(f)}" if f != 0 else "")
        ).strip()

        quadratic = (
            f"y = x^2 "
            + (f"{'+ ' if c > 0 else '- '}{'x' if abs(c) == 1 else f'{abs(c)}x'} " if c != 0 else "")
            + (f"{'+ ' if e > 0 and c != 0 else '- ' if e < 0 else ''}{abs(e)}" if e != 0 else "")
        ).strip()

        x_values = np.arange(-10, 11)
        df = pd.DataFrame({
            'x': x_values,
            f'{linear}': [d * t + f for t in x_values],
            f'{quadratic}': [t**2 + c * t + e for t in x_values]
        })
        b = c - d
        a = e - f

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
                    "solutions": [f"( {-i}, {-i*d + f})", f"({-j}, {-j*d + f})"],
                    "table of values": df.to_dict(orient="records")
                }


@app.get("/quadratic-system", tags=["Quadratic System Generator"])
async def get_quadratic_system():
    """
    Returns a randomly generated quadratic-linear system and its factored form.
    """
    try:
        return quad_linear_system()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate system: {str(e)}")


@app.get("/chatbot", tags=["AI Chatbot"])
async def get_chatbot_response(prompt: str = Query(..., description="The prompt to send to the chatbot")):
    """
    Returns a response from the OpenAI GPT-3.5 chatbot based on the provided prompt.
    """
    if not prompt:
        raise HTTPException(status_code=400, detail="The 'prompt' parameter is required.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7,
        )

        answer = response.choices[0].message['content'].strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get response from OpenAI: {str(e)}")


@app.get("/", tags=["Default"])
async def root():
    """
    Default route for the root endpoint.
    """
    return {"message": "Welcome to the Quadratic-Linear System API. Use /quadratic-system or /chatbot endpoints."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)