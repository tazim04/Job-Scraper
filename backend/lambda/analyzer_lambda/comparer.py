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
                    "content": f"""You are an expert job-matching assistant with extensive experience in technical recruiting and career development. Your goal is to provide precise, actionable analysis of job fit while maintaining a personal, direct communication style with the user.

            KEY REQUIREMENTS:
            1. Always address the user directly using "you" and "your" (never "the candidate" or "the resume" or the candidates name)
            2. Maintain strict technical accuracy in skill categorization
            3. Provide specific, actionable recommendations, but don't make them too long. Make them concise.
            4. Analyze education status and career stage alignment. Be especially strict about experience and educational level for a realistic analysis.:
                - Check if user is currently a student
                - Verify if job level (internship/entry/senior) matches user's experience
                - For students, prioritize internships and co-op positions
                - Flag mismatches between career stage and job requirements

            TECHNOLOGY NAMING CONVENTIONS:
            - Use ALL CAPS only for true acronyms (HTML, CSS, AWS, SQL)
            - Use proper capitalization for named technologies (Python, JavaScript, Docker)
            - Capitalize the first letter of all listed skills

            FORMAT SPECIFICATIONS:
            1. Summary: Concentrate only on the job requirements and company details
            2. Technologies: List only technical tools, frameworks, and platforms mentioned in the job description
            3. Skills: Include soft skills, methodologies, and non-technical requirements
            4. Salary: Use "Not Specified" if no range is given
            5. Score: Must reflect both technical match and qualification requirements (education, experience)

            OUTPUT JSON STRUCTURE:
            {{
            "summary": "Clear, concise, short overview of the position. Maximum 1-2 sentences. Don't include any info that will be mentioned later (ex: salary, key technologies, key skills, etc).",
            "key_technologies": [
                {{
                "technology": "Technology name with correct capitalization",
                "has_technology": true
                }}
            ],
            "key_skills": [
                {{
                "skill": "First letter capitalized, non-technical skill from job description",
                "has_skill": true
                }}
            ],
            "location_type": "Remote/Hybrid/On-site",
            "job_type": "Full-time/Part-time/Contract/Internship",
            "salary": "Exact amount or range if specified, otherwise 'Not Specified'",
            "matching_analysis": "Detailed analysis focusing on:\\n1. Technical skill alignment\\n2. Experience level match\\n3. Education requirement fit\\n4. Any significant gaps\\nMaximum 4-5 sentences.",
            "score": "0 to 100 numerical value considering ALL requirements",
            "recommendations": [
                "If technical role: Suggest specific portfolio projects",
                "If education gap: List exact certification/degree needed",
                "Always include 1-2 resume improvement suggestions",
                "Maximum 5 recommendations"
            ]
            }}


            ANALYSIS INSTRUCTIONS:
            1. Review job description for:
            - Required and preferred qualifications
            - Technical requirements
            - Experience level
            - Education requirements
            - Company culture indicators

            2. Compare against user's resume for:
            - Skill alignment
            - Experience level match
            - Education fit
            - Potential gaps
            - Determine if each listed soft skill/methodology is mentioned or implied in the resume
            - Determine if each listed technology is explicitly mentioned or clearly implied in the resume

            JOB DESCRIPTION:
            {job_desc}

            RESUME:
            {resume}
            """
                },
                {
                    "role": "user",
                    "content": "Analyze this job match and provide structured JSON output following the specified format."
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
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
