# src/collectors/base.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import aiohttp
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import PyPDF2
import io

@dataclass
class DataRecord:
    """Standard format for all collected data"""
    source: str
    data: Dict[str, Any]
    timestamp: datetime 
    id: Optional[int] = None

class BaseCollector:
    """Template for all collectors"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(name)

    async def collect(self) -> List[DataRecord]:
        """Must be implemented by each collector"""
        raise NotImplementedError("Subclasses must implement collect()")
    
    async def _make_api_request(self, url: str, headers: Optional[Dict] = None) -> Dict:
        """Make an async API request"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}")
                return await response.json()
            
    async def _scrape_webpage(self, url: str) -> BeautifulSoup:
        """Scrape webpage content"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Web scraping failed with status {response.status}")
                html = await response.text()
                return BeautifulSoup(html, 'html.parser')
    
    def _setup_selenium(self) -> webdriver.Chrome:
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        return webdriver.Chrome(options=chrome_options)
    
    async def _download_file(self, url: str) -> bytes:
        """Download file content"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"File download failed with status {response.status}")
                return await response.read()
            
    def _extract_pdf_text(self, pdf_content: bytes) -> str:
        """Extract text from PDF content"""
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    async def _submit_form(self, url: str, data: Dict[str, Any]) -> Dict:
        """Submit form data"""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status != 200:
                    raise Exception(f"Form submission failed with status {response.status}")
                return await response.json()
            
    def cleanup(self):
        """Cleanup resources"""
        pass