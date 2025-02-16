from flask import Blueprint, jsonify, request
from .scrapers.glassdoor_scraper import JobScraperGlassdoor
from .scrapers.linkedin_scraper import JobScraperLinkedIn
from .comparer import Comparer
import nest_asyncio
import os
import json
from .aws_config import AWS_BUCKET_NAME, AWS_REGION
from .s3_util import upload_file_to_s3, generate_presigned_url
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import re


nest_asyncio.apply() # apply nest_asyncio to allow asyncio to work with sync code

# Load environment variables
load_dotenv()

main = Blueprint('main', __name__) # create a blueprint for the main route
# glassdoor_scraper = JobScraperGlassdoor
comparer = Comparer()

@main.route('/api/')
def test_analyzer():
    return comparer.test()


@main.route('/api/compare', methods=["POST"])
def compare():
    print("\n=== Starting job scraping request ===")
    try:
        resume_path = request.json.get("resume_path")
        original_link = request.json.get("link")
        
        # Extract job ID from LinkedIn URL
        parsed = urlparse(original_link)
        query_params = parse_qs(parsed.query)
        
        # Try to get from query parameter first
        job_id = query_params.get('currentJobId', [None])[0]
        
        # If not found in query params, try to get from path
        if not job_id:
            path_match = re.search(r'/jobs/view/(\d+)', parsed.path)
            if path_match:
                job_id = path_match.group(1)
        
        if not job_id:
            return jsonify({"error": "Could not extract job ID from URL"}), 400
        
        # Construct guest API URL
        guest_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        linkedin_scraper = JobScraperLinkedIn()
        
        # Use the constructed guest URL instead of original link
        job = linkedin_scraper.scrape_job(guest_url)
        
        # Rest of your comparison logic...
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
        print(f"Error in /api/compare: {e}")
        return jsonify({"error": str(e)}), 500
    
# Upload File to S3
@main.route("/api/upload_resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files or "email" not in request.form:
        return jsonify({"error": "Missing file or email"}), 400

    file = request.files["file"]  # Get file from request
    email = request.form["email"]  # Get email from request

    # Define S3 path: Store resumes under user-specific folders
    s3_path = f"resumes/{email}/{file.filename}"  

    # Upload directly to S3 without saving locally
    success = upload_file_to_s3(file, s3_path)  

    if success:
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_path}"
        return jsonify({"message": "Upload successful", "resume_url": file_url}), 200
    else:
        return jsonify({"error": "Failed to upload file"}), 500

# Fetch the url of a user's resume if it exists
@main.route("/api/get_resume_url", methods=["POST"])
def get_resume_url():
    user_email = request.json.get("email")

    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    file_path = f"resumes/{user_email}/resume.pdf"

    # Generate a presigned URL (this checks if the file exists)
    file_url = generate_presigned_url(file_path)

    if file_url:
        return jsonify({"resumeUrl": file_url}), 200
    else:
        return jsonify({"resumeUrl": None})  # Resume does not exist
