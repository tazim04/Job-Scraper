from flask import Blueprint, jsonify, request
from .scrapers.glassdoor_scraper import JobScraperGlassdoor
from .comparer import Comparer
import nest_asyncio
import os
import json
from .aws_config import s3_client, AWS_BUCKET_NAME
from botocore.exceptions import ClientError


nest_asyncio.apply() # apply nest_asyncio to allow asyncio to work with sync code

main = Blueprint('main', __name__) # create a blueprint for the main route
glassdoor_scraper = JobScraperGlassdoor
comparer = Comparer()

# change this to work with s3 buckets later 
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Navigate to the project root
resume_path = os.path.join(base_dir, "Resume - Tazim Khan.pdf")

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
    
# Upload File to S3
@main.route("/api/upload_resume", methods=["POST"])
def upload_resume():
    print("upload_resume()")
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Get file and user's email from request
    file = request.files["file"]
    user_email = request.form.get("email")

    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    file_path = f"resumes/{user_email}/resume.pdf"

    try:
        s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_path, ExtraArgs={"ContentType": file.content_type})

        file_url = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file_path}"
        print(f"file_url: {file_url}")
        return jsonify({"resumeUrl": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Fetch File from S3

# Fetch the url of a user's resume if it exists
@main.route("/api/get_resume_url", methods=["POST"])
def get_resume_url():
    user_email = request.json.get("email")
    
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    file_path = f"resumes/{user_email}/resume.pdf"
    
    try:
        # Generate a presigned URL (checks if file exists)
        response = s3_client.head_object(Bucket=AWS_BUCKET_NAME, Key=file_path)

        # If the file exists, construct the URL
        file_url = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file_path}"
        return jsonify({"resumeUrl": file_url}), 200
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return jsonify({"resumeUrl": None})  # Resume does not exist
        return jsonify({"error": str(e)}), 500
