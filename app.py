from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort, url_for, make_response


load_dotenv()

app = Flask(__name__)

