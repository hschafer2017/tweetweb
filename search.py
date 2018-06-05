import os
from flask import Flask, redirect, render_template, request


app = Flask(__name__)

@app.route('/')
def get_homepage():
   return "Hello World"


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug = True)