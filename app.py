from flask import Flask, render_template, request, redirect, url_for
from utu.downloader import Downloader
from utu.utils import b64encode_filter
from utu.endpoints import QUESTION_PAPERS
import time

app = Flask(__name__)
app.jinja_env.filters['b64encode'] = b64encode_filter

downloader = Downloader()

@app.get('/')
def home():
    return render_template("index.html")

@app.get('/courses')
def courses():
    start = time.time()
    
    year = request.args.get('year', '')
    season = request.args.get('season', '')
    # TODO: return bad/malaformed request if keys not included.
    courses = downloader.get_papers(int(year), season)
    end = time.time()
    return render_template("courses.html", data=courses, year=year, season=season, time=round((end - start), 2) )

@app.get('/get-papers/')
def get_papers():
    zip_url = request.args.get('zip', '')
    
    return render_template('papers.html', zip_url=zip_url)

@app.get('/download/')
def download():
    start = time.time()
    zip_url = request.args.get('zip', '')
    
    files = downloader.download_zip(zip_url)
    
    end = time.time()
    return render_template('paper_view.html', files=files, time=round((end - start), 2))