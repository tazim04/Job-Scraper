from flask import Blueprint, jsonify
from .scraper import scrape_jobs
from .comparer import Comparer
import nest_asyncio

nest_asyncio.apply() # apply nest_asyncio to allow asyncio to work with sync code

main = Blueprint('main', __name__) # create a blueprint for the main route

# test route
# @main.route('/api/')
# def test():
#     return jsonify({'message': 'Hello, World!'})

@main.route('/api/')
def test_analyzer():
    comparer = Comparer()
    return comparer.test()

@main.route('/api/jobs')
def get_jobs():
    print("\n=== Starting job scraping request ===")
    try:
        jobs = scrape_jobs()
        print(f"Found {len(jobs)} jobs")
        return jsonify(jobs)
    except Exception as e:
        print(f"Error in /api/jobs: {e}")
        return jsonify({"error": str(e)}), 500