from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
import openai
import os 


import os
print(os.getenv("OPENAI_API_KEY"))
