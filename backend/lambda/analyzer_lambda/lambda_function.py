import json
import re
import os
from urllib.parse import urlparse, parse_qs
from analyzer_lambda.linkedin_scraper import JobScraperLinkedIn
from analyzer_lambda.comparer import Comparer

comparer = Comparer()

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        resume_path = body.get("resume_path")
        original_link = body.get("link")

        if not resume_path or not original_link:
            return response(400, {"error": "Missing resume_path or link"})

        # Extract job ID from LinkedInURL
        parsed = urlparse(original_link)
        query_params = parse_qs(parsed.query)
        job_id = query_params.get('currentJobId', [None])[0]

        if not job_id:
            path_match = re.search(r'/jobs/view/(\d+)', parsed.path)
            if path_match:
                job_id = path_match.group(1)

        if not job_id:
            return response(400, {"error": "Could not extract job ID from URL"})

        # Construct guest URL
        guest_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

        # Scrape job data from guest URL
        scraper = JobScraperLinkedIn()
        job = scraper.scrape_job(guest_url)

        # Comparison analysis
        groq_res = comparer.compare(resume_path, job.description)

        if isinstance(groq_res, str):
            groq_res = json.loads(groq_res)

        job.summary = groq_res.get("summary")
        job.key_technologies = groq_res.get("key_technologies")
        job.key_skills = groq_res.get("key_skills")
        job.location_type = groq_res.get("location_type")
        job.job_type = groq_res.get("job_type")
        job.salary = groq_res.get("salary")
        job.matching_analysis = groq_res.get("matching_analysis")
        job.score = groq_res.get("score")
        job.recommendations = groq_res.get("recommendations")

        return response(200, job.to_dict())

    except Exception as e:
        print("ERROR:", e)
        return response(500, {"error": str(e)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }