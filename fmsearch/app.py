import sqlite3
from flask import g, Flask, render_template
from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
from multiprocessing import Pool
from .pool_methods import parse_page
from datetime import datetime, timedelta

p = Pool(4)
app = Flask(__name__)

def get_data_df():
    pages = p.map(parse_page, range(10))
    merged_page = []
    for page in pages:
        merged_page += page

    df = pd.DataFrame(merged_page)
    df = df.dropna()
    df.href = df.href.apply(lambda path: f"https://www.fredmiranda.com{path}")
    json_data = df.to_json(orient='records') 
    return json_data

@app.route('/')
def index():
    json_data = get_data_df()
    return render_template('main.html', json_data=json_data)
