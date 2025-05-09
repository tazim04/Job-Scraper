import asyncio
from playwright.async_api import async_playwright
from models import Job

class JobScraperLinkedIn:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        print("Initialized LinkedIn scraper")

    async def init_browser(self):
        try:
            print("Starting playwright...")
            self.playwright = await async_playwright().start()
            print("Launching chromium...")
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args = [
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--no-zygote",
                    "--disable-accelerated-2d-canvas",
                    "--disable-background-networking",
                    "--disable-renderer-backgrounding",
                    "--disable-sync",
                    "--metrics-recording-only",
                    "--mute-audio",
                    "--no-first-run",
                    "--disable-popup-blocking",
                    "--disable-default-apps",
                    "--disable-features=AudioServiceOutOfProcess",
                    "--hide-scrollbars",
                    "--autoplay-policy=user-gesture-required",
                    "--use-gl=swiftshader",
                    "--single-process",
                    "--disable-extensions"
                ]
            )
            print("Creating new context...")
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            )
            print("Opening new page...")
            self.page = await self.context.new_page()
            print("Browser ready!")
        except Exception as e:
            print(f"Browser initialization failed: {e}")
            await self.cleanup()
            raise

    async def scrape_job_async(self, link):
        try:
            await self.init_browser()
            print(f"Navigating to LinkedIn job page: {link}")
            
            # Add timeout handling for navigation
            try:
                await self.page.goto(link, wait_until='domcontentloaded', timeout=15000)
            except Exception as e:
                print(f"Navigation error: {e}")
                return None

            # Handle potential authwalls
            if "authwall" in self.page.url:
                print("Hit LinkedIn authwall")
                return None

            # Add more robust waiting
            try:
                await self.page.wait_for_selector('.top-card-layout__title, h1', timeout=15000)
            except Exception as e:
                print(f"Failed to find main content: {e}")
                return None

            job_details = await self.page.evaluate('''() => {
                try {
                    const cleanText = (text) => text ? text.replace(/\\s+/g, ' ').trim() : '';
                    
                    const safeQuery = (selector, attr = 'textContent') => {
                        const el = document.querySelector(selector);
                        return el ? (el[attr] || '').trim() : '';
                    };

                    // Main job details
                    const title = safeQuery('.top-card-layout__title') || safeQuery('h1');
                    const company = safeQuery('.topcard__org-name-link') || safeQuery('.topcard__flavor--black-link');
                    const location = safeQuery('.topcard__flavor--bullet') || safeQuery('.job-search-card__location');
                    const date_posted = safeQuery('.posted-time-ago__text') || safeQuery('time');

                    // Get raw HTML of description
                    let description = '';
                    const descriptionContainer = document.querySelector('.show-more-less-html__markup');
                    if (descriptionContainer) {
                        description = descriptionContainer.innerHTML;
                    }

                    return {
                        title: cleanText(title),
                        company: cleanText(company),
                        location: cleanText(location),
                        date_posted: cleanText(date_posted),
                        description: description // Keep raw HTML
                    };
                } catch (e) {
                    console.error('Evaluation error:', e);
                    return null;
                }
            }''')

            if not job_details:
                print("Failed to extract job details")
                return None

            print(f"Exctracted details: {job_details}")

            return Job(
                title=job_details.get('title') or 'N/A',
                company=job_details.get('company') or 'N/A',
                location=job_details.get('location') or 'N/A',
                link=link,
                date_posted=job_details.get('date_posted') or '',
                description=job_details.get('description') or '',
                # Additional fields to be added by groq api
                summary=None,
                key_technologies=None,
                key_skills=None,
                location_type=None,
                job_type=None,
                salary=None,
                matching_analysis=None,
                score=None,
                recommendations=None
            )

        except Exception as e:
            print(f"Error scraping LinkedIn job: {e}")
            return None
        finally:
            await self.cleanup()

    async def cleanup(self):
        if self.context: await self.context.close()
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()

    @classmethod
    def scrape_job(cls, link):
        scraper = cls()
        return asyncio.run(scraper.scrape_job_async(link))

def scrape_linkedin_job(link):
    return JobScraperLinkedIn.scrape_job(link)