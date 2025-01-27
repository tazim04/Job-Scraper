import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
from .models import Job
from .comparer import Comparer
import random

load_dotenv()

class JobScraper:
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

    async def scrape_jobs_async(self):
        print("Starting scrape_jobs_async...")
        jobs: list[Job] = []
        
        # for testing purposes, will handle uploading resumes later
        dummy_resume = """
                        John Doe
                        Aspiring Surgeon
                        123 Main Street, Cityville, ST 12345
                        (555) 123-4567 | john.doe@email.com

                        Objective
                        Highly motivated medical graduate with a passion for surgical excellence and patient care. Seeking to leverage my education and clinical experience to contribute to a dynamic healthcare team while continuing to grow as a surgeon-in-training.

                        Education
                        Doctor of Medicine (M.D.)
                        Cityville Medical School, Cityville, ST
                        Graduated: May 2024

                        Bachelor of Science in Biology
                        University of State, Anytown, ST
                        Graduated: May 2020

                        Clinical Experience
                        Surgical Intern
                        Cityville General Hospital, Cityville, ST
                        May 2024 – Present
                        - Assisted in over 50 surgical procedures, including general surgery, orthopedics, and trauma care.
                        - Monitored post-operative patients, ensuring timely interventions and updates to the surgical team.
                        - Gained proficiency in sterile techniques, suturing, and operating room protocols.

                        Medical Student – Surgery Rotation
                        Cityville Medical School, Cityville, ST
                        July 2023 – December 2023
                        - Observed and assisted in general and specialized surgical cases.
                        - Conducted pre-operative assessments and prepared case reports.
                        - Gained exposure to laparoscopic and minimally invasive surgical techniques.

                        Skills
                        - Surgical Assisting: Suturing, wound management, and instrumentation
                        - Clinical Proficiency: Patient evaluations, diagnostic interpretations, and treatment planning
                        - Research: Authored two research papers on advancements in minimally invasive surgery
                        - Technology: Proficient in EMR systems, surgical robotics, and laparoscopic equipment

                        Certifications
                        - Basic Life Support (BLS)
                        - Advanced Cardiac Life Support (ACLS)
                    """ 

        try:
            print("Initializing browser...")
            await self.init_browser()
            print("Browser initialized")

            print("Navigating to Glassdoor...")
            await self.page.goto(
                'https://www.glassdoor.ca/Job/software-engineer-intern-jobs-SRCH_KO0,23.htm',
                wait_until='networkidle'
            )

            print("Waiting for job cards...")
            await self.page.wait_for_selector('.JobsList_jobsList__lqjTr', timeout=30000)

            print("Getting initial job listings...")

            # Get initial job listings
            raw_jobs = await self.page.evaluate('''() => {
                const cleanText = (text) => {
                    return text?.replace(/\s+/g, ' ')?.trim() || '';
                };

                return Array.from(document.querySelectorAll('.JobsList_jobListItem__wjTHv')).map(card => {
                    if (card.classList.contains('JobsList_noop___gffo')) {
                        return null;
                    }

                    const titleElem = card.querySelector('.JobCard_jobTitle__GLyJ1');
                    const companyElem = card.querySelector('.EmployerProfile_compactEmployerName__9MGcV');
                    const locationElem = card.querySelector('.JobCard_location__Ds1fM');
                    const salaryElem = card.querySelector('.JobCard_salaryEstimate__QpbTW');
                    const dateElem = card.querySelector('.JobCard_listingAge__jJsuc');
                    const linkElem = card.querySelector('a[data-test="job-link"]');

                    return {
                        title: cleanText(titleElem?.innerText),
                        company: cleanText(companyElem?.innerText),
                        location: cleanText(locationElem?.innerText),
                        salary: cleanText(salaryElem?.innerText),
                        date_posted: cleanText(dateElem?.innerText),
                        link: linkElem?.href,
                        cardId: card.getAttribute('data-jobid')
                    };
                }).filter(job => job !== null && job.title && job.company);
            }''')

            # for each job card, click it and get additional details
            for job in raw_jobs:
                print(f"Processing job: {job['title']} at {job['company']}")

                try:
                    await self.page.wait_for_timeout(500)
                    await self.page.wait_for_timeout(random.randint(1000, 3000))  # Random delay
                    card_selector = f'.JobsList_jobListItem__wjTHv[data-jobid="{job["cardId"]}"]'
                    await self.page.wait_for_selector(card_selector, timeout=5000)
                    await self.page.click(card_selector)

                    await self.page.wait_for_selector('.JobDetails_jobDescription__uW_fK', timeout=5000)

                    print(f"Reading details for {job['title']} at {job['company']}")
                    details = await self.page.evaluate('''() => {
                        const cleanText = (text) => {
                            return text?.replace(/\s+/g, ' ')?.trim() || '';
                        };

                        const descElem = document.querySelector('.JobDetails_jobDescription__uW_fK');

                        return {
                            description: cleanText(descElem?.innerText),
                        };
                    }''')
                    
                    # print(f"Job description: {job['description']}")
                    
                    # Add retries for loading job details
                    for _ in range(3):  # Retry up to 3 times
                        try:
                            await self.page.wait_for_selector('.JobDetails_jobDescription__uW_fK', timeout=10000)
                            break
                        except Exception:
                            print("Retrying to load job details...")
                            await self.page.reload()

                    job.update(details)

                except Exception as e:
                    print(f"Error getting details for job {job['title']}: {e}")
                    continue

                if job['title'] and job['company']:
                    analysis = self.comparer.compare_resume_to_job(dummy_resume, job['description'])
                    job['matching_analysis'] = analysis["matching_analysis"]
                    job['summary'] = analysis["summary"]
                    job['score'] = analysis["score"]
                    job['recommendation'] = analysis["recommendation"]
                    

                    jobs.append(Job(**job))

        except Exception as e:
            print(f"Error scraping jobs: {e}")

        finally:
            print(f"Scraped {len(jobs)} jobs")
            if hasattr(self, 'context') and self.context:
                await self.context.close()
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()

        return [job.to_dict() for job in jobs]

    @classmethod
    def scrape_jobs(cls):
        print("Creating scraper instance...")
        scraper = cls()
        print("Scraper instance created")
        print("Starting async scraping...")
        try:
            return asyncio.run(scraper.scrape_jobs_async())
        except Exception as e:
            print(f"Error in scrape_jobs: {e}")
            return []

# function to be imported by routes.py
def scrape_jobs():
    return JobScraper.scrape_jobs()
