import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

class Comparer:
    def __init__(self):
        self.client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
        
        # Extract resume text from pdf
    def extract_text_from_pdf(self, file_path):
        reader = PdfReader(file_path)
        return "".join(page.extract_text() for page in reader.pages)

    # Compare the users resume to the scraped job description
    def compare(self, resume_path, job_desc):
        resume = self.extract_text_from_pdf(resume_path)
        # Validate inputs
        if not job_desc.strip() or not resume.strip():
            raise ValueError("Job description or resume is empty.")

        print(f"Job Desc: {job_desc[:500]}...")  # Log first 500 characters
        print(f"Resume: {resume[:500]}...")  # Log first 500 characters

        # Format prompt using f-string with escaped braces for JSON
        chat_completion = self.client.chat.completions.create(
            # Main prompt for the model
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are an expert job-matching assistant specializing in comparing resumes with job descriptions. Your task is to determine how well a candidate’s resume matches a given job description based on skills, experience, qualifications, and other relevant factors.

                    ---

                    ### **Instructions**:
                    1. Carefully read the **Job Description** and **Resume** provided below.
                    2. Analyze the overlap between the candidate’s skills, experience, and qualifications with the job requirements, with particular attention to **technologies mentioned**, such as programming languages, cloud platforms, databases, frameworks, tools, and other technical skills.
                    3. DO NOT refer to the user or their resume as "the candidate" or "the resume". If you want to refer to the user's resume, skills, etc, talk to them directly. For example: "Your resume..." or "You have a strong technical background...". Always talk DIRECTLY to the user.
                    4. Provide the following outputs in strict JSON format:

                    #### **Outputs from the Analysis**:
                    ```json
                    {{
                        "summary": "A very concise, high-level overview of the job and its requirements. No need to include any matching analysis here, just focus on the job itself.",
                        "key_technologies": ["Technology1", "Technology2", "Technology3, ..."], // Mentioned tech in the job description, NOT from the resume
                        "key_skills": ["Skill1", "Skill2", "Skill3, ..."], // Mentioned skills in the job description, NOT from the resume
                        "location_type": "Remote/In-person/Hybrid",
                        "job_type": "Internship/Full-Time/Part-Time/etc
                        "matching_analysis": "Detailed explanation of alignment and mismatches, focusing on technical skills and experience. If there is a mismatch or missing form of education required, make sure to mention that as a big factor.",
                        "score": 85,
                        "recommendations": ["Recommendation1", "Recommendation2", "Recommendation3, ... "] // If the job description is a tech/engineering based job, ensrue to provide recomended personal projects the user can do and add to their resume. If there was missing educatino you mentioned for the matching_analysis, you shoud list it here as a key recommendation. You can also give tips for improving the resume itself.
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
        
    def test(self):
        job_desc = """
Job Title: Family Medicine Doctor (Licensed in Ontario) - Educated in Canada - Business Development Consultant for Virtual Therapy Group

Company: RewPaz, Inc.
Location: Remote (Ontario-based)
Job Type: Part-time, Contract, Consultant (Case-by-Case)
Compensation: Competitive, based on experience (Retainer or Hourly)

About Us: RewPaz, Inc. is a growing teletherapy platform that offers virtual mental health services across Canada. We are seeking a qualified and licensed Family Medicine Doctor in Ontario to join us as a Business Development Consultant. In this role, you will provide critical expertise in virtual healthcare practices and assist in client meetings. This is a flexible, part-time consulting position where you will help shape the direction of an early-stage company trying to disrupt big-name virtual care providers in the mental health space. We expect total consulting hours not to exceed a few hours per month.

Key Responsibilities:

● Act as the face of RewPaz in client and stakeholder meetings, offering clinical credibility and expertise.

● Provide expert advice on virtual healthcare practices and compliance in Ontario and across Canada.

● Engage with clients on a case-by-case basis to answer clinical questions and guide the development of services.

● Advise on regulatory and operational matters specific to virtual healthcare in Ontario.

● Support business development initiatives by contributing medical insights to strategy discussions.

● Offer feedback on the RewPaz platform to ensure clinical applicability and ease of use for patients and therapists.

Qualifications:

● Licensed Family Medicine Doctor in Ontario.

● Experience with virtual healthcare or telemedicine services.

● Strong communication and interpersonal skills, with the ability to convey medical knowledge to a non-medical audience.

● Previous consulting or business development experience in healthcare is a plus.

Why Join RewPaz?

● Flexible, remote work with a minimal time commitment—ideal for a physician seeking a side role.

● Opportunity to shape the future of virtual therapy in Canada.

● Competitive compensation package, with pay structured on either a retainer or hourly basis.

How to Apply: To apply, please submit your resume and a brief cover letter outlining your experience with virtual healthcare and business development, as well as salary expectation (per hour). Include whether you would be willing to join in-person meetings, should those arise (in the Toronto area). Applications can be sent to Texia at admin@rewpaz.ca.

RewPaz, Inc. is committed to diversity and inclusion in the workplace. We encourage all qualified candidates, regardless of gender, race, or background, to apply.

Job Type: Freelance

Pay: $90.00-$100.00 per hour

Benefits:

Flexible schedule
Schedule:

Monday to Friday
Education:

Doctoral Degree (preferred)
Work Location: On the road
        """
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Navigate to the project root
        resume_path = os.path.join(base_dir, "Resume - Tazim Khan.pdf")
        
        return self.compare(resume_path, job_desc)