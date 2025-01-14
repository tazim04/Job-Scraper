import asyncio
from playwright.async_api import async_playwright

class JobScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True) # use chromium browser
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            java_script_enabled=True,
            ignore_https_errors=True
        )
        self.page = await self.context.new_page()

    async def scrape_jobs_async(self):
        jobs = [] # list of jobs to return
        try:
            await self.init_browser() # initialize browser
            
            print("Navigating to LinkedIn...")
            # scraping linkedin jobs (change location to match users requested location)
            await self.page.goto('https://www.linkedin.com/jobs/search?')
            
            print("Waiting for job cards...")
            try:
                await self.page.wait_for_selector('.job-card-container', 
                                                timeout=120000,
                                                state='visible')
            except Exception as e:
                print(f"Error waiting for job cards: {e}")
                # Try an alternative selector
                await self.page.wait_for_selector('[data-job-id]', 
                                                timeout=120000,
                                                state='visible')
            
            # Add a small delay to ensure content is loaded
            await self.page.wait_for_timeout(2000)
            
            print("Extracting job data...")
            
            # scroll to load more jobs (optional)
            # for _ in range(3):
            #     await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            #     await self.page.wait_for_timeout(1000)  # wait for 1 second
            
            # extract job data
            jobs = await self.page.evaluate('''() => {
                const jobCards = document.querySelectorAll('.job-card-container');
                return Array.from(jobCards).map(card => ({
                    title: card.querySelector('.job-card-list__title')?.innerText?.trim(),
                    company: card.querySelector('.job-card-container__company-name')?.innerText?.trim(),
                    location: card.querySelector('.job-card-container__metadata-item')?.innerText?.trim(),
                    link: card.querySelector('.job-card-list__title')?.href,
                }));
            }''')

        except Exception as e:
            print(f"Error scraping jobs: {e}")
            
        finally:
            # safely close all resources
            if hasattr(self, 'context') and self.context:
                await self.context.close()
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
            
        return jobs

# function to scrape jobs (used in routes.py)
def scrape_jobs():
    scraper = JobScraper() # create an instance of JobScraper class
    return asyncio.get_event_loop().run_until_complete(scraper.scrape_jobs_async()) # run the async function