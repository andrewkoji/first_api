from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import pandas as pd
import numpy as np
import random
import fractions
import signal
import sys

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


def generate_linear_equation():
    """Generate a random linear equation in slope-intercept form (y = mx + b)."""
    numerator = random.randint(-10, 10)  # Random numerator
    denominator = random.randint(1, 10)  # Random denominator (non-zero)
    m = fractions.Fraction(numerator, denominator)  # Slope as a fraction
    b = random.randint(-10, 10)  # Random y-intercept

    if m == 0:
        # If slope is 0, the equation is a horizontal line
        equation = f"y = {b}"
    elif b == 0:
        # If y-intercept is 0, omit it from the equation
        equation = f"y = {m}x" if m != 1 else "y = x"
    else:
        # General case
        slope_part = f"{m}x" if m != 1 else "x"
        equation = f"y = {slope_part} {'+' if b > 0 else '-'} {abs(b)}"

    return {
        "equation": equation,
        "slope": float(m),
        "y_intercept": b
    }

@app.get("/linear-equation", tags=["Linear Equation Generator"])
async def get_linear_equation():
    """
    Returns a randomly generated linear equation in slope-intercept form.
    """
    try:
        return generate_linear_equation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate linear equation: {str(e)}")


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

# Graceful shutdown handler
def shutdown_handler(signum, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    import uvicorn
    import os
    # Use the PORT environment variable provided by Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("fastapi_template:app", host="0.0.0.0", port=port, reload=True)