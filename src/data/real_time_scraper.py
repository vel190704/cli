"""
Real-time financial data scraper for oil & gas companies
Retrieves actual financial data from official sources
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import trafilatura
from config import Config

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class RealTimeFinancialScraper:
    """Scrapes real-time financial data from official company sources."""
    
    def __init__(self):
        """Initialize the scraper with company data sources."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Official financial data sources
        self.company_sources = {
            "Shell": {
                "earnings_url": "https://www.shell.com/investors/financial-information/quarterly-results.html",
                "investor_relations": "https://www.shell.com/investors.html",
                "symbol": "SHEL",
                "exchange": "NYSE"
            },
            "BP": {
                "earnings_url": "https://www.bp.com/en/global/corporate/investors/results-and-reporting.html",
                "investor_relations": "https://www.bp.com/en/global/corporate/investors.html",
                "symbol": "BP",
                "exchange": "NYSE"
            },
            "ExxonMobil": {
                "earnings_url": "https://corporate.exxonmobil.com/investors/investor-relations/quarterly-earnings",
                "investor_relations": "https://corporate.exxonmobil.com/investors",
                "symbol": "XOM",
                "exchange": "NYSE"
            },
            "Chevron": {
                "earnings_url": "https://www.chevron.com/investors/quarterly-earnings",
                "investor_relations": "https://www.chevron.com/investors",
                "symbol": "CVX", 
                "exchange": "NYSE"
            }
        }
    
    def get_company_financial_data(self, company: str) -> Dict[str, Any]:
        """Get real financial data for a specific company."""
        try:
            if company not in self.company_sources:
                logger.error(f"Company {company} not supported")
                return {}
            
            company_info = self.company_sources[company]
            
            # Try to get earnings data from official source
            earnings_data = self._scrape_earnings_page(company, company_info["earnings_url"])
            
            # Enhance with market data if possible
            market_data = self._get_basic_market_data(company_info["symbol"])
            
            # Combine all data
            financial_data = {
                "company": company,
                "symbol": company_info["symbol"],
                "exchange": company_info["exchange"],
                "data_source": "official_website",
                "scraped_at": datetime.now().isoformat(),
                **earnings_data,
                **market_data
            }
            
            logger.info(f"Successfully scraped financial data for {company}")
            return financial_data
            
        except Exception as e:
            logger.error(f"Error scraping data for {company}: {e}")
            return {}
    
    def _scrape_earnings_page(self, company: str, url: str) -> Dict[str, Any]:
        """Scrape earnings information from company's official page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Use trafilatura to extract clean text content
            text_content = trafilatura.extract(response.content)
            
            if not text_content:
                # Fallback to BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()
            
            # Extract financial metrics from text content
            extracted_data = self._extract_financial_metrics(text_content, company)
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error scraping earnings page for {company}: {e}")
            return {}
    
    def _extract_financial_metrics(self, text_content: str, company: str) -> Dict[str, Any]:
        """Extract financial metrics from scraped text content."""
        import re
        
        metrics = {}
        text_lower = text_content.lower()
        
        # Common financial metric patterns
        patterns = {
            'revenue': [
                r'revenue[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)',
                r'total revenue[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)',
                r'sales[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)'
            ],
            'net_income': [
                r'net income[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)',
                r'net earnings[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)',
                r'profit[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)'
            ],
            'free_cash_flow': [
                r'free cash flow[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)',
                r'operating cash flow[:\s]+\$?([0-9,]+\.?[0-9]*)\s*(million|billion|m|b)'
            ],
            'production': [
                r'production[:\s]+([0-9,]+\.?[0-9]*)\s*(thousand|million|k|m)?\s*(boe|barrels|bpd)',
                r'oil production[:\s]+([0-9,]+\.?[0-9]*)\s*(thousand|million|k|m)?\s*(boe|barrels|bpd)'
            ]
        }
        
        for metric, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        value = float(match.group(1).replace(',', ''))
                        unit = match.group(2).lower() if len(match.groups()) > 1 else ''
                        
                        # Convert to standard units (millions)
                        if unit in ['billion', 'b']:
                            value *= 1000
                        elif unit in ['thousand', 'k']:
                            value /= 1000
                        
                        metrics[metric] = value
                        break
                    except (ValueError, IndexError):
                        continue
        
        # Add metadata
        current_date = datetime.now()
        quarter = f"Q{((current_date.month - 1) // 3) + 1}"
        
        metrics.update({
            'report_type': 'quarterly',
            'quarter': quarter,
            'year': current_date.year,
            'report_date': current_date.strftime("%Y-%m-%d"),
            'data_quality': 'scraped_official'
        })
        
        return metrics
    
    def _get_basic_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get basic market data for stock symbol."""
        try:
            # This is a simplified approach - in production you'd use a proper financial API
            # For now, return empty dict as we focus on scraped financial data
            return {
                'market_data_available': False,
                'note': 'Market data requires financial API integration'
            }
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return {}
    
    def update_all_companies(self) -> Dict[str, Dict[str, Any]]:
        """Update financial data for all tracked companies."""
        all_data = {}
        
        for company in self.company_sources.keys():
            logger.info(f"Updating financial data for {company}")
            company_data = self.get_company_financial_data(company)
            if company_data:
                all_data[company] = company_data
        
        return all_data
    
    def get_company_news_sentiment(self, company: str) -> Dict[str, Any]:
        """Get recent news and sentiment for company."""
        try:
            company_info = self.company_sources.get(company, {})
            if not company_info:
                return {}
            
            # Scrape investor relations page for recent news
            ir_url = company_info.get("investor_relations", "")
            if ir_url:
                response = self.session.get(ir_url, timeout=10)
                response.raise_for_status()
                
                text_content = trafilatura.extract(response.content)
                
                # Basic sentiment analysis based on keywords
                positive_keywords = ['growth', 'increase', 'strong', 'improved', 'profit', 'positive', 'success']
                negative_keywords = ['decline', 'decrease', 'weak', 'loss', 'negative', 'challenge', 'concern']
                
                text_lower = text_content.lower() if text_content else ""
                
                positive_count = sum(text_lower.count(word) for word in positive_keywords)
                negative_count = sum(text_lower.count(word) for word in negative_keywords)
                
                sentiment_score = (positive_count - negative_count) / max(positive_count + negative_count, 1)
                
                return {
                    'sentiment_score': sentiment_score,
                    'sentiment': 'positive' if sentiment_score > 0.1 else 'negative' if sentiment_score < -0.1 else 'neutral',
                    'positive_signals': positive_count,
                    'negative_signals': negative_count,
                    'news_source': ir_url
                }
        
        except Exception as e:
            logger.error(f"Error getting news sentiment for {company}: {e}")
        
        return {}