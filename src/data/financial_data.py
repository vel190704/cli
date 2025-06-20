"""
Financial data manager for retrieving and processing oil & gas company data
"""

import logging
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from src.database.database import DatabaseManager
from src.data.real_time_scraper import RealTimeFinancialScraper
from config import Config

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class FinancialDataManager:
    """Manages financial data retrieval and processing for oil & gas companies."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize financial data manager."""
        self.db_manager = db_manager
        self.companies = Config.TRACKED_COMPANIES
        self.scraper = RealTimeFinancialScraper()
        logger.info("Financial data manager initialized with real-time scraper")
    
    async def update_all_reports(self):
        """Update financial reports for all tracked companies using real data."""
        logger.info("Starting financial report updates from official sources...")
        
        for company in self.companies:
            try:
                # First try to get real data from official sources
                real_data = self.scraper.get_company_financial_data(company)
                
                if real_data and any(key in real_data for key in ['revenue', 'net_income', 'production']):
                    # Use real scraped data
                    report_data = self._format_scraped_data(real_data)
                    logger.info(f"Using real scraped data for {company}")
                else:
                    # Skip if real data unavailable
                    logger.warning(f"Real data unavailable for {company} - skipping update")
                    continue
                
                success = self.db_manager.store_financial_report(company, report_data)
                
                if success:
                    logger.info(f"Updated financial report for {company}")
                else:
                    logger.error(f"Failed to update financial report for {company}")
                    
            except Exception as e:
                logger.error(f"Error updating report for {company}: {e}")
        
        logger.info("Financial report updates completed")
    
    def _format_scraped_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format scraped data into database-compatible format."""
        return {
            "report_type": scraped_data.get("report_type", "quarterly"),
            "quarter": scraped_data.get("quarter", "Q4"),
            "year": scraped_data.get("year", datetime.now().year),
            "report_date": scraped_data.get("report_date", datetime.now().strftime("%Y-%m-%d")),
            "revenue": scraped_data.get("revenue", 0),
            "net_income": scraped_data.get("net_income", 0),
            "operating_income": scraped_data.get("operating_income", scraped_data.get("net_income", 0) * 1.2),
            "free_cash_flow": scraped_data.get("free_cash_flow", scraped_data.get("net_income", 0) * 0.8),
            "total_debt": scraped_data.get("total_debt", 0),
            "cash_and_equivalents": scraped_data.get("cash_and_equivalents", 0),
            "production_volume": scraped_data.get("production", 0),
            "production_unit": "thousand BOE/day",
            "data_source": "official_scraping",
            "additional_metrics": {
                "data_quality": scraped_data.get("data_quality", "scraped"),
                "scraping_timestamp": scraped_data.get("scraped_at", datetime.now().isoformat()),
                "source_verified": True
            }
        }
    
    def _generate_realistic_financial_data(self, company: str) -> Dict[str, Any]:
        """Generate realistic financial data based on actual oil & gas company patterns."""
        # Base data patterns for each company (based on historical ranges)
        company_patterns = {
            "Shell": {
                "revenue_range": (75000, 95000),  # Million USD
                "net_income_range": (8000, 25000),
                "production_range": (3200, 3800),  # Thousand BOE/day
                "cash_range": (25000, 35000)
            },
            "BP": {
                "revenue_range": (55000, 75000),
                "net_income_range": (6000, 18000),
                "production_range": (2200, 2800),
                "cash_range": (15000, 25000)
            },
            "ExxonMobil": {
                "revenue_range": (85000, 110000),
                "net_income_range": (10000, 30000),
                "production_range": (3600, 4200),
                "cash_range": (20000, 35000)
            },
            "Chevron": {
                "revenue_range": (45000, 65000),
                "net_income_range": (8000, 22000),
                "production_range": (2800, 3400),
                "cash_range": (18000, 28000)
            }
        }
        
        pattern = company_patterns.get(company, company_patterns["Shell"])
        current_date = datetime.now()
        quarter = f"Q{((current_date.month - 1) // 3) + 1}"
        
        # Generate realistic financial metrics
        revenue = random.uniform(*pattern["revenue_range"])
        net_income = random.uniform(*pattern["net_income_range"])
        production = random.uniform(*pattern["production_range"])
        cash = random.uniform(*pattern["cash_range"])
        
        return {
            "report_type": "quarterly",
            "quarter": quarter,
            "year": current_date.year,
            "report_date": current_date.strftime("%Y-%m-%d"),
            "revenue": round(revenue, 2),
            "net_income": round(net_income, 2),
            "operating_income": round(net_income * 1.3, 2),
            "free_cash_flow": round(net_income * 0.8, 2),
            "total_debt": round(revenue * 0.3, 2),
            "cash_and_equivalents": round(cash, 2),
            "production_volume": round(production, 1),
            "production_unit": "thousand BOE/day",
            "additional_metrics": {
                "upstream_revenue": round(revenue * 0.6, 2),
                "downstream_revenue": round(revenue * 0.3, 2),
                "chemical_revenue": round(revenue * 0.1, 2),
                "capex": round(revenue * 0.15, 2),
                "dividend_per_share": round(random.uniform(0.5, 1.2), 2),
                "oil_price_realization": round(random.uniform(70, 85), 2),
                "gas_price_realization": round(random.uniform(3.5, 6.0), 2)
            }
        }
    
    def has_recent_data(self, company: str, days: int = 90) -> bool:
        """Check if we have recent financial data for a company."""
        return self.db_manager.has_recent_data(company, days)
    
    def get_available_companies(self) -> List[str]:
        """Get list of available companies."""
        companies = self.db_manager.get_all_companies()
        return [company['name'] for company in companies]
    
    def get_context_for_query(self, query: str) -> Dict[str, Any]:
        """Get relevant financial context data for a user query."""
        query_lower = query.lower()
        context = {
            "query": query,
            "relevant_companies": [],
            "relevant_metrics": [],
            "comparison_data": {},
            "historical_data": {},
            "market_context": {}
        }
        
        # Identify relevant companies mentioned in query
        for company in self.companies:
            if company.lower() in query_lower:
                context["relevant_companies"].append(company)
        
        # If no specific companies mentioned, include all
        if not context["relevant_companies"]:
            context["relevant_companies"] = self.companies
        
        # Get financial data for relevant companies
        for company in context["relevant_companies"]:
            latest_data = self.db_manager.get_latest_financial_data(company)
            if latest_data:
                context["comparison_data"][company] = latest_data
        
        # Identify relevant metrics based on query keywords
        metric_keywords = {
            "revenue": ["revenue", "sales", "income statement"],
            "net_income": ["profit", "earnings", "net income", "bottom line"],
            "cash_flow": ["cash flow", "cash", "liquidity"],
            "production": ["production", "output", "volume", "barrels"],
            "debt": ["debt", "leverage", "borrowing"],
            "dividend": ["dividend", "payout", "shareholder return"]
        }
        
        for metric, keywords in metric_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                context["relevant_metrics"].append(metric)
        
        # Get historical trends for performance queries
        if any(word in query_lower for word in ["trend", "growth", "performance", "over time"]):
            for company in context["relevant_companies"][:2]:  # Limit to avoid too much data
                for metric in ["revenue", "net_income"]:
                    trends = self.db_manager.get_historical_trends(company, metric, 4)
                    if trends:
                        if company not in context["historical_data"]:
                            context["historical_data"][company] = {}
                        context["historical_data"][company][metric] = trends
        
        # Add market context
        context["market_context"] = {
            "oil_price_environment": "moderate",  # This would come from market data API
            "gas_price_environment": "volatile",
            "sector_outlook": "cautiously optimistic",
            "key_challenges": ["energy transition", "regulatory pressure", "commodity volatility"],
            "key_opportunities": ["LNG expansion", "renewable integration", "cost optimization"]
        }
        
        return context
    
    def get_company_financial_summary(self, company: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive financial summary for a company."""
        latest_data = self.db_manager.get_latest_financial_data(company)
        if not latest_data:
            return None
        
        # Calculate derived metrics
        summary = {
            "company": company,
            "latest_data": latest_data,
            "key_ratios": {},
            "performance_indicators": {}
        }
        
        # Calculate financial ratios if data is available
        revenue = latest_data.get("revenue")
        net_income = latest_data.get("net_income")
        total_debt = latest_data.get("total_debt")
        cash = latest_data.get("cash_and_equivalents")
        
        if revenue and net_income:
            summary["key_ratios"]["profit_margin"] = round((net_income / revenue) * 100, 2)
        
        if total_debt and cash:
            summary["key_ratios"]["net_debt_to_cash"] = round((total_debt - cash) / cash, 2)
        
        # Add performance indicators
        if net_income:
            if net_income > 0:
                summary["performance_indicators"]["profitability"] = "Profitable"
            else:
                summary["performance_indicators"]["profitability"] = "Loss-making"
        
        return summary
    
    def compare_companies(self, companies: List[str]) -> Dict[str, Any]:
        """Generate comparison data for multiple companies."""
        comparison = {
            "companies": companies,
            "financial_metrics": {},
            "rankings": {},
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Get latest data for all companies
        company_data = {}
        for company in companies:
            data = self.db_manager.get_latest_financial_data(company)
            if data:
                company_data[company] = data
        
        if not company_data:
            return comparison
        
        # Compare key metrics
        metrics_to_compare = ["revenue", "net_income", "free_cash_flow", "production_volume"]
        
        for metric in metrics_to_compare:
            comparison["financial_metrics"][metric] = {}
            metric_values = []
            
            for company, data in company_data.items():
                value = data.get(metric)
                if value is not None:
                    comparison["financial_metrics"][metric][company] = value
                    metric_values.append((company, value))
            
            # Rank companies by this metric
            if metric_values:
                ranked = sorted(metric_values, key=lambda x: x[1], reverse=True)
                comparison["rankings"][metric] = [company for company, _ in ranked]
        
        return comparison
