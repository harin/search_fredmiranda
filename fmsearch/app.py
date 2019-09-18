import sqlite3
from flask import g, Flask, render_template
from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
from multiprocessing import Pool
from .pool_methods import parse_page

p = Pool(4)
app = Flask(__name__)

@app.route('/')
def index():
    pages = p.map(parse_page, range(4))
    merged_page = []
    for page in pages:
        merged_page += page

    df = pd.DataFrame(merged_page)
    
    print(pages)
    return str(df.to_html())
