import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from app.scraper import JobScraper

@pytest.fixture
async def mock_scraper():
    scraper = JobScraper()
    # mock playwright and browser setup
    scraper.playwright = Mock()
    scraper.browser = Mock()
    scraper.context = Mock()
    scraper.page = Mock()
    return scraper

@pytest.mark.asyncio
async def test_init_browser():
    scraper = JobScraper()
    
    with patch('app.scraper.async_playwright') as mock_playwright:
        # setup mock chain
        mock_playwright_instance = Mock()
        mock_playwright.return_value = Mock()
        mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
        mock_chromium = Mock()
        mock_playwright_instance.chromium = mock_chromium
        mock_browser = Mock()
        mock_chromium.launch = AsyncMock(return_value=mock_browser)
        mock_context = Mock()
        mock_browser.new_context = AsyncMock(return_value=mock_context)
        mock_page = Mock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        
        await scraper.init_browser()
        
        # verify browser initialization
        assert scraper.playwright == mock_playwright_instance
        assert scraper.browser == mock_browser
        assert scraper.context == mock_context
        assert scraper.page == mock_page
        
        # verify correct parameters were used
        mock_chromium.launch.assert_called_once_with(headless=True)
        mock_browser.new_context.assert_called_once_with(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )

@pytest.mark.asyncio
async def test_scrape_jobs_successful_extraction(mock_scraper):
    mock_jobs_data = [
        {
            'title': 'Software Engineer',
            'company': 'Tech Corp',
            'location': 'New York, NY',
            'link': 'https://linkedin.com/jobs/1'
        }
    ]
    
    # mock init_browser
    mock_scraper.init_browser = AsyncMock()
    
    # mock cleanup methods
    mock_scraper.context.close = AsyncMock()
    mock_scraper.browser.close = AsyncMock()
    mock_scraper.playwright.stop = AsyncMock()
    
    # mock all the necessary page methods
    mock_scraper.page.goto = AsyncMock()
    mock_scraper.page.wait_for_selector = AsyncMock()
    mock_scraper.page.evaluate = AsyncMock(return_value=mock_jobs_data)
    
    jobs = await mock_scraper.scrape_jobs_async()
    
    assert len(jobs) == 1
    assert jobs[0]['title'] == 'Software Engineer'
    assert jobs[0]['company'] == 'Tech Corp'
    assert jobs[0]['location'] == 'New York, NY'
    assert jobs[0]['link'] == 'https://linkedin.com/jobs/1'

@pytest.mark.asyncio
async def test_scrape_jobs_navigation_error(mock_scraper):
    # simulate navigation error
    mock_scraper.page.goto = Mock(side_effect=Exception("Navigation failed"))
    
    jobs = await mock_scraper.scrape_jobs_async()
    
    assert jobs == []

@pytest.mark.asyncio
async def test_scrape_jobs_selector_timeout(mock_scraper):
    mock_scraper.page.goto = Mock()
    mock_scraper.page.wait_for_selector = Mock(side_effect=Exception("Timeout"))
    
    jobs = await mock_scraper.scrape_jobs_async()
    
    assert jobs == []

@pytest.mark.asyncio
async def test_scrape_jobs_evaluation_error(mock_scraper):
    mock_scraper.page.goto = Mock()
    mock_scraper.page.wait_for_selector = Mock()
    mock_scraper.page.evaluate = Mock(side_effect=Exception("Evaluation failed"))
    
    jobs = await mock_scraper.scrape_jobs_async()
    
    assert jobs == []

@pytest.mark.asyncio
async def test_cleanup_on_error(mock_scraper):
    # mock cleanup methods
    mock_scraper.context.close = AsyncMock()
    mock_scraper.browser.close = AsyncMock()
    mock_scraper.playwright.stop = AsyncMock()
    
    # force an error during scraping
    mock_scraper.init_browser = AsyncMock()
    mock_scraper.page.goto = AsyncMock(side_effect=Exception("Test error"))
    
    await mock_scraper.scrape_jobs_async()
    
    # verify cleanup calls
    assert mock_scraper.context.close.call_count == 1
    assert mock_scraper.browser.close.call_count == 1
    assert mock_scraper.playwright.stop.call_count == 1

def test_scrape_jobs_sync():
    with patch('app.scraper.JobScraper') as MockJobScraper:
        mock_instance = Mock()
        MockJobScraper.return_value = mock_instance
        mock_instance.scrape_jobs_async = Mock(return_value=[])
        
        result = JobScraper.scrape_jobs()
        
        assert result == [] 