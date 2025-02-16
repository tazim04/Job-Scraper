import os
import tempfile
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
import requests

load_dotenv()

class Comparer:
    def __init__(self):
        self.client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
        
    # download resume from s3
    def download_file_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            # Create a temporary file to store the downloaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(response.content)
                return temp_file.name
        except Exception as e:
            print(f"Error downloading file from URL: {e}")
            raise
        
        # Extract resume text from pdf
    def extract_text_from_pdf(self, file_path):
        reader = PdfReader(file_path)
        return "".join(page.extract_text() for page in reader.pages)

    # Compare the users resume to the scraped job description
    def compare(self, resume_url, job_desc):
        """Compare the user's resume to the scraped job description."""
        try:
            # Download the resume from the presigned URL
            local_resume_path = self.download_file_from_url(resume_url)
            
            # Extract text from the downloaded PDF
            resume = self.extract_text_from_pdf(local_resume_path)
            
            # Clean up the temporary file
            os.unlink(local_resume_path)

            # Validate inputs
            if not job_desc.strip() or not resume.strip():
                raise ValueError("Job description or resume is empty.")

            print(f"Job Desc: {job_desc[:500]}...")  # Log first 500 characters
            print(f"Resume: {resume[:500]}...")  # Log first 500 characters

            # Format prompt using f-string with escaped braces for JSON
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                        You are an expert job-matching assistant specializing in comparing resumes with job descriptions. Your task is to determine how well a candidate’s resume matches a given job description based on skills, experience, qualifications, and other relevant factors. Ensure any lists like skills always have the first letter for each listed item capitalized. Any key technologies that should be all caps (HTML, CSS, etc) make them all caps, BUT this does not mean make all technologies all caps, if a technology is not an achronym but a name (Java, Python, TypeScript, etc) then use regular capitilization. Salary can be set or a range. If the salary or range isn't specified just put "Not Specified".

                        ---

                        ### **Instructions**:
                        1. Carefully read the **Job Description** and **Resume** provided below.
                        2. Analyze the overlap between the candidate’s skills, experience, and qualifications with the job requirements, with particular attention to **technologies mentioned**, such as programming languages, cloud platforms, databases, frameworks, tools, and other technical skills. Ensure the listed technologies are actually technologies and mistakenly other things like plain words found in the description.
                        3. DO NOT refer to the user or their resume as "the candidate" or "the resume". If you want to refer to the user's resume, skills, etc, talk to them directly. For example: "Your resume..." or "You have a strong technical background...". Always talk DIRECTLY to the user.
                        4. Provide the following outputs in strict JSON format:

                        #### **Outputs from the Analysis**:
                        ```json
                        {{
                            "summary": "A very concise, high-level overview of the job and its requirements. No need to include any matching analysis here, just focus on the job itself.",
                            "key_technologies": ["Technology1", "Technology2", "Technology3, ..."], // Mentioned tech in the job description, NOT from the resume
                            "key_skills": ["Skill1", "Skill2", "Skill3, ..."], // Mentioned skills in the job description, NOT from the resume
                            "location_type": "Remote/In-person/Hybrid",
                            "job_type": "Internship/Full-Time/Part-Time/etc,
                            "salary": "$141,500 - $212,300"
                            "matching_analysis": "Detailed explanation of alignment and mismatches, focusing on technical skills and experience. If there is a mismatch or missing form of education required, make sure to mention that as a big factor.",
                            "score": 85,
                            "recommendations": ["Recommendation1", "Recommendation2", "Recommendation3, ... "] // If the job description is a tech/engineering based job, ensure to provide recomended personal projects the user can do and add to their resume. If there was missing educatino you mentioned for the matching_analysis, you shoud list it here as a key recommendation. You can also give tips for improving the resume itself.
                        }}
                        ```

                        ---

                        ### **Job Description**:
                        {job_desc}

                        ### **Candidate Resume**:
                        {resume}
                        """
                    },
                    {
                        "role": "user",
                        "content": "Provide the JSON output for the given resume and job description.",
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}  # Enables JSON mode
            )

            # Handle API response
            try:
                res = chat_completion.choices[0].message.content
                return res
            except (KeyError, IndexError) as e:
                raise ValueError("The response from the API was not as expected.") from e

        except Exception as e:
            print(f"Error in compare method: {e}")
            raise
