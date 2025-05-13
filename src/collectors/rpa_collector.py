# src/collectors/rpa_collector.py

from .base import BaseCollector, DataRecord
import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any
from src.config.settings import settings
from src.utils.rate_limiter import RateLimiter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RPACollector(BaseCollector):
    # Example configuration
    rpa_config = {
        "pdf_urls": [
            "https://exchange1.com/report.pdf",
            "https://exchange2.com/report.pdf"
        ],
        "exchanges": [{
            "name": "Exchange1",
            "url": "https://exchange1.com/trading",
            "requires_login": True,
            "credentials": {
                "username": "your_username",
                "password": "your_password"
            },
            "login_button_xpath": "//button[@type='submit']",
            "login_success_xpath": "//div[@class='user-profile']",
            "data_selectors": [
                {
                    "name": "btc_volume",
                    "xpath": "//div[@class='trading-volume']"
                },
                {
                    "name": "btc_price",
                    "xpath": "//div[@class='current-price']"
                }
            ]
        }]
    }
    def __init__(self) -> None:
        super().__init__(name="rpa")
        self.rate_limiter = RateLimiter(calls_per_minute=settings.RPA_RATE_LIMIT)
        self.max_retries = 3
        self.retries = 0
        self.driver = None
    
    async def collectPDFReports(self, pdf_urls: List[str]) -> List[DataRecord]:
        """
        Download and extract text from PDF reports
        """
        data_records = []
        for url in pdf_urls:
            try:
                # Using inherited _download_file method
                pdf_content = await self._download_file(url)
                
                # Using inherited _extract_pdf_text method
                text = self._extract_pdf_text(pdf_content)

                data_records.append(
                    DataRecord(
                        source=self.name,
                        data={
                            "type": "pdf_report",
                            "url": url,
                            "content": text,
                            "status": "success"
                        },
                        timestamp=datetime.now(timezone.utc)
                    )
                )
            except Exception as e:
                data_records.append(
                    DataRecord(
                        source=self.name,
                        data={
                            "type": "pdf_report",
                            "url": url,
                            "error": str(e),
                            "status": "failed"
                        },
                        timestamp=datetime.now(timezone.utc)
                    )
                )
        return data_records
    
    async def collectExchangeData(self, exchange_configs: List[Dict[str, Any]]) -> List[DataRecord]:
        """
        Collect data from exchanges using Selenium
        """
        data_records = []
        # Using inherited _setup_selenium method
        self.driver = self._setup_selenium()

        try:
            for config in exchange_configs:
                try:
                    await self.rate_limiter.wait_if_needed()
                    self.driver.get(config["url"])

                    # Handle login if required
                    if config.get("requires_login"):
                        username_elem = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(By.NAME, "username")
                        )
                        password_elem = self.driver.find_element(By.NAME, "password")

                        username_elem.send_keys(config["credentials"]["username"])
                        password_elem.send_keys(config["credentials"]["password"])

                        login_button = self.driver.find_element(By.XPATH, config["login_button_xpath"])
                        login_button.click()

                        # Wait for login to complete
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, config["login_success_xpath"]))
                        )
                    
                    # Extract data using provided selectors
                    for selector in config["data_selectors"]:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, selector["xpath"]))
                        )

                        data_records.append(
                            DataRecord(
                                source=self.name,
                                data={
                                    "type": "exchange_data",
                                    "exchange": config["name"],
                                    "field": selector["name"],
                                    "value": element.text,
                                    "status": "success"
                                },
                                timestamp=datetime.now(timezone.utc)
                            )
                        )
                except Exception as e:
                    data_records.append(
                        DataRecord(
                            source=self.name,
                            data={
                                "type": "exchange_data",
                                "exchange": config["name"],
                                "error": str(e),
                                "status": "failed"
                            },
                            timestamp=datetime.now(timezone.utc)
                        )
                    )
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
        
        return data_records
    
    async def collect(self, config: Dict[str, Any] = None) -> List[DataRecord]:
        """
        Implementation of the base collector interface.
        Requires configuration specifying what to collect.
        """
        if not config:
            raise ValueError("RPA collector requires configuration")
        
        data_records = []

        # Collect PDF reports if configured
        if "pdf_urls" in config:
            pdf_records = await self.collectPDFReports(config["pdf_urls"])
            data_records.extend(pdf_records)
        
        # Collect exchange data if configured
        if "exchanges" in config:
            exchange_records = await self.collectExchangeData(config["exchanges"])
            data_records.extend(exchange_records)
        
        return data_records
    
    def cleanup(self):
        """Cleanup Selenium resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
                        