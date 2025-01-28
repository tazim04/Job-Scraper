from flask import Blueprint, jsonify
from .scrapers.glassdoor_scraper import JobScraperGlassdoor
from .comparer import Comparer
import nest_asyncio
import os
import json

nest_asyncio.apply() # apply nest_asyncio to allow asyncio to work with sync code

main = Blueprint('main', __name__) # create a blueprint for the main route
glassdoor_scraper = JobScraperGlassdoor
comparer = Comparer()

# change this to work with s3 buckets later 
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Navigate to the project root
resume_path = os.path.join(base_dir, "Resume - Tazim Khan.pdf")

# test route
# @main.route('/api/')
# def test():
#     return jsonify({'message': 'Hello, World!'})

@main.route('/api/')
def test_analyzer():
    return comparer.test()

@main.route('/api/compare')
def compare():
    print("\n=== Starting job scraping request ===")
    try:
        job = glassdoor_scraper.scrape_job()     
        groq_res = comparer.compare(resume_path, job.description)
        
        print(groq_res)
        
        if isinstance(groq_res, str):
            groq_res = json.loads(groq_res)
        
        job.summary = groq_res.get("summary")
        job.key_technologies = groq_res.get("key_technologies")
        job.key_skills = groq_res.get("key_skills")
        job.location_type = groq_res.get("location_type")
        job.job_type = groq_res.get("job_type")
        job.matching_analysis = groq_res.get("matching_analysis")
        job.score = groq_res.get("score")
        job.recommendations = groq_res.get("recommendations")

        return jsonify(job.to_dict())      


    except Exception as e:
        print(f"Error in /api/jobs: {e}")
        return jsonify({"error": str(e)}), 500