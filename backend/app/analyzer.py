from huggingface_hub import InferenceApi
import os
import json


class JobAnalyzer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobAnalyzer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        print("Initializing JobAnalyzer with Hugging Face Inference API...")

        huggingface_api_token = os.getenv("HUGGINGFACE_TOKEN")
        if not huggingface_api_token:
            raise ValueError("The Hugging Face API token is not set. Please set the environment variable `HUGGINGFACE_TOKEN`.")

        # initialize fine tuned model from hugging face
        self.matching_model = InferenceApi(
            repo_id="LlamaFactoryAI/cv-job-description-matching",
            token=huggingface_api_token
        )

        print("Hugging Face model for matching initialized.")
        self._initialized = True

    def compare_resume_to_job(self, resume: str, job_description: str):
        """
        Compare a resume to a job description and return a confidence score for match.
        """
        try:
            print("Comparing resume to job description...")
            input_payload = f"""
                Analyze the compatibility between the following CV and job description.

                CV:
                {resume}

                Job Description:
                {job_description}

                Your task is to output a structured JSON format with the following:
                1. matching_analysis: Analyze the CV against the job description to identify key strengths and gaps.
                2. summary: Summarize the relevance of the CV to the job description in a few concise sentences.
                3. score: Provide a numerical compatibility score (0-100) based on qualifications, skills, and experience.
                4. recommendation: Suggest actions for the candidate to improve their match or readiness for the role.

                Output the result in JSON format.
            """
            response = self.matching_model(inputs=input_payload)
            
            # Parse the response
            if isinstance(response, dict):
                print("Raw API response:", response)
                return {
                    "matching_analysis": response.get("matching_analysis", "No analysis available."),
                    "summary": response.get("summary", "No summary available."),
                    "score": response.get("score", 0),
                    "recommendation": response.get("recommendation", "No recommendations available."),
                }
            else:
                print("Unexpected API response format:", response)
                return {
                    "matching_analysis": "Unexpected response format.",
                    "summary": "",
                    "score": 0,
                    "recommendation": "",
                }

        except Exception as e:
            print(f"Error comparing resume to job description: {e}")
            return {
                "matching_analysis": "Error occurred.",
                "summary": "",
                "score": 0,
                "recommendation": "",
            }
