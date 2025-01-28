import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
from ..models import Job
from ..comparer import Comparer

load_dotenv()

class JobScraperGlassdoor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.comparer = Comparer()

        print("Initialized scraper")

    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)  # use chromium browser
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        )
        self.page = await self.context.new_page()

    # scrape job
    async def scrape_job_async(self):
        print("Starting scrape_current_open_job...")
        try:
            print("Initializing browser...")
            await self.init_browser()
            print("Browser initialized")

            print("Navigating to Glassdoor...")
            await self.page.goto(
                'https://www.glassdoor.ca/Job/ottawa-on-canada-health-care-jobs-SRCH_IL.0,16_IC2286068_KO17,28.htm',
                wait_until='networkidle'
            )

            print("Waiting for job details panel...")
            # Wait for the job details panel on the right to load
            await self.page.wait_for_selector('.TwoColumnLayout_jobDetailsContainer__qyvJZ', timeout=30000, state="visible")

            print("Extracting job ID from the open job panel...")
            # Extract the job ID from the open job on the right
            open_job_id = await self.page.evaluate('''() => {
                const openJobContainer = document.querySelector('.TwoColumnLayout_jobDetailsContainer__qyvJZ');
                if (!openJobContainer) return null;
                const jobIdElem = openJobContainer.querySelector('[id^="job-viewed-waypoint-"]');
                if (!jobIdElem) return null;
                return jobIdElem.id.replace('job-viewed-waypoint-', '');
            }''')

            if not open_job_id:
                print("No open job found.")
                return []

            print(f"Open Job ID: {open_job_id}")

            print("Extracting job details...")
            # Extract job details primarily from the right-side job panel
            job_details = await self.page.evaluate(f'''
                () => {{
                    const cleanText = (text) => text?.replace(/\\s+/g, ' ')?.trim() || '';

                    // Extract details from the right-side job panel
                    const titleElem = document.querySelector('.heading_Level1__soLZs');
                    const companyElem = document.querySelector('.EmployerProfile_employerNameContainer__ptolz h4');
                    const locationElem = document.querySelector('.JobDetails_location__mSg5h');
                    const salaryElem = document.querySelector('.SalaryEstimate_salaryRange__brHFy');
                    const descriptionElem = document.querySelector('.JobDetails_jobDescription__uW_fK');

                    return {{
                        title: cleanText(titleElem?.innerText),
                        company: cleanText(companyElem?.innerText),
                        location: cleanText(locationElem?.innerText),
                        salary: cleanText(salaryElem?.innerText),
                        description: cleanText(descriptionElem?.innerText)
                    }};
                }}
            ''')

            # If job_details is invalid, stop further execution
            if not job_details or not job_details.get('title') or not job_details.get('company'):
                print("Failed to extract job details from the right panel.")
                return []

            # Extract additional details like link and date_posted from the left-side job card
            left_panel_data = await self.page.evaluate(f'''
                () => {{
                    const cleanText = (text) => text?.replace(/\\s+/g, ' ')?.trim() || '';
                    const jobCardElem = document.querySelector('.JobsList_jobListItem__wjTHv[data-jobid="{open_job_id}"]');
                    if (!jobCardElem) return null;

                    // Extract link and date_posted from the left-side job card
                    const linkElem = jobCardElem.querySelector('.JobCard_jobTitle__GLyJ1[data-test="job-title"]'); // Job link
                    const datePostedElem = jobCardElem.querySelector('.JobCard_listingAge__jJsuc[data-test="job-age"]'); // Date posted

                    return {{
                        link: linkElem ? linkElem.href : null,   // Extract href from the link element
                        date_posted: cleanText(datePostedElem?.innerText) // Include date posted
                    }};
                }}
            ''')

            # Merge the extracted details
            if left_panel_data:
                job_details.update(left_panel_data)

            # Map job details to the Job model
            try:
                job = Job(
                    title=job_details.get('title'),
                    company=job_details.get('company'),
                    location=job_details.get('location'),
                    link=job_details.get('link'), 
                    salary=job_details.get('salary'),
                    date_posted=job_details.get('date_posted'),
                    description=job_details.get('description'),
                    # Additional fields to be added by groq api
                    summary=None,
                    key_technologies=None,
                    key_skills=None,
                    location_type=None,
                    job_type=None,
                    matching_analysis=None,
                    score=None,
                    recommendations=None
                )
            except Exception as e:
                print(f"Error mapping job details to Job model: {e}")
                return []

            print(f"Successfully created Job model instance: {job}")
            return job  # Return the job as an object

        except Exception as e:
            print(f"Error scraping the current open job: {e}")
            return []

        finally:
            if hasattr(self, 'context') and self.context:
                await self.context.close()
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()



    @classmethod
    def scrape_job(cls):
        print("Creating scraper instance...")
        scraper = cls()
        print("Scraper instance created")
        print("Starting async scraping...")
        try:
            return asyncio.run(scraper.scrape_job_async())
        except Exception as e:
            print(f"Error in scrape_jobs: {e}")
            return []

# Function to be imported by routes.py
def scrape_job():
    return JobScraperGlassdoor.scrape_job()
