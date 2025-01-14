from flask import Blueprint, jsonify
from .scraper import scrape_jobs
import nest_asyncio

nest_asyncio.apply() # apply nest_asyncio to allow asyncio to work with sync code

main = Blueprint('main', __name__) # create a blueprint for the main route

@main.route('/api/jobs')
def get_jobs():
    jobs = scrape_jobs() # scrape jobs
    return jsonify(jobs) # return jobs as a json response